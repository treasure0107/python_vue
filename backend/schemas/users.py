"""用户 Schema：注册用 UserCreate，注册/登录返回 UserOut。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """用户公开字段基类（不含密码）。"""
    username: str = Field(min_length=2, max_length=64)
    nickname: str | None = Field(default=None, max_length=64)
    avatar: str | None = Field(default=None, max_length=512)
    bio: str | None = Field(default=None, max_length=512)
    email: EmailStr | None = None


class UserCreate(UserBase):
    """注册入库 DTO，由 crud.users.create_user 消费。"""

    password: str = Field(min_length=6, max_length=128)


class UserUpdate(BaseModel):
    """后台或资料/改密时的部分更新。"""
    username: str | None = Field(default=None, min_length=2, max_length=64)
    nickname: str | None = Field(default=None, max_length=64)
    avatar: str | None = Field(default=None, max_length=512)
    bio: str | None = Field(default=None, max_length=512)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)
    is_active: bool | None = None


class ProfileUpdateRequest(BaseModel):
    """当前用户可修改的公开资料（不含用户名）。"""

    nickname: str | None = Field(default=None, max_length=64)
    avatar: str | None = Field(default=None, max_length=512)
    bio: str | None = Field(default=None, max_length=512)


class ChangePasswordRequest(BaseModel):
    """POST /auth/password 请求体。"""

    old_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    """注册/登录 AuthResponse.user 结构（不含 hashed_password）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserProfileOut(UserOut):
    """个人信息页：在 UserOut 基础上增加对外展示的 account_id。"""

    account_id: str
