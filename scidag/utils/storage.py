from typing import Any
from omegaconf import DictConfig


class MetaBorg(type):
    """Borg  class  that contains shared state between storages"""

    _state = {"__skip_init__": False}

    def __call__(cls, *args: list[Any], **kwargs: dict[Any, Any]):
        if cls._state["__skip_init__"]:
            cls.__check_args(*args, **kwargs)

        instance = object().__new__(cls, *args, **kwargs)

        instance.__dict__ = cls._state

        if not cls._state["__skip_init__"]:
            instance.__init__(*args, **kwargs)
            cls._state["__skip_init__"] = True

        return instance


class Storage(MetaBorg):
    """
    Storage that contains inputs and outputs of each task.
    """

    def __init__(self, cfg: DictConfig) -> None:
        self.task_name = cfg.name
        self.dependencies = cfg.dependencies
        self.dict = {}

    def put(self, name: str, value: Any) -> None:
        """
        Put value with name in Storage.
        """

    def get(self, name: str) -> Any:
        """
        Get value from task it depends storage by it's name.
        """
