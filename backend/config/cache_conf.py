"""Redis 连接与缓存 Key / TTL（参见 1-6 缓存设计）。"""

import os

REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() in ("1", "true", "yes")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# 过期时间（秒）
TTL_NEWS_DETAIL = 60 * 60  # 1 小时
TTL_NEWS_LIST = 30 * 60  # 30 分钟
TTL_NEWS_CATEGORIES = 2 * 60 * 60  # 2 小时
TTL_HISTORY_LIST = 60 * 60  # 1 小时

# 批量清理用模式
PATTERN_NEWS_LIST = "news:list:*"


def news_detail_key(news_id: int) -> str:
    return f"news:detail:{news_id}"


def news_list_key(category_id: int | str, page: int, size: int) -> str:
    return f"news:list:{category_id}:{page}:{size}"


def news_categories_key() -> str:
    return "news:categories"


def history_list_key(user_id: int) -> str:
    return f"history:list:{user_id}"
