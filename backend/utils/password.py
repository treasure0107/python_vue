"""
passlib 密码加密模块（注册 / 登录 / 改密统一调用）

1. 安装：pip install "passlib[bcrypt]==1.7.4"
2. 创建 CryptContext，统一管理 bcrypt 策略
3. 加密：get_password_hash；校验：verify_password
"""

from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """注册、修改密码：明文 → 可入库的哈希值。"""
    try:
        return pwd_context.hash(password)
    except (ValueError, RuntimeError) as exc:
        raise RuntimeError(
            "密码加密失败：请安装 passlib[bcrypt]==1.7.4 且 bcrypt>=3.2,<4.0"
        ) from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """登录、改密验旧密码：明文与库中哈希比对。"""
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, TypeError):
        return False


# 历史别名，与 get_password_hash 等价
hash_password = get_password_hash
