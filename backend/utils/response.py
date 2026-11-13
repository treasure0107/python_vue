"""
统一 API 响应封装（工厂模式）。

成功：{"code": 200, "message": "...", "data": ...}
失败：由 exception_handlers 使用同一 envelope，data 为 null。

data 支持 Pydantic、ORM、dict、list 等，经 jsonable_encoder 序列化。
路由推荐：response_model=ApiResponse[T] + return success(data, message=...)
"""

from __future__ import annotations

from typing import Any, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponseFactory:
    """构造 code / message / data 统一外壳。"""

    @staticmethod
    def encode_data(data: Any) -> Any:
        """将 Pydantic、ORM、datetime 等转为可 JSON 序列化的结构。"""
        if data is None:
            return None
        if isinstance(data, BaseModel):
            return data.model_dump(mode="json")
        return jsonable_encoder(data)

    @staticmethod
    def envelope(
        *,
        code: int,
        message: str,
        data: Any = None,
    ) -> dict[str, Any]:
        return {
            "code": code,
            "message": message,
            "data": ApiResponseFactory.encode_data(data),
        }

    @staticmethod
    def success(
        data: T | None = None,
        *,
        message: str = "操作成功",
        code: int = 200,
    ) -> dict[str, Any]:
        return ApiResponseFactory.envelope(code=code, message=message, data=data)

    @staticmethod
    def success_response(
        data: Any = None,
        *,
        message: str = "success",
        code: int = 200,
        status_code: int | None = None,
    ) -> JSONResponse:
        """
        直接返回 JSONResponse（与课件 success_response 一致）。
        未声明 response_model 的接口可使用。
        """
        content = ApiResponseFactory.success(data, message=message, code=code)
        return JSONResponse(
            status_code=status_code if status_code is not None else code,
            content=content,
        )

    @staticmethod
    def error_response(
        message: str,
        *,
        code: int,
        status_code: int | None = None,
        data: Any = None,
    ) -> JSONResponse:
        """失败响应：生产环境 data 多为 null；DEBUG 时可附带排查信息。"""
        http_status = status_code if status_code is not None else code
        return JSONResponse(
            status_code=http_status,
            content=ApiResponseFactory.envelope(code=code, message=message, data=data),
        )


# 路由层便捷函数（与课件命名一致）
def success(
    data: T | None = None,
    *,
    message: str = "操作成功",
    code: int = 200,
) -> dict[str, Any]:
    return ApiResponseFactory.success(data, message=message, code=code)


def success_response(
    message: str = "success",
    data: Any = None,
    *,
    code: int = 200,
    status_code: int | None = None,
) -> JSONResponse:
    return ApiResponseFactory.success_response(
        data, message=message, code=code, status_code=status_code
    )
