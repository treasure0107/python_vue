"""收藏：列表、切换、单条删除、清空。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favorite as favorite_crud
from dependencies.auth import get_current_user
from models.users import User
from schemas.favorite import FavoriteClearData, FavoriteListItem, FavoriteToggleData
from schemas.response import ApiResponse
from utils.response import success_response

router = APIRouter(prefix="/favorites", tags=["收藏"])


@router.get("", response_model=ApiResponse[list[FavoriteListItem]])
async def list_favorites(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """GET /favorites — 我的收藏列表。"""
    if limit > 200:
        limit = 200
    data = await favorite_crud.list_user_favorites(
        db, current_user.id, skip=skip, limit=limit
    )
    return success_response("获取收藏成功", data)


@router.post("/{news_id}", response_model=ApiResponse[FavoriteToggleData])
async def toggle_favorite(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST /favorites/{news_id} — 切换收藏状态。"""
    payload = await favorite_crud.toggle_favorite_checked(
        db, current_user.id, news_id
    )
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资讯不存在")
    msg = "已收藏" if payload.favorited else "已取消收藏"
    return success_response(msg, payload)


@router.delete("/{news_id}", response_model=ApiResponse[None])
async def remove_one_favorite(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """DELETE /favorites/{news_id} — 取消单条收藏。"""
    await favorite_crud.remove_favorite(db, current_user.id, news_id)
    return success_response("已取消收藏", None)


@router.delete("", response_model=ApiResponse[FavoriteClearData])
async def clear_all_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """DELETE /favorites — 清空收藏。"""
    removed = await favorite_crud.clear_favorites(db, current_user.id)
    return success_response("已清空收藏", FavoriteClearData(removed=removed))
