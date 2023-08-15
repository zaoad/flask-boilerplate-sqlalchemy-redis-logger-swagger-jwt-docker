# -*- coding: utf-8 -*-
from datetime import timedelta
from enum import Enum
from typing import Union

from my_api.redis_manager.flask_redis import redis_store


class KeyType(Enum):
    INTEGER = 0
    STRING = 1
    SET = 2
    ZSET = 3
    LIST = 4
    HASH = 5


class Base(object):
    """Base model class for redis-py operations"""

    def __init__(self, keyname: str, keytype: KeyType, keyid=None):
        self._redis = redis_store.connection
        self._prefix = redis_store.redis_prefix
        self.keytype = keytype
        self.id = keyid
        self.key = ":".join([self._prefix, ":".join([keyname, keyid]) if keyid else keyname])

    def exists(self):
        return self._redis.exists(self.key) == 1

    def delete(self):
        return self._redis.delete(self.key) == 1

    def expire(self, ttl: timedelta):
        return self._redis.expire(self.key, ttl)

    def ttl(self):
        return self._redis.ttl(self.key)

    def get(self):
        if self.keytype == KeyType.STRING or self.keytype == KeyType.INTEGER:
            return self._redis.get(self.key)
        raise TypeError("Unsupported operation 'get' on non-string key")

    def set(self, value):
        if self.keytype == KeyType.STRING or self.keytype == KeyType.INTEGER:
            return self._redis.set(self.key, value)
        raise TypeError("Unsupported operation 'set' on non-string key")

    def setex(self, ttl: timedelta, value="true"):
        if self.keytype == KeyType.STRING or self.keytype == KeyType.INTEGER:
            return self._redis.setex(self.key, ttl, value)
        raise TypeError("Unsupported operation 'setex' on non-string key")

    def setnx(self, value: str = "true"):
        if self.keytype == KeyType.STRING or self.keytype == KeyType.INTEGER:
            return self._redis.setnx(self.key, value)
        raise TypeError("Unsupported operation 'setnx' on non-string key")

    def incrby(self, amount=1):
        if self.keytype == KeyType.INTEGER:
            return self._redis.incrby(self.key, amount=amount)
        raise TypeError("Unsupported operation 'incrby' on non-string key")

    def incr(self):
        if self.keytype == KeyType.INTEGER:
            return self._redis.incr(self.key)
        raise TypeError("Unsupported operation 'incr' on non-string key")

    def decr(self):
        if self.keytype == KeyType.INTEGER:
            return self._redis.decr(self.key)
        raise TypeError("Unsupported operation 'decr' on non-string key")

    def sadd(self, elements: Union[set, list]):
        if self.keytype == KeyType.SET:
            return self._redis.sadd(self.key, *elements)
        raise TypeError("Unsupported operation 'sadd' on non-set key")

    def smembers(self):
        if self.keytype == KeyType.SET:
            return self._redis.smembers(self.key)
        raise TypeError("Unsupported operation 'smembers' on non-set key")

    def srem(self, *value):
        if self.keytype == KeyType.SET:
            return self._redis.srem(self.key, *value)
        raise TypeError("Unsupported operation 'srem' on non-set key")

    def zadd(self, data: dict, nx: bool = False, xx: bool = False, incr: bool = False):
        if self.keytype == KeyType.ZSET:
            for k, v in data.items():
                if not isinstance(k, str) or not isinstance(v, (int, float)):
                    raise ValueError("Unsupported {key, value} types")
            return self._redis.zadd(self.key, data, nx=nx, xx=xx, incr=incr)
        raise TypeError("Unsupported operation 'zadd' on non-zset key")

    def zincrby(self, value: str, amount=1, score_cast_func=lambda x: int(x)):
        if self.keytype == KeyType.ZSET:
            return score_cast_func(self._redis.zincrby(self.key, score_cast_func(amount), value))
        raise TypeError("Unsupported operation 'zincrby' on non-zset key")

    def zrange(self, start: int, end: int, desc=True, score_cast_func=lambda x: int(x)):
        if self.keytype == KeyType.ZSET:
            return self._redis.zrange(
                self.key, start, end, desc=desc, withscores=False, score_cast_func=score_cast_func
            )
        raise TypeError("Unsupported operation 'zrange' on non-zset key")

    def zrangebyscore(
        self,
        min_score: str,
        max_score: str,
        start=None,
        size=None,
        desc=True,
        score_cast_func=lambda x: int(x),
        withscores=False,
    ):
        if self.keytype == KeyType.ZSET:
            if desc:
                return self._redis.zrevrangebyscore(
                    self.key,
                    max_score,
                    min_score,
                    start=start,
                    num=size,
                    withscores=withscores,
                    score_cast_func=score_cast_func,
                )
            return self._redis.zrangebyscore(
                self.key,
                min_score,
                max_score,
                start=start,
                num=size,
                withscores=withscores,
                score_cast_func=score_cast_func,
            )
        raise TypeError("Unsupported operation 'zrangebyscore' on non-zset key")

    def zrem(self, value: str):
        if self.keytype == KeyType.ZSET:
            return self._redis.zrem(self.key, value)
        raise TypeError("Unsupported operation 'zrem' on non-zset key")

    def zpopmin(self, count: int = 1):
        if self.keytype == KeyType.ZSET:
            return self._redis.zpopmin(self.key, count)
        raise TypeError("Unsupported operation 'zpopmin' on non-zset key")

    def zcount(self, low: float, high: float):
        if self.keytype == KeyType.ZSET:
            return self._redis.zcount(self.key, low, high)
        raise TypeError("Unsupported operation 'zcount' on non-zset key")

    def zremrangebyscore(self, min_score: str, max_score):
        if self.keytype == KeyType.ZSET:
            return self._redis.zremrangebyscore(self.key, min_score, max_score)
        raise TypeError("Unsupported operation 'zremrangebyscore' on non-zset key")

    def zcard(self):
        if self.keytype == KeyType.ZSET:
            return self._redis.zcard(self.key)
        raise TypeError("Unsupported operation 'zcard' on non-zset key")

    def zrank(self, value: str):
        if self.keytype == KeyType.ZSET:
            return self._redis.zrank(self.key, value)
        raise TypeError("Unsupported operation 'zrank' on non-zset key")

    def lpush(self, value: str):
        if self.keytype == KeyType.LIST:
            return self._redis.lpush(self.key, value)
        raise TypeError("Unsupported operation 'lpush' on non-list key")

    def rpop(self):
        if self.keytype == KeyType.LIST:
            return self._redis.rpop(self.key)
        raise TypeError("Unsupported operation 'rpop' on non-list key")

    def llen(self):
        if self.keytype == KeyType.LIST:
            return self._redis.llen(self.key)
        raise TypeError("Unsupported operation 'llen' on non-list key")

    def lrange(self, start: int, end: int):
        if self.keytype == KeyType.LIST:
            return self._redis.lrange(self.key, start, end)
        raise TypeError("Unsupported operation 'lrange' on non-list key")

    def lsetex(self, ttl: timedelta):
        if self.keytype == KeyType.LIST:
            return self._redis.expire(self.key, ttl)
        raise TypeError("Unsupported operation 'lsetex' on non-list key")

    def hsetex(self, ttl: timedelta):
        if self.keytype == KeyType.HASH:
            return self._redis.expire(self.key, ttl)
        raise TypeError("Unsupported operation 'hsetex' on non-hash key")

    def hmset(self, mapping: dict):
        if self.keytype == KeyType.HASH:
            return self._redis.hmset(self.key, mapping=mapping)
        raise TypeError("Unsupported operation 'hmset' on non-hash key")

    def hmget(self, hash_keys: list):
        if self.keytype == KeyType.HASH:
            return self._redis.hmget(self.key, hash_keys)
        raise TypeError("Unsupported operation 'hmget' on non-hash key")

    def hkeys(self):
        if self.keytype == KeyType.HASH:
            return self._redis.hkeys(self.key)
        raise TypeError("Unsupported operation 'hkeys' on non-hash key")

    def hgetall(self):
        if self.keytype == KeyType.HASH:
            return self._redis.hgetall(self.key)
        raise TypeError("Unsupported operation 'hgetall' on non-hash key")

    def hdel(self, hash_keys: list):
        if self.keytype == KeyType.HASH:
            return self._redis.hdel(self.key, *hash_keys)
        raise TypeError("Unsupported operation 'hdel' on non-hash key")
