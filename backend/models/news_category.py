from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from config.db_conf import Base


class NewsCategory(Base):
    """新闻分类表 news_category。"""

    __tablename__ = "news_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), unique=True, nullable=False, index=True)
    sort_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
