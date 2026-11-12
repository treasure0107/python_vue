"""密码哈希与校验（bcrypt，兼容既有 passlib 生成的哈希）。"""

import bcrypt


def hash_password(plain_password: str) -> str:
    """注册/改密时对明文密码做 bcrypt 哈希。"""
    salt = bcrypt.gensalt()
    digest = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return digest.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文与库中 hashed_password 是否匹配。"""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
