from typing import Any

from scidag.storage.base import Storage

try:
    import redis
    import redis_om
except ModuleNotFoundError:
    raise ModuleNotFoundError(f"Dask not found try to install scidag[dask]")


class Row(redis_om.HashModel):
    target: str
    variable: str
    source: str
    value: Any

class RedisCache(Storage):
    def __init__(self) -> None:
        super().__init__()
        self._db = redis.Redis(host="localhost", port=6379, db=0)

    async def get(self, request_name):
        target_rows = Row.find(Row.target == target)
        if Row.

    def add_dependency(self) -> None:
        pass

    def remove_dependency(self) -> None:
        pass

    def store(self, node_name: str, value_name: str, value: Any):
        pass

    def show(self):
        pass
