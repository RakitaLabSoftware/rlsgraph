import asyncio
from typing import Any

from scidag.storage.base import DataRow, Storage


class DictStorage(Storage):
    def __init__(self):
        self._storage: list[DataRow] = []

    async def get(self, request_name: str):
        ret = {
            row.value_name: row.value
            for row in self._storage
            if row.node_to == request_name
        }
        if not all(val is not None for val in ret.values()):
            await asyncio.sleep(0.1)
        return ret

    def store(self, node_from: str, value_name: str, value: Any) -> None:
        # find all values that required node_name
        indexes: list[int] = [
            idx
            for idx, row in enumerate(self._storage)
            if (row.node_from == node_from and row.value_name == value_name)
        ]
        # fill all values
        for index in indexes:
            self._storage[index].value = value

    def add_dependency(self, node_from: str, node_to: str, value_name: str) -> None:
        self._storage.append(DataRow(node_from, node_to, value_name))

    def remove_dependency(self, node_from: str, node_to: str, value_name: str) -> None:
        ref = DataRow(node_from, node_to, value_name)
        self._storage.remove(ref)
