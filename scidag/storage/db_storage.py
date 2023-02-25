import sqlite3 as sl
from typing import Any

from scidag.storage.base import Storage

try:
    import sqlalchemy
except ImportError as ex:
    ex.add_note("Module sqlalchemy is not found")


class DBStorage(Storage):
    def __init__(self) -> None:
        self.storage = sqlalchemy.create_engine("/")

    def add_dependency(self, target: str, variable: str, source: str) -> None:
        return super().add_dependency(target, variable, source)

    def get(self, target: str) -> dict[str, Any]:
        return {}  # return await super().get(target)

    def store(self, source: str, value: Any) -> None:
        return super().store(source, value)

    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        return super().remove_dependency(target, variable, source)

    def save(self) -> None:
        return super().save()
