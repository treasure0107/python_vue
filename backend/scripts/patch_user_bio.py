"""为 user 表增加 bio 字段（可重复执行）。用法: python scripts/patch_user_bio.py"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import text

from config.db_conf import AsyncSessionLocal, engine
from crud.users import DEFAULT_ADMIN_USERNAME, ensure_default_admin, get_user_by_username

DEFAULT_BIO = "这是一个测试账号"
DEFAULT_AVATAR = "https://picsum.photos/seed/toutiao-cat/200/200"


async def patch() -> None:
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE user ADD COLUMN bio VARCHAR(512) NULL"))
            print("已添加 user.bio 列")
        except Exception:
            print("user.bio 已存在，跳过 DDL")

    async with AsyncSessionLocal() as db:
        await ensure_default_admin(db)
        admin = await get_user_by_username(db, DEFAULT_ADMIN_USERNAME)
        if admin:
            updated = False
            if not admin.bio:
                admin.bio = DEFAULT_BIO
                updated = True
            if not admin.avatar:
                admin.avatar = DEFAULT_AVATAR
                updated = True
            if updated:
                await db.commit()
                print("已补全 admin 个人简介与头像")
        print("patch_user_bio 完成")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(patch())
