"""用户表 CRUD：注册入库、查询、资料与密码（注册流程依赖 create_user / get_user_by_*）。"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from models.users import User
from schemas.users import (
    ChangePasswordRequest,
    ProfileUpdateRequest,
    UserCreate,
    UserOut,
    UserProfileOut,
    UserUpdate,
)
from services.auth_password import AuthPasswordService

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"
DEFAULT_ADMIN_BIO = "这是一个测试账号"
DEFAULT_ADMIN_AVATAR = "https://picsum.photos/seed/toutiao-cat/200/200"
DEFAULT_NEW_USER_BIO = "这个人很懒，什么都没留下"
DEFAULT_NEW_USER_AVATAR = "https://picsum.photos/seed/register-avatar/200/200"


def format_account_id(user_id: int) -> str:
    """对外展示的账号编码，如 heima-00001。"""
    return f"heima-{user_id:05x}"


def user_to_register_info(user: User):
    """注册响应 userInfo：id、用户名、简介、头像。"""
    from schemas.auth import RegisterUserInfo

    return RegisterUserInfo(
        id=user.id,
        username=user.username,
        bio=user.bio or DEFAULT_NEW_USER_BIO,
        avatar=user.avatar or DEFAULT_NEW_USER_AVATAR,
    )


def user_to_out(user: User) -> UserOut:
    """ORM → 列表/详情响应（避免空邮箱等脏数据触发 500）。"""
    return UserOut.model_validate(user)


def user_to_profile_out(user: User) -> UserProfileOut:
    """ORM 用户 → 个人信息 API 响应。"""
    payload = UserOut.model_validate(user).model_dump()
    payload["account_id"] = format_account_id(user.id)
    return UserProfileOut(**payload)


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """按主键查询用户。"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """按用户名查询（注册前查重、登录）。"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """按邮箱查询（注册可选邮箱查重）。"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    """用户列表分页（管理接口）。"""
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """注册核心：明文密码 bcrypt 哈希后写入 user 表。"""
    try:
        hashed_password = AuthPasswordService.hash_for_register(user_in.password)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    db_user = User(
        username=user_in.username,
        email=str(user_in.email) if user_in.email else None,
        nickname=(user_in.nickname or None) or user_in.username,
        avatar=user_in.avatar or DEFAULT_NEW_USER_AVATAR,
        bio=user_in.bio or DEFAULT_NEW_USER_BIO,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在",
        ) from exc
    await db.refresh(db_user)
    return db_user


async def ensure_default_admin(db: AsyncSession) -> None:
    """不存在 admin 时创建默认账号，初始密码 123456。"""
    existing = await get_user_by_username(db, DEFAULT_ADMIN_USERNAME)
    if existing:
        changed = False
        if not existing.bio:
            existing.bio = DEFAULT_ADMIN_BIO
            changed = True
        if not existing.avatar:
            existing.avatar = DEFAULT_ADMIN_AVATAR
            changed = True
        if changed:
            await db.commit()
        return
    admin_in = UserCreate(
        username=DEFAULT_ADMIN_USERNAME,
        password=DEFAULT_ADMIN_PASSWORD,
        nickname="管理员",
        email="admin@example.com",
        bio=DEFAULT_ADMIN_BIO,
        avatar=DEFAULT_ADMIN_AVATAR,
    )
    await create_user(db, admin_in)


async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    """通用更新；若含 password 字段则自动哈希为 hashed_password。"""
    data = user_in.model_dump(exclude_unset=True)
    if "password" in data:
        data["hashed_password"] = AuthPasswordService.hash_for_update(data.pop("password"))
    if "email" in data and data["email"] is not None:
        data["email"] = str(data["email"])
    for field, value in data.items():
        setattr(db_user, field, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, db_user: User) -> None:
    """删除用户行。"""
    await db.delete(db_user)
    await db.commit()


async def update_profile(
    db: AsyncSession, db_user: User, body: ProfileUpdateRequest
) -> UserProfileOut:
    """更新当前用户昵称、头像、个人简介。"""
    data = body.model_dump(exclude_unset=True)
    user_in = UserUpdate(**data)
    updated = await update_user(db, db_user, user_in)
    return user_to_profile_out(updated)


async def change_password(
    db: AsyncSession, db_user: User, body: ChangePasswordRequest
) -> None:
    """校验旧密码后更新为新密码。"""
    AuthPasswordService.ensure_old_password_valid(
        body.old_password, db_user.hashed_password
    )
    if body.old_password == body.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码不能与旧密码相同",
        )
    await update_user(db, db_user, UserUpdate(password=body.new_password))
