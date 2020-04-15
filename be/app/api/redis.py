from os import getenv

from redis import Redis as RedisClient


class Redis:
    def __init__(
        self,
        host: str = getenv("REDIS_MASTER_SERVICE_HOST", "0.0.0.0"),
        port: str = getenv("REDIS_MASTER_SERVICE_PORT", "6379"),
        hash: str = "default_hash",
    ):
        self.db = RedisClient(host=host, port=int(port))
        self.hash = hash

    def get_all(self):
        return self.db.hgetall(self.hash)

    def get(self, key: str):
        return self.db.hget(self.hash, key)

    def set(self, key: str, value: str):
        return self.db.hsetnx(self.hash, key, value)
