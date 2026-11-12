"""用户令牌表 user_token：Bearer token 与过期时间。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.db_conf import Base


class UserToken(Base):
    """用户令牌表 user_token：登录态，支持过期。"""

    __tablename__ = "user_token"
    __table_args__ = (
        Index("token_UNIQUE", "token", unique=True),
        Index("fk_user_token_user_idx", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="令牌ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="用户ID",
    )
    token: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="令牌值"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="过期时间"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
