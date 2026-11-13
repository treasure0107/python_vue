from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db_conf import AsyncSessionLocal, Base, engine, settings
from crud.news_category import ensure_default_categories
import models  # noqa: F401
from routers import auth as auth_router
from routers import news as news_router
from routers import users as users_router
from utils.exception_handlers import register_exception_handlers
from utils.redis_cache import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await ensure_default_categories(db)
        from crud.users import ensure_default_admin

        await ensure_default_admin(db)
    yield
    await engine.dispose()
    close_redis()


app = FastAPI(title=settings.app_title, debug=settings.debug, lifespan=lifespan)

register_exception_handlers(app)
#允许的来源(可以是域名列表)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api")
app.include_router(users_router.router, prefix="/api")
app.include_router(news_router.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "头条资讯 API", "docs": "/docs"}
