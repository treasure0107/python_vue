"""
为下拉「加载更多」插入 33 条测试新闻（默认归入「头条」分类）。

用法（在 backend 目录）：
  python scripts/seed_news_pagination.py
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import select

import models  # noqa: F401
from config.db_conf import AsyncSessionLocal, engine
from crud.news_category import ensure_default_categories, get_category_by_name
from models.news import News

TITLE_PREFIX = "【分页测试】"
CATEGORY_NAME = "头条"
COUNT = 33


async def seed_pagination_news() -> None:
    async with AsyncSessionLocal() as db:
        await ensure_default_categories(db)
        cat = await get_category_by_name(db, CATEGORY_NAME)
        if not cat:
            print(f"分类「{CATEGORY_NAME}」不存在，请先执行 init_db / seed_news。")
            await engine.dispose()
            return

        result = await db.execute(
            select(News.title).where(News.title.like(f"{TITLE_PREFIX}%"))
        )
        existing_titles = set(result.scalars().all())
        base_time = datetime.now(timezone.utc)
        added = 0

        for i in range(1, COUNT + 1):
            title = f"{TITLE_PREFIX}第{i:02d}条 · 滚动加载验证"
            if title in existing_titles:
                continue
            published = base_time - timedelta(minutes=i)
            db.add(
                News(
                    title=title,
                    summary=f"用于分页加载更多测试的第 {i} 条示例摘要，分类：{CATEGORY_NAME}。",
                    content=(
                        f"本条为分页测试数据（序号 {i}/{COUNT}）。"
                        f"前端 pageSize=20 时，「{CATEGORY_NAME}」分类下数据足够触发第二页与 hasMore。"
                    ),
                    source="测试数据",
                    category_id=cat.id,
                    cover_url=f"https://picsum.photos/seed/pagetest{i:02d}/400/240",
                    view_count=100 + i,
                    created_at=published,
                    updated_at=published,
                )
            )
            added += 1

        if added == 0:
            print(f"已存在 {COUNT} 条「{TITLE_PREFIX}」测试新闻，未重复插入。")
        else:
            await db.commit()
            print(f"已在「{CATEGORY_NAME}」插入 {added} 条分页测试新闻（目标共 {COUNT} 条同类标题）。")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_pagination_news())
