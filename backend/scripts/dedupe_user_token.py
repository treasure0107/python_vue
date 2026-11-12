"""
清理 user_token：同一 user_id 只保留最新一条（id 最大）。

用法（在 backend 目录）:
    .venv\\Scripts\\python.exe scripts\\dedupe_user_token.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import text

from config.db_conf import AsyncSessionLocal


async def main() -> None:
    sql = """
    DELETE t1 FROM user_token t1
    INNER JOIN user_token t2
      ON t1.user_id = t2.user_id AND t1.id < t2.id
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(text(sql))
        await db.commit()
        print(f"已删除重复令牌行数: {result.rowcount}")


if __name__ == "__main__":
    asyncio.run(main())
