"""认证请求/响应模型（注册 LoginRequest / RegisterRequest / AuthResponse）。"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from schemas.users import UserOut


class LoginRequest(BaseModel):
    """POST /auth/login 请求体。"""
    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    """POST /auth/register 请求体（密码长度由 Field 校验）。"""

    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    nickname: str | None = Field(default=None, max_length=64)
    email: EmailStr | None = None


class AuthResponse(BaseModel):
    """注册/登录成功后的 data 结构。"""

    token: str
    expires_at: datetime
    user: UserOut
