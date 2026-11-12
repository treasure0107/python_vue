"""资讯 Redis 缓存读写（供 crud/news 业务方法调用）。"""

from config import cache_conf
from schemas.news import NewsListPageData, NewsOut
from schemas.news_category import NewsCategoryOut
from utils.cache_invalidate import invalidate_news_on_write
from utils.redis_cache import cache_get, cache_set


def category_cache_key() -> str:
    return cache_conf.news_categories_key()


def list_cache_key(category: str | None, skip: int, limit: int) -> str:
    cid = category if category else "all"
    page = skip // limit + 1 if limit > 0 else 1
    return cache_conf.news_list_key(cid, page, limit)


def detail_cache_key(news_id: int) -> str:
    return cache_conf.news_detail_key(news_id)


def get_cached_categories() -> list | None:
    return cache_get(category_cache_key())


def set_cached_categories(items: list[NewsCategoryOut]) -> None:
    payload = [c.model_dump(mode="json") for c in items]
    cache_set(category_cache_key(), payload, cache_conf.TTL_NEWS_CATEGORIES)


def get_cached_news_list(category: str | None, skip: int, limit: int) -> list | None:
    return cache_get(list_cache_key(category, skip, limit))


def set_cached_news_list(
    category: str | None, skip: int, limit: int, items: list[NewsOut]
) -> None:
    payload = [n.model_dump(mode="json") for n in items]
    cache_set(
        list_cache_key(category, skip, limit),
        payload,
        cache_conf.TTL_NEWS_LIST,
    )


def get_cached_news_detail(news_id: int) -> dict | None:
    return cache_get(detail_cache_key(news_id))


def set_cached_news_detail(news_id: int, item: NewsOut) -> None:
    cache_set(
        detail_cache_key(news_id),
        item.model_dump(mode="json"),
        cache_conf.TTL_NEWS_DETAIL,
    )


def page_cache_key(category_id: int, page: int, page_size: int) -> str:
    return cache_conf.news_list_key(category_id, page, page_size)


def get_cached_news_page(
    category_id: int, page: int, page_size: int
) -> dict | None:
    raw = cache_get(page_cache_key(category_id, page, page_size))
    if raw and isinstance(raw, dict) and "list" in raw:
        return raw
    return None


def set_cached_news_page(
    category_id: int, page: int, page_size: int, data: NewsListPageData
) -> None:
    cache_set(
        page_cache_key(category_id, page, page_size),
        data.model_dump(mode="json"),
        cache_conf.TTL_NEWS_LIST,
    )


def invalidate_after_news_write(news_id: int | None = None) -> None:
    invalidate_news_on_write(news_id)
