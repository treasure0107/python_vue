from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.news_category import NewsCategory
from schemas.news_category import NewsCategoryOut

# 与前端「全部分类」一致，列表/详情/相关推荐共用同一套接口规则
DEFAULT_CATEGORIES = (
    "头条",
    "社会",
    "国内",
    "国际",
    "娱乐",
    "体育",
    "科技",
    "财经",
    "推荐",
    "热点",
    "视频",
    "军事",
)


async def get_category_by_id(db: AsyncSession, category_id: int) -> NewsCategory | None:
    result = await db.execute(select(NewsCategory).where(NewsCategory.id == category_id))
    return result.scalar_one_or_none()


async def get_category_by_name(db: AsyncSession, name: str) -> NewsCategory | None:
    result = await db.execute(select(NewsCategory).where(NewsCategory.name == name))
    return result.scalar_one_or_none()


def categories_to_out(rows: list[NewsCategory]) -> list[NewsCategoryOut]:
    return [NewsCategoryOut.model_validate(row) for row in rows]


async def list_category_out(db: AsyncSession) -> list[NewsCategoryOut]:
    rows = await list_active_categories(db)
    return categories_to_out(rows)


async def list_active_categories(db: AsyncSession) -> list[NewsCategory]:
    stmt = (
        select(NewsCategory)
        .where(NewsCategory.is_active.is_(True))
        .order_by(NewsCategory.sort_order, NewsCategory.id)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def ensure_default_categories(db: AsyncSession) -> None:
    """补齐 DEFAULT_CATEGORIES 中缺失的分类（不修改已存在记录的 sort_order）。"""
    result = await db.execute(select(NewsCategory.name))
    existing = {name for name in result.scalars().all()}
    for idx, name in enumerate(DEFAULT_CATEGORIES):
        if name in existing:
            continue
        db.add(NewsCategory(name=name, sort_order=idx, is_active=True))
    await db.commit()


async def resolve_category_id(
    db: AsyncSession, *, category_id: int | None, category: str | None
) -> int:
    if category_id is not None:
        row = await get_category_by_id(db, category_id)
        if row:
            return row.id
    name = category or "推荐"
    row = await get_category_by_name(db, name)
    if row:
        return row.id
    row = NewsCategory(name=name, sort_order=99, is_active=True)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row.id
