"""
统一 API 响应封装（工厂模式）。

成功：{"code": 200, "message": "...", "data": ...}
失败：exception_handlers 使用 ApiResponseFactory.error_response

路由层请统一：return success_response(message="...", data=业务 schemas 实例)
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
            return data.model_dump(mode="json", by_alias=True)
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
        """课件标准：JSONResponse + jsonable_encoder 整包序列化。"""
        content = ApiResponseFactory.envelope(code=code, message=message, data=data)
        http_status = status_code
        if http_status is None:
            http_status = code if code in (200, 201) else 200
        return JSONResponse(
            status_code=http_status,
            content=jsonable_encoder(content),
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
        content = ApiResponseFactory.envelope(code=code, message=message, data=data)
        return JSONResponse(
            status_code=http_status,
            content=jsonable_encoder(content),
        )


def success_response(
    message: str = "success",
    data: Any = None,
    *,
    code: int = 200,
    status_code: int | None = None,
) -> JSONResponse:
    """
    路由统一成功返回（与课件签名一致：message 在前）。
    示例：return success_response("注册成功", data)
    """
    return ApiResponseFactory.success_response(
        data, message=message, code=code, status_code=status_code
    )


def success(
    data: T | None = None,
    *,
    message: str = "操作成功",
    code: int = 200,
) -> JSONResponse:
    """兼容旧写法 success(data, message=...) → 内部转 success_response。"""
    return success_response(message=message, data=data, code=code)
