from typing import Any, Callable

from hydra.utils import instantiate

from scidag.core.base import ANode, build_io
from scidag.storage import Storage
from scidag.utils.configurable import NodeConfig, make_node_config
from scidag.utils.types import AnyCallable


def build_node(cfg: NodeConfig):
    return Node.from_config(cfg)


class Node(ANode):
    """
    Base node Class
    """

    def __init__(self, name: str, content: Callable[..., Any]) -> None:
        self.name = name
        self.content = content
        self.inputs, self.outputs = build_io(self.content)

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> "Node":
        name = cfg.name
        content: AnyCallable = instantiate(cfg.content)
        return Node(name=name, content=content)

    def to_config(self) -> NodeConfig:
        return make_node_config(self)

    def set_storage(self, storage: Storage) -> None:
        self.storage = storage

    async def get_inputs(self):
        res = await self.storage.get(self.name)
        if self.inputs is not None:
            for name in self.inputs.keys():
                self.inputs[name].value = res[name]
        return res

    async def run(self) -> None:
        inputs = await self.get_inputs()
        outputs = self.content(**inputs)
        self.storage.store(self.name, outputs)
