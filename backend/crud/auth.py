"""注册、登录并签发令牌。"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_token as token_crud
from crud import users as user_crud
from schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponseData,
)
from schemas.users import UserCreate, UserOut
from services.auth_password import AuthPasswordService


async def register_user(
    db: AsyncSession, body: RegisterRequest
) -> RegisterResponseData:
    """
    注册业务流程（与产品流程图一致）：
    1. 按用户名查重
    2. 密码 bcrypt 加密并 create_user
    3. 生成访问令牌（UUID）写入 user_token
    4. 返回 token + userInfo
    """
    existing = await user_crud.get_user_by_username(db, body.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    if body.email and await user_crud.get_user_by_email(db, str(body.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已注册",
        )

    user_in = UserCreate(
        username=body.username,
        password=body.password,
        nickname=body.nickname or body.username,
        email=body.email,
    )
    user = await user_crud.create_user(db, user_in)
    token_row = await token_crud.create_user_token(db, user.id)
    return RegisterResponseData(
        token=token_row.token,
        userInfo=user_crud.user_to_register_info(user),
        expires_at=token_row.expires_at,
    )


async def login_user(db: AsyncSession, body: LoginRequest) -> AuthResponse:
    """校验用户名密码，返回 token 与用户摘要。"""
    user = await user_crud.get_user_by_username(db, body.username)
    if not user or not AuthPasswordService.verify_for_login(
        body.password, user.hashed_password
    ):
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
