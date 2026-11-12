"""注册、登录并签发令牌。"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_token as token_crud
from crud import users as user_crud
from schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from schemas.users import UserCreate, UserOut
from utils.security import verify_password


async def register_user(db: AsyncSession, body: RegisterRequest) -> AuthResponse:
    """注册业务：用户名/邮箱查重 → create_user → create_user_token → AuthResponse。"""
    if await user_crud.get_user_by_username(db, body.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    if body.email and await user_crud.get_user_by_email(db, str(body.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已注册")

    user_in = UserCreate(
        username=body.username,
        password=body.password,
        nickname=body.nickname,
        email=body.email,
    )
    user = await user_crud.create_user(db, user_in)
    token_row = await token_crud.create_user_token(db, user.id)
    return AuthResponse(
        token=token_row.token,
        expires_at=token_row.expires_at,
        user=UserOut.model_validate(user),
    )


async def login_user(db: AsyncSession, body: LoginRequest) -> AuthResponse:
    """校验用户名密码，返回 token 与用户摘要。"""
    user = await user_crud.get_user_by_username(db, body.username)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已禁用",
        )
    token_row = await token_crud.create_user_token(db, user.id)
    return AuthResponse(
        token=token_row.token,
        expires_at=token_row.expires_at,
        user=UserOut.model_validate(user),
    )
