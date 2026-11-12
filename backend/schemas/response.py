from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一接口响应：code + message + data。"""

    code: int = Field(..., description="业务状态码，200/201 为成功")
    message: str = Field(..., description="状态提示")
    data: T | None = None


def success(
    data: T | None = None,
    *,
    message: str = "操作成功",
    code: int = 200,
) -> dict:
    return {"code": code, "message": message, "data": data}


def fail_message(message: str, *, code: int = 400) -> str:
    """供 HTTPException detail 使用（由全局处理器转为统一 JSON）。"""
    return message
