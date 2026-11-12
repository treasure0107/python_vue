"""手动确保默认 admin 账号存在。用法: python scripts/ensure_admin.py"""

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.db_conf import AsyncSessionLocal
from crud.users import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME, ensure_default_admin


async def main() -> None:
    async with AsyncSessionLocal() as db:
        await ensure_default_admin(db)
    print(f"已校验默认账号: {DEFAULT_ADMIN_USERNAME} / {DEFAULT_ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
