"""收藏接口 data 模型。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FavoriteListItem(BaseModel):
    """我的收藏列表项。"""

    model_config = ConfigDict(from_attributes=True)

    news_id: int
    title: str
    cover_url: str | None = None
    source: str | None = None
    published_at: datetime | None = Field(default=None, description="新闻发布时间")
    favorited_at: datetime = Field(description="收藏时间")


class FavoriteToggleData(BaseModel):
    """切换收藏状态后的 data。"""

    news_id: int
    favorited: bool


class FavoriteClearData(BaseModel):
    """清空收藏结果。"""

    removed: int
