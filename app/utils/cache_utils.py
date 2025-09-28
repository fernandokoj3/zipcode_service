from __future__ import annotations

from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Final, Literal

import diskcache
from diskcache import Cache
from redis import Redis

from app.utils.settings import settings


class BaseCache(ABC):

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ex: int) -> None:
        pass

    @abstractmethod
    def clear(self, key) -> None:
        pass


class RedisCache(BaseCache):

    def __init__(self):
        self._cache = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.host.db,
            password=settings.redis.password,
            decode_responses=True,
        )

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ex: int) -> None:
        self._cache.set(name=key, value=value, ex=ex)

    def clear(self, key) -> None:
        self._cache.delete(key)


class MemoryCache(BaseCache):
    _CACHE_SIZE_MB: Final[int] = 450

    def __init__(self):
        self._cache: Cache = diskcache.Cache(
            size_limit=self._CACHE_SIZE_MB * 1024 * 1024,
            eviction_policy="least-recently-used",
            directory="/tmp",  # nosec
            sqlite_synchronous=0,
        )

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ex: int) -> None:
        self._cache.set(key, value, expire=ex)

    def clear(self, key) -> None:
        self._cache.delete(key)


def cache_factory(
    backend: Literal["memory", "redis"],
) -> BaseCache:
    if backend == "memory":
        return MemoryCache()
    elif backend == "redis":
        return RedisCache()
    else:
        raise ValueError(
            f"Backend '{backend}' não suportado. Use 'memory' ou 'redis'."
        )


cache_module: BaseCache = cache_factory("memory")


def async_ttl_cache(ttl: int, key: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            local_key = f"{func.__name__}:{key}"

            if found := cache_module.get(local_key):
                return found

            result = await func(*args, **kwargs)
            cache_module.set(local_key, result, ex=ttl)
            return result

        return wrapper

    return decorator


def ttl_cache(ttl: int, key: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            local_key = f"{func.__name__}:{key}"

            if found := cache_module.get(local_key):
                return found

            result = func(*args, **kwargs)
            cache_module.set(local_key, result, ex=ttl)
            return result

        return wrapper

    return decorator


__all__ = [async_ttl_cache, ttl_cache]
