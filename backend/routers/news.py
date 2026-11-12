"""资讯 HTTP 路由：分类、分页列表、详情、增删改。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news as news_crud
from crud import news_category as category_crud
from schemas.news import NewsCreate, NewsDetailData, NewsListPageData, NewsOut, NewsUpdate
from schemas.news_category import NewsCategoryOut
from schemas.response import ApiResponse, success

router = APIRouter(prefix="/news", tags=["资讯"])


@router.get("/categories", response_model=ApiResponse[list[NewsCategoryOut]])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """GET /news/categories — 全部分类。"""
    data = await news_crud.list_categories_cached(db)
    return success(data, message="获取新闻分类成功")


@router.get("/list", response_model=ApiResponse[NewsListPageData])
async def list_news_page(
    categoryId: int,
    page: int = 1,
    pageSize: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """GET /news/list — 按分类 id 分页（下拉加载更多）。"""
    if page < 1:
        page = 1
    if pageSize < 1:
        pageSize = 10
    if pageSize > 100:
        pageSize = 100
    if not await category_crud.get_category_by_id(db, categoryId):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    data = await news_crud.list_news_page(
        db, categoryId, page=page, page_size=pageSize
    )
    return success(data, message="success")


@router.get("", response_model=ApiResponse[list[NewsOut]])
async def list_news(
    skip: int = 0,
    limit: int = 20,
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """GET /news — 旧版 skip/limit 列表。"""
    data = await news_crud.list_news_cached(
        db, skip=skip, limit=limit, category=category
    )
    return success(data, message="获取新闻列表成功")


@router.get("/{news_id}", response_model=ApiResponse[NewsDetailData])
async def get_news(news_id: int, db: AsyncSession = Depends(get_db)):
    """GET /news/{id} — 正文、浏览量+1、相关推荐。"""
    data = await news_crud.get_news_detail_with_related(db, news_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资讯不存在")
    return success(data, message="success")


@router.post("", response_model=ApiResponse[NewsOut], status_code=status.HTTP_201_CREATED)
async def create_news(news_in: NewsCreate, db: AsyncSession = Depends(get_db)):
    """POST /news — 创建资讯。"""
    data = await news_crud.create_news_item(db, news_in)
    return success(data, message="创建资讯成功", code=201)


@router.put("/{news_id}", response_model=ApiResponse[NewsOut])
async def update_news(
    news_id: int, news_in: NewsUpdate, db: AsyncSession = Depends(get_db)
):
    """PUT /news/{id} — 更新资讯。"""
    data = await news_crud.update_news_item(db, news_id, news_in)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资讯不存在")
    return success(data, message="更新资讯成功")


@router.delete("/{news_id}", response_model=ApiResponse[None])
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
    """DELETE /news/{id} — 删除资讯。"""
    ok = await news_crud.delete_news_item(db, news_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资讯不存在")
    return success(None, message="删除资讯成功")
