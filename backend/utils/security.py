"""
密码工具兼容入口。

推荐：
    from utils.password import get_password_hash, verify_password
或：
    from utils.security import hash_password, verify_password
"""

from utils.password import (
    get_password_hash,
    hash_password,
    pwd_context,
    verify_password,
)

__all__ = [
    "pwd_context",
    "get_password_hash",
    "hash_password",
    "verify_password",
]
