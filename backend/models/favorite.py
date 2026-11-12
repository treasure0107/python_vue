from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, func

from config.db_conf import Base


class Favorite(Base):
    """收藏表 favorite：用户与新闻关联。"""

    __tablename__ = "favorite"
    __table_args__ = (UniqueConstraint("user_id", "news_id", name="uq_favorite_user_news"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
