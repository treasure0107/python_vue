from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class NewsBase(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    summary: str | None = Field(default=None, max_length=512)
    content: str = Field(min_length=1)
    cover_url: str | None = Field(default=None, max_length=512)
    source: str | None = Field(default=None, max_length=64)
    author_id: int | None = None


class NewsCreate(NewsBase):
    category_id: int | None = None
    category: str | None = Field(default=None, max_length=32)

    @model_validator(mode="after")
    def category_required(self):
        if self.category_id is None and not self.category:
            self.category = "推荐"
        return self


class NewsUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=256)
    summary: str | None = Field(default=None, max_length=512)
    content: str | None = Field(default=None, min_length=1)
    category_id: int | None = None
    category: str | None = Field(default=None, max_length=32)
    cover_url: str | None = Field(default=None, max_length=512)
    source: str | None = Field(default=None, max_length=64)
    author_id: int | None = None


class NewsOut(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    category: str = "推荐"
    view_count: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NewsListItem(BaseModel):
    """列表项：不含正文，减轻流量。"""

    id: int
    category_id: int
    category: str | None = None
    title: str
    description: str | None = None
    cover_url: str | None = None
    source: str | None = None
    view_count: int = 0
    created_at: datetime | None = None


class NewsListPageData(BaseModel):
    list: list[NewsListItem]
    total: int
    hasMore: bool


class NewsRelatedItem(BaseModel):
    """详情页「相关新闻」列表项。"""

    id: int
    title: str
    cover_url: str | None = None
    description: str | None = None
    source: str | None = None
    view_count: int = 0


class NewsDetailData(BaseModel):
    """新闻详情（含浏览量与相关推荐）。"""

    id: int
    title: str
    content: str
    views: int
    summary: str | None = None
    cover_url: str | None = None
    source: str | None = None
    category: str | None = None
    category_id: int | None = None
    created_at: datetime | None = None
    relatedNews: list[NewsRelatedItem] = Field(default_factory=list)
