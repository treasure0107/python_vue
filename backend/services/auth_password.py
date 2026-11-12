"""
认证密码服务：封装「加密入库 / 登录校验 / 改密校验」。

用法示例::

    from services.auth_password import AuthPasswordService

    stored = AuthPasswordService.hash_for_register(plain)
    ok = AuthPasswordService.verify_for_login(plain, user.hashed_password)
    AuthPasswordService.ensure_old_password_valid(old, user.hashed_password)
"""

from fastapi import HTTPException, status

from utils.password import get_password_hash, verify_password


class AuthPasswordService:
    """passlib 之上的薄封装，供注册、登录、修改密码调用。"""

    @staticmethod
    def hash_for_register(plain_password: str) -> str:
        """注册或重置密码：返回写入 user.hashed_password 的值。"""
        return get_password_hash(plain_password)

    @staticmethod
    def hash_for_update(plain_password: str) -> str:
        """修改密码时设置新密码（与注册相同算法）。"""
        return get_password_hash(plain_password)

    @staticmethod
    def verify_for_login(plain_password: str, hashed_password: str) -> bool:
        """登录：校验用户名对应密码是否正确。"""
        return verify_password(plain_password, hashed_password)

    @staticmethod
    def ensure_old_password_valid(plain_password: str, hashed_password: str) -> None:
        """修改密码：旧密码不正确时抛出 400。"""
        if not verify_password(plain_password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="原密码不正确",
            )
