from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from config.db_conf import Base


class News(Base):
    """新闻表 news：标题、内容、作者、浏览量等。"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False, index=True)
    summary = Column(String(512), nullable=True)
    content = Column(Text, nullable=False)
    category_id = Column(
        Integer, ForeignKey("news_category.id"), nullable=False, index=True
    )
    cover_url = Column(String(512), nullable=True)
    source = Column(String(64), nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    view_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    category = relationship("NewsCategory", backref="news_list")
    author = relationship("User", backref="news_list")
