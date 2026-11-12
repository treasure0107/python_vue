from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NewsCategoryOut(BaseModel):
    """分类接口 data 单项结构。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=32)
    sort_order: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
