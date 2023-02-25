from scidag.storage.base import Storage
from scidag.storage.csv_storage import CSVStorage
from scidag.storage.db_storage import DBStorage
from typing import Type


def build_storage(cfg) -> Storage:
    storage_type = "CSV"
    storage_cls = _build_storage(storage_type=storage_type)
    return storage_cls.from_config(cfg)


def _build_storage(storage_type: str) -> Type[Storage]:
    match storage_type:
        case "CSV":
            return CSVStorage
        case "DB":
            return DBStorage
        case _:
            raise NameError(f"Storage of type {storage_type} not exist")
