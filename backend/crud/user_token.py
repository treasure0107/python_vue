"""登录令牌 user_token：注册/登录成功后签发 Bearer token。"""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_token import UserToken


def _utcnow() -> datetime:
    """当前 UTC 时间（带时区）。"""
    return datetime.now(timezone.utc)


async def create_user_token(
    db: AsyncSession,
    user_id: int,
    *,
    days: int = 7,
) -> UserToken:
    """为新注册用户或登录用户创建 token，默认有效期 7 天。"""
    row = UserToken(
        user_id=user_id,
        token=secrets.token_urlsafe(48),
        expires_at=_utcnow() + timedelta(days=days),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def get_valid_token(db: AsyncSession, token: str) -> UserToken | None:
    """校验 token 是否存在且未过期，供 get_current_user 使用。"""
    result = await db.execute(select(UserToken).where(UserToken.token == token))
    row = result.scalar_one_or_none()
    if row is None:
        return None
    expires = row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < _utcnow():
        return None
    return row
