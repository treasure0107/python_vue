"""写库后失效相关缓存（失效策略，非主动更新）。"""

from config import cache_conf
from utils.redis_cache import cache_delete, cache_delete_by_pattern


def invalidate_news_detail(news_id: int) -> None:
    cache_delete(cache_conf.news_detail_key(news_id))


def invalidate_news_list_all() -> None:
    cache_delete_by_pattern(cache_conf.PATTERN_NEWS_LIST)


def invalidate_news_categories() -> None:
    cache_delete(cache_conf.news_categories_key())


def invalidate_news_on_write(news_id: int | None = None) -> None:
    """资讯增删改后：详情 + 全部分页列表 + 分类导航。"""
    if news_id is not None:
        invalidate_news_detail(news_id)
    invalidate_news_list_all()
    invalidate_news_categories()


def invalidate_user_history(user_id: int) -> None:
    cache_delete(cache_conf.history_list_key(user_id))
