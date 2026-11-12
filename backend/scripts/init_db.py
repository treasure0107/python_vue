"""
本地初始化 MySQL 库与六张业务表（异步 ORM：create_async_engine + run_sync 建表）。

用法（在 backend 目录）:
    python scripts/init_db.py
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

import models  # noqa: F401
from config.db_conf import AsyncSessionLocal, Base, engine, settings, to_async_url
from crud.news_category import ensure_default_categories


def ensure_database_exists() -> None:
    url = make_url(to_async_url(settings.database_url))
    if not url.drivername.startswith("mysql"):
        return
    db_name = url.database
    if not db_name:
        return
    sync_url = url.set(drivername="mysql+pymysql")
    server_url = sync_url.set(database=None)
    server_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "", db_name)
    if safe_name != db_name:
        raise ValueError(f"非法库名: {db_name}")
    with server_engine.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{safe_name}` "
                "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    server_engine.dispose()


async def create_tables() -> None:
    ensure_database_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await ensure_default_categories(db)


async def main_async() -> None:
    await create_tables()
    tables = sorted(Base.metadata.tables.keys())
    print("数据库初始化完成，已创建/校验表：")
    for name in tables:
        print(f"  - {name}")
    await engine.dispose()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
