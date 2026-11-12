"""为 news_category 表补充 updated_at 字段（已有库执行一次即可）。"""

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import text

from config.db_conf import engine


async def main() -> None:
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text(
                    "ALTER TABLE news_category ADD COLUMN updated_at "
                    "DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
                )
            )
            print("已添加 news_category.updated_at")
        except Exception as exc:
            print("跳过（可能已存在）:", exc)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
