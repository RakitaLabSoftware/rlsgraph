from typing import Any

from scidag.storage.base import Storage

# try:
#     import redis
# except ModuleNotFoundError:
#     raise ModuleNotFoundError(f"Dask not found try to install scidag[dask]")


class RedisStorage(Storage):
    def __init__(self) -> None:
        super().__init__()

    def get(self, request_name):
        return

    def add_dependency(self) -> None:
        pass

    def remove_dependency(self) -> None:
        pass

    def store(self, node_name: str, value_name: str, value: Any):
        pass
