from scidag.storage.base import Storage
from scidag.storage.csv_storage import CSVStorage
from scidag.storage.dict_storage import DictStorage
from scidag.storage.redis_storage import RedisStorage


def build_storage(storage_type: str) -> Storage:
    match storage_type:
        case "CSV":
            return CSVStorage()
        case "DB":
            return RedisStorage()
        case "Dict":
            return DictStorage()
        case _:
            raise NameError(f"Storage of type {storage_type} not exist")
