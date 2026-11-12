from collections.abc import AsyncGenerator
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "mysql+aiomysql://root@127.0.0.1:3306/toutiao?charset=utf8mb4"
    )
    app_title: str = "头条资讯 API"
    debug: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


class Base(DeclarativeBase):
    """ORM 模型基类（继承 DeclarativeBase）。"""


def to_async_url(url: str) -> str:
    if url.startswith("sqlite://") and "+aiosqlite" not in url:
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    if "mysql+pymysql://" in url:
        return url.replace("mysql+pymysql://", "mysql+aiomysql://", 1)
    if url.startswith("mysql://"):
        return url.replace("mysql://", "mysql+aiomysql://", 1)
    return url


def _create_async_engine():
    url = to_async_url(settings.database_url)
    if url.startswith("sqlite"):
        return create_async_engine(url, echo=settings.debug)
    return create_async_engine(
        url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


engine = _create_async_engine()
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """路由注入：Depends(get_db) 获取异步会话。"""
    async with AsyncSessionLocal() as session:
        yield session
