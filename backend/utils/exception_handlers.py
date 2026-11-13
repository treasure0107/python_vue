"""
全局异常处理器：业务 / 参数 / 数据库 / 系统层统一返回 { code, message, data }。

用法（main.py）：
    register_exception_handlers(app)
"""

from __future__ import annotations

import logging
import traceback
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

from config.db_conf import settings
from utils.response import ApiResponseFactory

logger = logging.getLogger(__name__)

# 与 config.settings.debug 同步；教学环境可开，生产应关
DEBUG_MODE = settings.debug

ExceptionHandler = Callable[[Request, Exception], JSONResponse]


def _as_message(detail: Any) -> str:
    """将 HTTPException.detail 或校验错误列表转为前端可读字符串。"""
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


def _debug_payload(
    request: Request,
    exc: Exception,
    *,
    error_type: str | None = None,
    include_traceback: bool = False,
) -> dict[str, Any] | None:
    """DEBUG 模式下在 data 中附带错误类型、路径等，便于联调。"""
    if not DEBUG_MODE:
        return None
    payload: dict[str, Any] = {
        "error_type": error_type or type(exc).__name__,
        "error_detail": str(exc),
        "path": str(request.url),
    }
    if include_traceback:
        payload["traceback"] = traceback.format_exc()
    return payload


def _integrity_message(error_msg: str) -> str:
    """根据 MySQL 原始错误信息映射用户提示。"""
    lower = error_msg.lower()
    if "duplicate entry" in lower or "unique" in lower:
        if "username" in lower or "uq_user_username" in lower:
            return "用户名已存在"
        if "email" in lower or "uq_user_email" in lower:
            return "邮箱已注册"
        if "token" in lower:
            return "令牌冲突，请重新登录"
        if "favorite" in lower or "user_news_unique" in lower or "uq_favorite_user_news" in lower:
            return "该资讯已收藏，请勿重复收藏"
        return "数据已存在，请勿重复提交"
    if "foreign key" in lower:
        return "关联数据不存在"
    return "数据约束冲突，请检查输入"


async def http_exception_handler(
    _request: Request, exc: HTTPException
) -> JSONResponse:
    """HTTPException：业务层主动抛出，data 一般为 null。"""
    code = exc.status_code if exc.status_code >= 400 else 400
    return ApiResponseFactory.error_response(
        _as_message(exc.detail),
        code=code,
        status_code=exc.status_code,
        data=None,
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """请求参数校验失败（Pydantic / FastAPI）。"""
    return ApiResponseFactory.error_response(
        _as_message(exc.errors()),
        code=422,
        status_code=422,
        data=_debug_payload(_request, exc, error_type="RequestValidationError"),
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """数据库完整性约束：唯一键、外键等。"""
    error_msg = str(getattr(exc, "orig", exc))
    message = _integrity_message(error_msg)
    logger.warning("IntegrityError: %s", error_msg)
    return ApiResponseFactory.error_response(
        message,
        code=400,
        status_code=status.HTTP_400_BAD_REQUEST,
        data=_debug_payload(request, exc, error_type="IntegrityError"),
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """其它 SQLAlchemy / 连接 / 事务错误（IntegrityError 由专属处理器处理）。"""
    logger.exception("SQLAlchemyError: %s", exc)
    return ApiResponseFactory.error_response(
        "数据库操作失败，请稍后重试",
        code=500,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=_debug_payload(
            request, exc, error_type="SQLAlchemyError", include_traceback=True
        ),
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """兜底：未分类的系统异常。"""
    logger.exception("Unhandled error: %s", exc)
    return ApiResponseFactory.error_response(
        "服务器内部错误",
        code=500,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=_debug_payload(
            request, exc, include_traceback=True
        ),
    )


# 注册顺序：子类异常在前，Exception 兜底在最后
_EXCEPTION_HANDLERS: list[tuple[type[Exception], ExceptionHandler]] = [
    (HTTPException, http_exception_handler),
    (RequestValidationError, validation_exception_handler),
    (IntegrityError, integrity_error_handler),
    (SQLAlchemyError, sqlalchemy_error_handler),
    (Exception, general_exception_handler),
]


def register_exception_handlers(app: FastAPI) -> None:
    """全局注册异常处理器（课件：app.add_exception_handler）。"""
    for exc_cls, handler in _EXCEPTION_HANDLERS:
        app.add_exception_handler(exc_cls, handler)


# 兼容旧导入
unhandled_exception_handler = general_exception_handler
