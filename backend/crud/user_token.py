"""登录令牌 user_token：注册/登录成功后签发 Bearer token。"""

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_token import UserToken
from models.users import User

# 令牌有效期（天）
TOKEN_EXPIRE_DAYS = 7


def _utcnow() -> datetime:
    """当前 UTC 时间（带时区）。"""
    return datetime.now(timezone.utc)


async def revoke_tokens_for_user(db: AsyncSession, user_id: int) -> None:
    """删除某用户已有令牌，避免 user_token 表同一 user_id 多条记录。"""
    await db.execute(delete(UserToken).where(UserToken.user_id == user_id))


async def create_user_token(
    db: AsyncSession,
    user_id: int,
    *,
    days: int = TOKEN_EXPIRE_DAYS,
) -> UserToken:
    """
    签发新令牌（UUID），有效期默认 7 天。
    同一用户先撤销旧令牌再入库，保证每名用户仅一条记录。
    """
    await revoke_tokens_for_user(db, user_id)
    row = UserToken(
        user_id=user_id,
        token=str(uuid.uuid4()),
        expires_at=_utcnow() + timedelta(days=days),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def get_valid_token(db: AsyncSession, token: str) -> UserToken | None:
    """校验 token 是否存在且未过期，供 get_current_user 使用。"""
    pair = await get_valid_token_with_user(db, token)
    return pair[0] if pair else None


async def get_valid_token_with_user(
    db: AsyncSession, token: str
) -> tuple[UserToken, User] | None:
    """一次查询返回有效 token 与对应用户（减少鉴权往返）。"""
    result = await db.execute(
        select(UserToken, User)
        .join(User, User.id == UserToken.user_id)
        .where(UserToken.token == token)
    )
    row = result.one_or_none()
    if row is None:
        return None
    token_row, user = row
    expires = token_row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < _utcnow():
        return None
    if not user.is_active:
        return None
    return token_row, user
