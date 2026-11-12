from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from config.db_conf import Base


class User(Base):
    """用户表 user：用户名、加密密码、昵称、头像等。"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nickname = Column(String(64), nullable=True)
    avatar = Column(String(512), nullable=True)
    bio = Column(String(512), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
