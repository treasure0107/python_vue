import logging

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def _as_message(detail) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict):
                loc = ".".join(str(x) for x in item.get("loc", []))
                msg = item.get("msg", "")
                parts.append(f"{loc}: {msg}" if loc else msg)
            else:
                parts.append(str(item))
        return "；".join(parts) or "请求参数错误"
    return str(detail)


async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    code = exc.status_code if exc.status_code >= 400 else 400
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": code,
            "message": _as_message(exc.detail),
            "data": None,
        },
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": _as_message(exc.errors()),
            "data": None,
        },
    )


async def unhandled_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """未捕获异常：记录日志并返回统一 JSON，避免 Swagger 只显示纯文本堆栈。"""
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误，请查看后端日志",
            "data": None,
        },
    )
