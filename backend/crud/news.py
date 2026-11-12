"""资讯表 CRUD：查询、分页列表、详情（浏览量+1）、相关推荐与 Redis 缓存封装。"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud import news_cache
from crud import news_category as category_crud
from models.news import News
from models.news_category import NewsCategory
from schemas.news import (
    NewsCreate,
    NewsDetailData,
    NewsListItem,
    NewsListPageData,
    NewsOut,
    NewsRelatedItem,
    NewsUpdate,
)

# 详情页「相关推荐」条数上限（浏览量优先 + 发布时间次之）
RELATED_NEWS_LIMIT = 5


def news_to_related_item(news: News) -> NewsRelatedItem:
    """ORM 行 → 详情页相关新闻列表项。"""
    return NewsRelatedItem(
        id=news.id,
        title=news.title,
        cover_url=news.cover_url,
        description=news.summary,
        source=news.source,
        view_count=news.view_count,
    )


def news_to_detail_data(news: News, related: list[News]) -> NewsDetailData:
    """ORM 行与相关列表 → 详情 API 响应体（views 取自 view_count）。"""
    return NewsDetailData(
        id=news.id,
        title=news.title,
        content=news.content,
        views=news.view_count,
        summary=news.summary,
        cover_url=news.cover_url,
        source=news.source,
        category=news.category.name if news.category else None,
        category_id=news.category_id,
        created_at=news.created_at,
        relatedNews=[news_to_related_item(row) for row in related],
    )


def news_to_list_item(news: News) -> NewsListItem:
    """ORM 行 → 分页列表项（无正文，summary 映射为 description）。"""
    return NewsListItem(
        id=news.id,
        category_id=news.category_id,
        category=news.category.name if news.category else None,
        title=news.title,
        description=news.summary,
        cover_url=news.cover_url,
        source=news.source,
        view_count=news.view_count,
        created_at=news.created_at,
    )


def news_to_out(news: News) -> NewsOut:
    """ORM 行 → 完整资讯输出（含正文，供旧列表/缓存/管理接口）。"""
    return NewsOut(
        id=news.id,
        title=news.title,
        summary=news.summary,
        content=news.content,
        cover_url=news.cover_url,
        source=news.source,
        author_id=news.author_id,
        category_id=news.category_id,
        category=news.category.name if news.category else "推荐",
        view_count=news.view_count,
        created_at=news.created_at,
        updated_at=news.updated_at,
    )


async def get_news(db: AsyncSession, news_id: int) -> News | None:
    """按主键查询单条新闻，并预加载分类关系。"""
    stmt = (
        select(News)
        .options(selectinload(News.category))
        .where(News.id == news_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def count_news_by_category_id(db: AsyncSession, category_id: int) -> int:
    """统计某分类下的新闻总数（分页 hasMore 用）。"""
    stmt = select(func.count()).select_from(News).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return int(result.scalar_one())


async def get_related_news_by_category(
    db: AsyncSession,
    *,
    category_id: int,
    exclude_id: int,
    limit: int = RELATED_NEWS_LIMIT,
) -> list[News]:
    """同分类、排除当前 id。排序：浏览量最高优先；浏览量相同则发布时间最新优先；取前 limit 条。"""
    stmt = (
        select(News)
        .options(selectinload(News.category))
        .where(News.category_id == category_id, News.id != exclude_id)
        .order_by(News.view_count.desc(), News.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_news_list_by_category_id(
    db: AsyncSession,
    category_id: int,
    *,
    page: int = 1,
    page_size: int = 10,
) -> list[News]:
    """按分类 id 分页查询（page/page_size 会做边界修正，最大 100 条/页）。"""
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    if page_size > 100:
        page_size = 100
    skip = (page - 1) * page_size
    stmt = (
        select(News)
        .options(selectinload(News.category))
        .where(News.category_id == category_id)
        .order_by(News.created_at.desc())
        .offset(skip)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_news_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    category: str | None = None,
) -> list[News]:
    """旧版列表：skip/limit，可选按分类名称过滤。"""
    stmt = select(News).options(selectinload(News.category))
    if category:
        stmt = stmt.join(NewsCategory).where(NewsCategory.name == category)
    stmt = stmt.order_by(News.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_news(db: AsyncSession, news_in: NewsCreate) -> News:
    """写入新闻；解析 category_id / 分类名后入库并返回带分类的实体。"""
    cid = await category_crud.resolve_category_id(
        db, category_id=news_in.category_id, category=news_in.category
    )
    payload = news_in.model_dump(exclude={"category", "category_id"})
    db_news = News(**payload, category_id=cid)
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return await get_news(db, db_news.id)  # type: ignore[arg-type]


async def update_news(db: AsyncSession, db_news: News, news_in: NewsUpdate) -> News:
    """部分字段更新；若携带分类信息则先 resolve category_id。"""
    data = news_in.model_dump(exclude_unset=True)
    if "category" in data or "category_id" in data:
        cid = await category_crud.resolve_category_id(
            db,
            category_id=data.pop("category_id", None),
            category=data.pop("category", None),
        )
        data["category_id"] = cid
    for field, value in data.items():
        setattr(db_news, field, value)
    await db.commit()
    await db.refresh(db_news)
    return await get_news(db, db_news.id)  # type: ignore[arg-type]


async def delete_news(db: AsyncSession, db_news: News) -> None:
    """物理删除一条新闻。"""
    await db.delete(db_news)
    await db.commit()


async def increment_view_count(db: AsyncSession, db_news: News) -> News:
    """浏览量 +1 并提交，返回刷新后带分类的完整行（详情接口主路径）。"""
    db_news.view_count = db_news.view_count + 1
    await db.commit()
    await db.refresh(db_news)
    return await get_news(db, db_news.id)  # type: ignore[arg-type]


async def increment_view_count_by_id(db: AsyncSession, news_id: int) -> None:
    """仅按 id 将 view_count +1（命中详情缓存时使用，不返回实体）。"""
    result = await db.execute(select(News).where(News.id == news_id))
    row = result.scalar_one_or_none()
    if row is None:
        return
    row.view_count = row.view_count + 1
    await db.commit()


async def get_category_list(db: AsyncSession):
    """返回全部分类 DTO 列表。"""
    return await category_crud.list_category_out(db)


# ---------- 供路由调用的业务方法（含缓存） ----------


async def list_news_page(
    db: AsyncSession,
    category_id: int,
    *,
    page: int = 1,
    page_size: int = 10,
) -> NewsListPageData:
    """分页列表业务：优先 Redis，未命中则查库并写缓存，组装 list/total/hasMore。"""
    if page_size > 100:
        page_size = 100
    cached = news_cache.get_cached_news_page(category_id, page, page_size)
    if cached:
        return NewsListPageData.model_validate(cached)

    total = await count_news_by_category_id(db, category_id)
    rows = await get_news_list_by_category_id(
        db, category_id, page=page, page_size=page_size
    )
    items = [news_to_list_item(n) for n in rows]
    has_more = page * page_size < total
    payload = NewsListPageData(list=items, total=total, hasMore=has_more)
    news_cache.set_cached_news_page(category_id, page, page_size, payload)
    return payload


async def list_categories_cached(db: AsyncSession) -> list:
    """分类列表（带 Redis 缓存）。"""
    from schemas.news_category import NewsCategoryOut

    cached = news_cache.get_cached_categories()
    if cached and isinstance(cached[0], dict):
        return [NewsCategoryOut.model_validate(item) for item in cached]
    categories = await get_category_list(db)
    news_cache.set_cached_categories(categories)
    return categories


async def list_news_cached(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 20,
    category: str | None = None,
) -> list[NewsOut]:
    """旧版列表业务（带 Redis 缓存）。"""
    cached = news_cache.get_cached_news_list(category, skip, limit)
    if cached is not None:
        return [NewsOut.model_validate(item) for item in cached]
    items = await get_news_list(db, skip=skip, limit=limit, category=category)
    out = [news_to_out(n) for n in items]
    news_cache.set_cached_news_list(category, skip, limit, out)
    return out


async def get_news_detail_with_related(
    db: AsyncSession, news_id: int
) -> NewsDetailData | None:
    """详情：查新闻 → 浏览量+1 → 同分类相关推荐 → 更新详情缓存快照。"""
    db_news = await get_news(db, news_id)
    if not db_news:
        return None
    db_news = await increment_view_count(db, db_news)
    related = await get_related_news_by_category(
        db,
        category_id=db_news.category_id,
        exclude_id=news_id,
        limit=RELATED_NEWS_LIMIT,
    )
    out = news_to_detail_data(db_news, related)
    news_cache.set_cached_news_detail(news_id, news_to_out(db_news))
    return out


async def get_news_detail_cached(db: AsyncSession, news_id: int) -> NewsOut | None:
    """旧详情形态 NewsOut；命中缓存仍会 +1 浏览量（返回体中阅读量可能滞后）。"""
    cached = news_cache.get_cached_news_detail(news_id)
    if cached is not None:
        await increment_view_count_by_id(db, news_id)
        return NewsOut.model_validate(cached)
    db_news = await get_news(db, news_id)
    if not db_news:
        return None
    db_news = await increment_view_count(db, db_news)
    out = news_to_out(db_news)
    news_cache.set_cached_news_detail(news_id, out)
    return out


async def create_news_item(db: AsyncSession, news_in: NewsCreate) -> NewsOut:
    """创建新闻并失效资讯相关缓存。"""
    created = await create_news(db, news_in)
    news_cache.invalidate_after_news_write()
    return news_to_out(created)


async def update_news_item(
    db: AsyncSession, news_id: int, news_in: NewsUpdate
) -> NewsOut | None:
    """更新新闻；不存在返回 None，成功后失效缓存。"""
    db_news = await get_news(db, news_id)
    if not db_news:
        return None
    updated = await update_news(db, db_news, news_in)
    news_cache.invalidate_after_news_write(news_id)
    return news_to_out(updated)


async def delete_news_item(db: AsyncSession, news_id: int) -> bool:
    """删除新闻；不存在返回 False，成功后失效缓存。"""
    db_news = await get_news(db, news_id)
    if not db_news:
        return False
    await delete_news(db, db_news)
    news_cache.invalidate_after_news_write(news_id)
    return True
