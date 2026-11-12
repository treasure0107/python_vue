"""依赖注入：从请求头 Authorization: Bearer <token> 解析当前用户。"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import user_token as token_crud
from crud import users as user_crud
from models.users import User

# Bearer 持有者令牌（与前端 Authorization: Bearer <token> 对应）
_bearer = HTTPBearer(auto_error=False, scheme_name="Bearer")

_UNAUTHORIZED_HEADERS = {"WWW-Authenticate": "Bearer"}


def _unauthorized(detail: str) -> HTTPException:
    """401 且带 WWW-Authenticate: Bearer（HTTP 标准）。"""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers=_UNAUTHORIZED_HEADERS,
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    校验流程：
    1. 读取 Header Authorization
    2. scheme 须为 Bearer
    3. 用 token 字符串查 user_token 表并校验有效期
    4. 返回对应用户
    """
    if credentials is None:
        raise _unauthorized("未登录或令牌缺失，请在请求头携带 Authorization: Bearer <token>")
    if credentials.scheme.lower() != "bearer":
        raise _unauthorized("Authorization 须为 Bearer 类型")

    token_row = await token_crud.get_valid_token(db, credentials.credentials)
    if token_row is None:
        raise _unauthorized("令牌无效或已过期")

    user = await user_crud.get_user(db, token_row.user_id)
    if user is None or not user.is_active:
        raise _unauthorized("用户不存在或已禁用")
    return user
