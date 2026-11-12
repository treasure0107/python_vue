from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from config.db_conf import Base


class UserToken(Base):
    """用户令牌表 user_token：登录态，支持过期。"""

    __tablename__ = "user_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(128), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
