import inspect
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Callable

from hydra.utils import instantiate

from scidag.core.base import ANode
from scidag.storage import Storage
from scidag.utils.configurable import NodeConfig, make_node_config
from scidag.utils.types import AnyCallable


@dataclass
class Variable:
    name: str
    type: str
    _value: Any = field(init=False)

    @property
    @cache
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        if type(value) != self.type:
            raise TypeError(
                f"Type of {self.name} should be {self.type} not {type(value)}"
            )
        self.value = value


def _build_io(obj) -> tuple:
    sig = inspect.signature(obj)
    inputs = {}
    for param_name, param in sig.parameters.items():
        if param.default is inspect.Signature.empty:
            param_type = (
                param.annotation if param.annotation is not inspect._empty else None
            )
            inputs[param_name] = Variable(param_name, type=str(param_type))
    output = Variable("out", sig.return_annotation)
    return inputs, output


class Node(ANode):
    def __init__(self, name: str, content: Callable[..., Any]) -> None:
        self.name = name
        self.content = content
        self.build_io()

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> "Node":
        name = cfg.name
        content: AnyCallable = instantiate(cfg.content)
        return Node(name=name, content=content)

    def to_config(self) -> NodeConfig:
        return make_node_config(self)

    def set_storage(self, storage: Storage) -> None:
        self.storage = storage

    async def run(self) -> None:
        # TODO: Check if input values is same as specified in dependencies
        if self.storage is None:
            raise RuntimeError(f"self.storage is not set")
        inputs = await self.storage.get(self.name)
        outputs = self.content(**inputs)
        self.storage.store(self.name, outputs)

    def build_io(self) -> None:
        self.inputs, self.outputs = _build_io(self.content)
