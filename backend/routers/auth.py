"""认证与用户资料：注册、登录、个人信息、修改密码。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import auth as auth_crud
from crud import users as user_crud
from dependencies.auth import get_current_user
from models.users import User
from schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponseData,
)
from schemas.response import ApiResponse, success
from schemas.users import (
    ChangePasswordRequest,
    ProfileUpdateRequest,
    UserProfileOut,
)

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post(
    "/register",
    response_model=ApiResponse[RegisterResponseData],
    status_code=200,
)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """POST /auth/register — 查重、入库、签发令牌，返回 token 与 userInfo。"""
    data = await auth_crud.register_user(db, body)
    return success(data, message="注册成功", code=200)


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """POST /auth/login — 登录。"""
    data = await auth_crud.login_user(db, body)
    return success(data, message="登录成功")


@router.get("/me", response_model=ApiResponse[UserProfileOut])
async def me(current_user: User = Depends(get_current_user)):
    """GET /auth/me — 当前用户个人信息（含 account_id、bio）。"""
    return success(user_crud.user_to_profile_out(current_user), message="success")


@router.patch("/profile", response_model=ApiResponse[UserProfileOut])
async def update_profile(
    body: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """PATCH /auth/profile — 更新昵称、头像、个人简介。"""
    data = await user_crud.update_profile(db, current_user, body)
    return success(data, message="资料已更新")


@router.post("/password", response_model=ApiResponse[None])
async def change_password(
    body: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST /auth/password — 修改登录密码。"""
    await user_crud.change_password(db, current_user, body)
    return success(None, message="密码已修改")
