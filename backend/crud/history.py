"""用户浏览历史 CRUD。"""

from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News
from schemas.history import (
    HistoryListItem,
    HistoryListPageData,
    HistoryRecordOut,
)
from utils.cache_invalidate import invalidate_user_history


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _history_to_record(row: History) -> HistoryRecordOut:
    return HistoryRecordOut(
        id=row.id,
        user_id=row.user_id,
        news_id=row.news_id,
        viewed_at=row.viewed_at or _utcnow(),
    )


async def _get_history_row(
    db: AsyncSession, user_id: int, news_id: int
) -> History | None:
    result = await db.execute(
        select(History).where(
            History.user_id == user_id,
            History.news_id == news_id,
        )
    )
    return result.scalar_one_or_none()


async def upsert_history(
    db: AsyncSession, user_id: int, news_id: int
) -> History:
    """
    添加或更新浏览记录：未浏览过则插入，已浏览过则更新 viewed_at。
    """
    row = await _get_history_row(db, user_id, news_id)
    now = _utcnow()
    if row:
        row.viewed_at = now
        await db.commit()
        await db.refresh(row)
    else:
        row = History(user_id=user_id, news_id=news_id, viewed_at=now)
        db.add(row)
        await db.commit()
        await db.refresh(row)
    invalidate_user_history(user_id)
    return row


async def add_history_checked(
    db: AsyncSession, user_id: int, news_id: int
) -> HistoryRecordOut | None:
    """校验资讯存在后 upsert，不存在返回 None。"""
    from crud import news as news_crud

    if not await news_crud.get_news(db, news_id):
        return None
    row = await upsert_history(db, user_id, news_id)
    return _history_to_record(row)


async def list_history_page(
    db: AsyncSession,
    user_id: int,
    *,
    page: int = 1,
    page_size: int = 10,
) -> HistoryListPageData:
    """联表查询浏览历史：按 viewed_at 倒序，附带 total / hasMore。"""
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    if page_size > 100:
        page_size = 100

    total_stmt = select(func.count(History.id)).where(History.user_id == user_id)
    total = int((await db.execute(total_stmt)).scalar_one())

    offset = (page - 1) * page_size
    stmt = (
        select(History, News)
        .join(News, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.viewed_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    rows = (await db.execute(stmt)).all()
    items: list[HistoryListItem] = []
    for hist, news in rows:
        items.append(
            HistoryListItem(
                id=hist.id,
                news_id=news.id,
                title=news.title,
                cover_url=news.cover_url,
                source=news.source,
                published_at=news.created_at,
                viewed_at=hist.viewed_at,
            )
        )
    has_more = offset + len(items) < total
    return HistoryListPageData(list=items, total=total, hasMore=has_more)


async def remove_history_by_id(
    db: AsyncSession, user_id: int, history_id: int
) -> bool:
    """删除单条历史（仅限当前用户）。"""
    result = await db.execute(
        delete(History).where(
            History.id == history_id,
            History.user_id == user_id,
        )
    )
    await db.commit()
    if (result.rowcount or 0) > 0:
        invalidate_user_history(user_id)
        return True
    return False


async def clear_user_history(db: AsyncSession, user_id: int) -> int:
    """清空用户浏览历史。"""
    result = await db.execute(delete(History).where(History.user_id == user_id))
    await db.commit()
    removed = int(result.rowcount or 0)
    if removed:
        invalidate_user_history(user_id)
    return removed
