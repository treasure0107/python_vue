"""用户历史记录缓存（读写侧调用，写库后需 invalidate_user_history）。"""

from config import cache_conf
from utils.cache_invalidate import invalidate_user_history
from utils.redis_cache import cache_get, cache_set

__all__ = [
    "get_cached_history",
    "set_cached_history",
    "invalidate_user_history",
]


def get_cached_history(user_id: int) -> list | None:
    return cache_get(cache_conf.history_list_key(user_id))


def set_cached_history(user_id: int, items: list) -> None:
    cache_set(
        cache_conf.history_list_key(user_id),
        items,
        cache_conf.TTL_HISTORY_LIST,
    )
