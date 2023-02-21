import sqlite3 as sl
from typing import Any

from scidag.storage.base import Storage


class DBStorage(Storage):
    def __init__(self) -> None:
        sl.connect("my_database.db")
