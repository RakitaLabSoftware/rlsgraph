import abc
from dataclasses import dataclass, field
from typing import Any

from scidag.core.struct.variable import Variable
from scidag.storage.base import Storage
from scidag.utils.types import AnyCallable

from ..base import Base


class AHook(Base):
    name: str
    inputs: dict[str, Variable] | None

    @abc.abstractmethod
    def set_storage(self, storage: Storage) -> None:
        pass

    @abc.abstractmethod
    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """


class Hook(AHook):
    def __init__(self, hook_content: AnyCallable):
        self.content = hook_content

    async def get_inputs(self):
        """
        Retrieves inputs for the current node from storage.

        Returns:
            dict: A dictionary containing the inputs for the current node.
        """
        res = await self.storage.get(self.name)
        if self.inputs is not None:
            for name in self.inputs.keys():
                self.inputs[name].value = res[name]
        return res

    async def run(self) -> Any:
        try:
            inputs = await self.get_inputs()
            self.content(**inputs)
        except Exception:
            print(f"Dag Execution failed in Hook:{self.name}")
            raise


@dataclass
class Hooks:
    hook_map: dict[str, Hook] = field(default_factory=dict)

    def add(self, hook: Hook):
        self.hook_map["hook"] = hook

    def remove(self, hook_name: str):
        pass

    def connect(self, source: str):
        pass

    def disconnect(self, source: str):
        pass

    def disable_all(self):
        pass

    def enable_all(self):
        pass
