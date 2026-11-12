"""
将已有 MySQL user_token 表结构与 models/user_token.py 对齐。

用法（在 backend 目录）:
    .venv\\Scripts\\python.exe scripts\\migrate_user_token.py
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
    alters = [
        "ALTER TABLE user_token MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT COMMENT '令牌ID'",
        "ALTER TABLE user_token MODIFY COLUMN user_id INT NOT NULL COMMENT '用户ID'",
        "ALTER TABLE user_token MODIFY COLUMN token VARCHAR(255) NOT NULL COMMENT '令牌值'",
        "ALTER TABLE user_token MODIFY COLUMN expires_at DATETIME NOT NULL COMMENT '过期时间'",
        (
            "ALTER TABLE user_token MODIFY COLUMN created_at DATETIME NOT NULL "
            "DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'"
        ),
    ]
    drop_indexes = (
        "ix_user_token_token",
        "ix_user_token_id",
        "ix_user_token_user_id",  # 历史遗留，与 fk_user_token_user_idx 重复
        "uq_user_token",
        "token_UNIQUE",
        "fk_user_token_user_idx",
    )

    async with AsyncSessionLocal() as db:
        for stmt in alters:
            await db.execute(text(stmt))
        for idx in drop_indexes:
            try:
                await db.execute(text(f"DROP INDEX `{idx}` ON user_token"))
            except Exception:
                pass
        await db.execute(text("CREATE UNIQUE INDEX token_UNIQUE ON user_token (token)"))
        await db.execute(
            text("CREATE INDEX fk_user_token_user_idx ON user_token (user_id)")
        )
        await db.commit()
    print("user_token 表已对齐模型。")


if __name__ == "__main__":
    asyncio.run(main())
