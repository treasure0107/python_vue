"""Redis 连接与缓存 Key / TTL（参见 1-6 缓存设计）。"""

import os
from pathlib import Path
from typing import Any

import redis


def _load_dotenv() -> None:
    """加载项目根 / backend 下 .env，供 REDIS_* 等 os.getenv 使用。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    backend_dir = Path(__file__).resolve().parents[1]
    root = backend_dir.parent
    load_dotenv(root / ".env")
    load_dotenv(backend_dir / ".env")


_load_dotenv()

REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() in ("1", "true", "yes")
# Redis 服务器主机地址
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# Redis 端口号
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
# Redis 数据库编号 0~15
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
# phpStudy 等 Redis 3.x 常设密码；未配置则不带密码连接
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None
# redis-py 5+ 默认 RESP3 会发 HELLO，Redis 3.x 不支持，固定用协议 2
REDIS_PROTOCOL = 2


def redis_client_kwargs() -> dict[str, Any]:
    """
    创建 Redis 客户端所需参数（与课件 cache_conf 一致）。
    实际连接在 utils/redis_cache.get_redis() 中懒加载，失败则降级查库。
    """
    return {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "db": REDIS_DB,
        "password": REDIS_PASSWORD,
        "protocol": REDIS_PROTOCOL,
        "decode_responses": True,  # 字节解码为字符串，便于 JSON
        "socket_connect_timeout": 0.3,
        "socket_timeout": 0.3,
    }


def create_redis_client() -> redis.Redis:
    """按当前配置构造同步 Redis 客户端（课件 redis.Redis(...)）。"""
    return redis.Redis(**redis_client_kwargs())


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
