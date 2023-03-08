from typing import Any

from scidag.storage.base import Storage

try:
    import motor
except Exception as e:
    e.add_note(f"motor is not installed")

class MongoStorage(Storage):
    def __init__(self, data:Any|None=None) -> None:
        self._db = data if data is not None else 

    async def get(self, target: str) -> dict[str, Any]:
        return await super().get(target)

    def store(self, source: str, value: Any) -> None:
        return super().store(source, value)

    def add_dependency(self, target: str, variable: str, source: str) -> None:
        return super().add_dependency(target, variable, source)

    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        return super().remove_dependency(target, variable, source)

    def show(self):
        return super().show()

    def save(self, path: str | None = None) -> None:
        return super().save(path)
    