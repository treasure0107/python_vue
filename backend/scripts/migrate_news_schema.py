"""将旧版 news（category 字符串）迁移为 category_id 结构；必要时重建 news 子表。"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import text

import models  # noqa: F401
from config.db_conf import Base, engine


async def main() -> None:
    async with engine.begin() as conn:
        r = await conn.execute(text("SHOW COLUMNS FROM news LIKE 'category_id'"))
        if r.first() is not None:
            print("news 表已是新结构，无需迁移。")
            await engine.dispose()
            return
        await conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for table in ("history", "favorite", "news"):
            await conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
        await conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(
                bind=sync_conn,
                tables=[
                    Base.metadata.tables["news"],
                    Base.metadata.tables["favorite"],
                    Base.metadata.tables["history"],
                ],
            )
        )
    print("已重建 news / favorite / history 表。")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
