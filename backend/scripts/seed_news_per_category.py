"""
为每个分类补足至少 30 条新闻（列表分页 / 详情 / 相关推荐使用同一套后端规则）。

用法（backend 目录）：
  python scripts/seed_news_per_category.py
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import func, select

import models  # noqa: F401
from config.db_conf import AsyncSessionLocal, engine
from crud.news_category import DEFAULT_CATEGORIES, ensure_default_categories, get_category_by_name
from models.news import News
from models.news_category import NewsCategory
from utils.redis_cache import cache_delete_by_pattern
from config.cache_conf import PATTERN_NEWS_LIST

MIN_PER_CATEGORY = 30
TITLE_PREFIX = "【频道种子·"


async def ensure_all_categories(db) -> list[NewsCategory]:
    """确保 12 个默认分类存在，并按 DEFAULT_CATEGORIES 顺序写入 sort_order。"""
    await ensure_default_categories(db)
    rows: list[NewsCategory] = []
    for idx, name in enumerate(DEFAULT_CATEGORIES):
        row = await get_category_by_name(db, name)
        if not row:
            row = NewsCategory(name=name, sort_order=idx, is_active=True)
            db.add(row)
            await db.flush()
        elif row.sort_order != idx:
            row.sort_order = idx
        rows.append(row)
    await db.commit()
    return rows


async def count_by_category(db, category_id: int) -> int:
    stmt = select(func.count()).select_from(News).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return int(result.scalar_one())


async def seed_per_category() -> None:
    async with AsyncSessionLocal() as db:
        categories = await ensure_all_categories(db)
        base_time = datetime.now(timezone.utc)
        total_added = 0

        for cat_index, cat in enumerate(categories):
            existing = await count_by_category(db, cat.id)
            need = max(0, MIN_PER_CATEGORY - existing)
            if need == 0:
                print(f"「{cat.name}」已有 {existing} 条，跳过。")
                continue

            for seq in range(1, need + 1):
                global_seq = existing + seq
                title = f"{TITLE_PREFIX}{cat.name}】第{global_seq:02d}条"
                dup = await db.execute(select(News.id).where(News.title == title))
                if dup.scalar_one_or_none() is not None:
                    continue
                # 浏览量、发布时间错开，便于验证相关推荐（浏览量优先、时间次之）
                view_count = 80 + cat_index * 50 + global_seq * 3
                published = base_time - timedelta(days=cat_index, hours=global_seq)
                db.add(
                    News(
                        title=title,
                        summary=f"{cat.name}频道示例摘要 #{global_seq}，用于全分类列表与分页联调。",
                        content=(
                            f"本条属于「{cat.name}」频道测试数据（{global_seq}/{MIN_PER_CATEGORY}+）。"
                            "列表：GET /api/news/list；详情含 relatedNews，规则全频道一致。"
                        ),
                        source="频道种子",
                        category_id=cat.id,
                        cover_url=f"https://picsum.photos/seed/{cat.name}{global_seq:02d}/400/240",
                        view_count=view_count,
                        created_at=published,
                        updated_at=published,
                    )
                )
                total_added += 1

            await db.commit()
            after = await count_by_category(db, cat.id)
            print(f"「{cat.name}」新增 {need} 条，当前共 {after} 条。")

        if total_added:
            cache_delete_by_pattern(PATTERN_NEWS_LIST)
            cache_delete_by_pattern("news:detail:*")
            print(f"已清理列表/详情缓存。本次共插入 {total_added} 条。")
        else:
            print("所有分类均已满足 30 条，无需插入。")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_per_category())
