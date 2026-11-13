"""认证请求/响应模型（注册 LoginRequest / RegisterRequest / AuthResponse）。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from schemas.users import UserOut


class LoginRequest(BaseModel):
    """POST /auth/login 请求体。"""
    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    """POST /auth/register 请求体：仅用户名与密码（其余由服务端默认）。"""

    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    nickname: str | None = Field(default=None, max_length=64)
    email: EmailStr | None = None

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_as_none(cls, value):
        if value is None or value == "":
            return None
        return value

    @model_validator(mode="before")
    @classmethod
    def blank_optional_strings(cls, data):
        if not isinstance(data, dict):
            return data
        if data.get("nickname") == "":
            data["nickname"] = None
        if data.get("email") == "":
            data["email"] = None
        return data


class RegisterUserInfo(BaseModel):
    """注册成功返回的用户摘要（与产品稿 userInfo 一致）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    bio: str | None = None
    avatar: str | None = None


class RegisterResponseData(BaseModel):
    """注册成功 data：访问令牌 + userInfo（对应课件 UserAuthResponse）。"""

    model_config = ConfigDict(populate_by_name=True)

    token: str
    userInfo: RegisterUserInfo
    expires_at: datetime | None = None


class AuthResponse(BaseModel):
    """登录成功后的 data 结构。"""

    model_config = ConfigDict(from_attributes=True)

    token: str
    expires_at: datetime
    user: UserOut
