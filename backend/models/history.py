from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, func

from config.db_conf import Base


class History(Base):
    """浏览历史表 history：用户与新闻关联。"""

    __tablename__ = "history"
    __table_args__ = (UniqueConstraint("user_id", "news_id", name="uq_history_user_news"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False, index=True)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
