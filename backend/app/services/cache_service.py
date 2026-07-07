"""Redis-backed cache service.

Fails open on purpose: if Redis is unreachable for any reason, every method
degrades to a no-op / cache-miss instead of raising, so the app keeps working
(just without the speed-up) rather than going down because a cache is offline.
"""

import json
import logging

import redis
from flask import current_app

logger = logging.getLogger(__name__)

_client = None
_client_url = None


def _get_client():
    global _client, _client_url
    url = current_app.config["REDIS_URL"]
    if _client is None or _client_url != url:
        _client = redis.from_url(
            url, decode_responses=True, socket_connect_timeout=2, socket_timeout=2
        )
        _client_url = url
    return _client


class CacheService:
    @staticmethod
    def get(key):
        try:
            raw = _get_client().get(key)
            return json.loads(raw) if raw is not None else None
        except Exception as e:
            logger.debug(f"[CacheService] get miss for {key}: {e}")
            return None

    @staticmethod
    def set(key, value, ttl_seconds=None):
        try:
            ttl = ttl_seconds or current_app.config["CACHE_DEFAULT_TTL_SECONDS"]
            _get_client().set(key, json.dumps(value), ex=ttl)
        except Exception as e:
            logger.debug(f"[CacheService] set skipped for {key}: {e}")

    @staticmethod
    def delete(key):
        try:
            _get_client().delete(key)
        except Exception as e:
            logger.debug(f"[CacheService] delete skipped for {key}: {e}")

    @staticmethod
    def delete_pattern(pattern):
        try:
            client = _get_client()
            keys = list(client.scan_iter(match=pattern, count=100))
            if keys:
                client.delete(*keys)
        except Exception as e:
            logger.debug(f"[CacheService] delete_pattern skipped for {pattern}: {e}")
