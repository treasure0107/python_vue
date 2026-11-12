import json
import logging
from typing import Any

import redis

from config.cache_conf import REDIS_DB, REDIS_ENABLED, REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None
_redis_disabled = False


def get_redis() -> redis.Redis | None:
    """获取 Redis 客户端；未启用或连接失败时返回 None（降级走数据库）。"""
    global _client, _redis_disabled
    if not REDIS_ENABLED or _redis_disabled:
        return None
    if _client is not None:
        return _client
    try:
        _client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=0.3,
            socket_timeout=0.3,
        )
        _client.ping()
        return _client
    except redis.RedisError as exc:
        logger.warning("Redis 不可用，已降级为直查数据库: %s", exc)
        _redis_disabled = True
        _client = None
        return None


def close_redis() -> None:
    global _client, _redis_disabled
    if _client is not None:
        _client.close()
        _client = None
    _redis_disabled = False


def cache_get(key: str) -> Any | None:
    client = get_redis()
    if client is None:
        return None
    try:
        raw = client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except (redis.RedisError, json.JSONDecodeError) as exc:
        logger.warning("读取缓存失败 key=%s: %s", key, exc)
        return None


def cache_set(key: str, value: Any, ttl_seconds: int) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        client.setex(key, ttl_seconds, json.dumps(value, default=str))
    except (redis.RedisError, TypeError) as exc:
        logger.warning("写入缓存失败 key=%s: %s", key, exc)


def cache_delete(*keys: str) -> None:
    client = get_redis()
    if client is None or not keys:
        return
    try:
        client.delete(*keys)
    except redis.RedisError as exc:
        logger.warning("删除缓存失败: %s", exc)


def cache_delete_by_pattern(pattern: str) -> int:
    client = get_redis()
    if client is None:
        return 0
    deleted = 0
    try:
        for key in client.scan_iter(match=pattern, count=200):
            deleted += client.delete(key)
    except redis.RedisError as exc:
        logger.warning("按模式清理缓存失败 pattern=%s: %s", pattern, exc)
    return deleted
