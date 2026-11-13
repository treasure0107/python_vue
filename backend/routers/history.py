"""浏览历史：添加、分页列表、删除单条、清空。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history as history_crud
from dependencies.auth import get_current_user
from models.users import User
from schemas.history import (
    HistoryAddRequest,
    HistoryClearData,
    HistoryListPageData,
    HistoryRecordOut,
)
from schemas.response import ApiResponse
from utils.response import success_response

router = APIRouter(prefix="/history", tags=["浏览历史"])


@router.post("/add", response_model=ApiResponse[HistoryRecordOut])
async def add_history(
    body: HistoryAddRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST /history/add — 添加或更新浏览时间（需登录）。"""
    data = await history_crud.add_history_checked(
        db, current_user.id, body.news_id
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="资讯不存在"
        )
    return success_response("添加成功", data)


@router.get("/list", response_model=ApiResponse[HistoryListPageData])
async def list_history(
    page: int = 1,
    pageSize: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """GET /history/list — 分页浏览历史（需登录）。"""
    data = await history_crud.list_history_page(
        db, current_user.id, page=page, page_size=pageSize
    )
    return success_response("获取浏览历史成功", data)


@router.delete("/{history_id}", response_model=ApiResponse[None])
async def delete_history(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """DELETE /history/{history_id} — 删除单条记录。"""
    ok = await history_crud.remove_history_by_id(
        db, current_user.id, history_id
    )
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在"
        )
    return success_response("删除成功", None)


@router.delete("", response_model=ApiResponse[HistoryClearData])
async def clear_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """DELETE /history — 清空浏览历史。"""
    removed = await history_crud.clear_user_history(db, current_user.id)
    return success_response("已清空浏览历史", HistoryClearData(removed=removed))
