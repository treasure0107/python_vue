from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import users as user_crud
from schemas.response import ApiResponse, success
from schemas.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("", response_model=ApiResponse[list[UserOut]])
async def list_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await user_crud.get_users(db, skip=skip, limit=limit)
    return success(
        [user_crud.user_to_out(u) for u in users],
        message="获取用户列表成功",
    )


@router.get("/{user_id}", response_model=ApiResponse[UserOut])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return success(user_crud.user_to_out(db_user), message="获取用户成功")


@router.post("", response_model=ApiResponse[UserOut])
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    if await user_crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    if user_in.email and await user_crud.get_user_by_email(db, str(user_in.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已注册")
    user = await user_crud.create_user(db, user_in)
    return success(user_crud.user_to_out(user), message="创建用户成功", code=200)


@router.put("/{user_id}", response_model=ApiResponse[UserOut])
async def update_user(
    user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)
):
    db_user = await user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    updated = await user_crud.update_user(db, db_user, user_in)
    return success(user_crud.user_to_out(updated), message="更新用户成功")


@router.delete("/{user_id}", response_model=ApiResponse[None])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    await user_crud.delete_user(db, db_user)
    return success(None, message="删除用户成功")
