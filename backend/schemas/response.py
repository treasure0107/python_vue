"""统一响应外壳类型（OpenAPI response_model）；构造见 utils.response.success_response。"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一接口响应：code + message + data。"""

    code: int = Field(..., description="业务状态码，200/201 为成功")
    message: str = Field(..., description="状态提示")
    data: T | None = None


class RootMeta(BaseModel):
    """GET / 根路径 data 结构。"""

    title: str
    docs: str
    api_prefix: str = "/api"


def fail_message(message: str, *, code: int = 400) -> str:
    """供 HTTPException detail 使用（由全局处理器转为统一 JSON）。"""
    return message
