"""
写入演示新闻数据（与 UI 稿一致），并补齐 news.source 字段（若库表较旧）。

用法：python scripts/seed_news.py
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import select, text

import models  # noqa: F401
from config.db_conf import AsyncSessionLocal, engine
from crud.news_category import ensure_default_categories, get_category_by_name
from models.news import News

SEED_ITEMS = [
    {
        "title": "国家主席发表2024年新年贺词",
        "summary": "主席总结过去一年成就，展望未来发展蓝图，强调高质量发展。",
        "source": "新华社",
        "view_count": 12517,
        "category": "头条",
        "cover_url": "https://picsum.photos/seed/toutiao1/400/240",
        "content": (
            "新年前夕，国家主席发表二〇二四年新年贺词。"
            "贺词回顾了过去一年国家发展取得的重大成就，展望全面建设社会主义现代化国家新征程，"
            "号召全国人民坚定信心、开拓奋进，以高质量发展推进中国式现代化。"
        ),
    },
    {
        "title": "我国成功发射通信技术试验卫星十一号",
        "summary": "长征二号丁运载火箭在西昌卫星发射中心点火升空，卫星准确进入预定轨道。",
        "source": "央视新闻",
        "view_count": 11231,
        "category": "国内",
        "cover_url": "https://picsum.photos/seed/toutiao2/400/240",
        "content": (
            "2024年1月10日15时03分，我国在西昌卫星发射中心使用长征二号丁运载火箭，"
            "成功将通信技术试验卫星十一号发射升空，卫星顺利进入预定轨道，发射任务获得圆满成功。"
            "此次任务是长征系列运载火箭的第492次飞行。"
        ),
    },
    {
        "title": "多地推出惠民政策 助力春运出行",
        "summary": "交通、民航部门协同保障春运高峰，加开临客与夜间高铁。",
        "source": "人民日报",
        "view_count": 8650,
        "category": "社会",
        "cover_url": "https://picsum.photos/seed/toutiao3/400/240",
        "content": "春运期间，多地推出惠民出行政策，强化重点枢纽运力投放，方便群众平安返乡。",
    },
    {
        "title": "国际组织积极评价中国经济韧性",
        "summary": "多家机构上调对中国增长预期，看好高水平对外开放。",
        "source": "新华社",
        "view_count": 6421,
        "category": "国际",
        "cover_url": "https://picsum.photos/seed/toutiao4/400/240",
        "content": "国际舆论普遍认为，中国经济回升向好势头巩固，将为世界经济复苏注入更多确定性。",
    },
    {
        "title": "年度大片定档春节档 多部影片发布预告",
        "summary": "喜剧、动画、科幻类型齐聚，观众期待值持续攀升。",
        "source": "娱乐周刊",
        "view_count": 15880,
        "category": "娱乐",
        "cover_url": "https://picsum.photos/seed/toutiao5/400/240",
        "content": "春节档临近，多部新片陆续定档并发布预告片，票房市场被普遍看好。",
    },
    {
        "title": "亚洲杯小组赛开幕 国足首战迎考验",
        "summary": "国家队小组赛首战对阵强敌，教练组强调防守反击。",
        "source": "央视体育",
        "view_count": 22103,
        "category": "体育",
        "cover_url": "https://picsum.photos/seed/toutiao6/400/240",
        "content": "亚洲杯正式拉开帷幕，中国队首战备受关注，球队力争小组出线。",
    },
]


async def ensure_source_column() -> None:
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE news ADD COLUMN source VARCHAR(64) NULL"))
        except Exception:
            pass


async def seed() -> None:
    await ensure_source_column()

    async with AsyncSessionLocal() as db:
        await ensure_default_categories(db)

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(News.id).limit(1))
        if result.scalar_one_or_none() is not None:
            print("新闻表已有数据，跳过重复灌入（可先清空 news 表再执行）。")
            await engine.dispose()
            return

        await ensure_default_categories(db)

        published = datetime(2024, 1, 10, 18, 20, 0)
        for item in SEED_ITEMS:
            cat = await get_category_by_name(db, item["category"])
            if not cat:
                continue
            db.add(
                News(
                    title=item["title"],
                    summary=item["summary"],
                    content=item["content"],
                    source=item["source"],
                    category_id=cat.id,
                    cover_url=item["cover_url"],
                    view_count=item["view_count"],
                    created_at=published,
                    updated_at=published,
                )
            )
        await db.commit()
        print(f"已插入 {len(SEED_ITEMS)} 条演示新闻。")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
