from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
    func,
)

from config.db_conf import Base


class Favorite(Base):
    """收藏表 favorite：用户与新闻关联；同一用户对同一新闻仅一条收藏。"""

    __tablename__ = "favorite"
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
