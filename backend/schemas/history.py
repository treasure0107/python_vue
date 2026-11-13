"""浏览历史请求/响应模型。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HistoryAddRequest(BaseModel):
    """POST /history/add 请求体。"""

    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(..., alias="newsId", ge=1)


class HistoryRecordOut(BaseModel):
    """添加/更新浏览记录后的 data（与产品稿字段一致）。"""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    user_id: int = Field(serialization_alias="userId")
    news_id: int = Field(serialization_alias="newsId")
    viewed_at: datetime = Field(serialization_alias="viewTime")


class HistoryListItem(BaseModel):
    """浏览历史列表项（联表新闻摘要）。"""

    id: int
    news_id: int
    title: str
    cover_url: str | None = None
    source: str | None = None
    published_at: datetime | None = None
    viewed_at: datetime


class HistoryListPageData(BaseModel):
    """分页浏览历史。"""

    list: list[HistoryListItem]
    total: int
    hasMore: bool


class HistoryClearData(BaseModel):
    """清空浏览历史结果。"""

    removed: int
