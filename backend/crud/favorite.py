"""用户收藏 CRUD。"""

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News
from schemas.favorite import FavoriteListItem


async def is_favorited(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """当前用户是否已收藏该资讯。"""
    result = await db.execute(
        select(Favorite.id).where(
            Favorite.user_id == user_id,
            Favorite.news_id == news_id,
        )
    )
    return result.scalar_one_or_none() is not None


async def _get_favorite_row(
    db: AsyncSession, user_id: int, news_id: int
) -> Favorite | None:
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.news_id == news_id,
        )
    )
    return result.scalar_one_or_none()


async def add_favorite(db: AsyncSession, user_id: int, news_id: int) -> Favorite:
    """添加收藏；已存在或并发重复插入时返回已有记录。"""
    row = await _get_favorite_row(db, user_id, news_id)
    if row:
        return row
    row = Favorite(user_id=user_id, news_id=news_id)
    db.add(row)
    try:
        await db.commit()
        await db.refresh(row)
        return row
    except IntegrityError:
        await db.rollback()
        existing = await _get_favorite_row(db, user_id, news_id)
        if existing is None:
            raise
        return existing


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """取消收藏，返回是否删除成功。"""
    result = await db.execute(
        delete(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.news_id == news_id,
        )
    )
    await db.commit()
    return (result.rowcount or 0) > 0


async def clear_favorites(db: AsyncSession, user_id: int) -> int:
    """清空该用户全部收藏，返回删除条数。"""
    result = await db.execute(delete(Favorite).where(Favorite.user_id == user_id))
    await db.commit()
    return int(result.rowcount or 0)


async def list_user_favorites(
    db: AsyncSession,
    user_id: int,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[FavoriteListItem]:
    """收藏列表：按收藏时间倒序，附带新闻摘要字段。"""
    stmt = (
        select(Favorite, News)
        .join(News, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    rows = (await db.execute(stmt)).all()
    items: list[FavoriteListItem] = []
    seen_news_ids: set[int] = set()
    for fav, news in rows:
        if news.id in seen_news_ids:
            continue
        seen_news_ids.add(news.id)
        items.append(
            FavoriteListItem(
                news_id=news.id,
                title=news.title,
                cover_url=news.cover_url,
                source=news.source,
                published_at=news.created_at,
                favorited_at=fav.created_at,
            )
        )
    return items


async def toggle_favorite(
    db: AsyncSession, user_id: int, news_id: int
) -> bool:
    """切换收藏；返回切换后是否为已收藏。"""
    if await is_favorited(db, user_id, news_id):
        await remove_favorite(db, user_id, news_id)
        return False
    await add_favorite(db, user_id, news_id)
    return True


async def toggle_favorite_checked(
    db: AsyncSession, user_id: int, news_id: int
):
    """
    切换收藏（校验资讯存在）。
    资讯不存在返回 None，否则返回 FavoriteToggleData。
    """
    from crud import news as news_crud
    from schemas.favorite import FavoriteToggleData

    if not await news_crud.get_news(db, news_id):
        return None
    favorited = await toggle_favorite(db, user_id, news_id)
    return FavoriteToggleData(news_id=news_id, favorited=favorited)
