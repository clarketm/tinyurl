from os import getenv
from typing import Dict

from redis import Redis


class Database:
    def __init__(self, host: str = getenv("REDIS_MASTER_SERVICE_HOST", "0.0.0.0"), port: int = getenv("REDIS_MASTER_SERVICE_PORT", "6379")):
        self.db = Redis(host, port)

    def get_all(self, hash: str) -> Dict:
        return self.db.hgetall(hash)

    def get(self, hash: str, key: str) -> Dict:
        return self.db.hget(hash, key)
