import abc
import inspect
from typing import Any, Callable, Self

import hydra_zen as hz

from scidag.core.base import ANode
from scidag.core.struct.variable import build_io
from scidag.storage import Storage
from scidag.utils.configurable import NodeConfig, make_node_config
from scidag.utils.types import AnyCallable


class BaseNode(ANode):
    def __init__(self, name: str, content: AnyCallable) -> None:
        self.name = name
        self.content = content
        self.inputs, self.outputs = build_io(self.content)

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> Self:
        """
        Builds a new instance of `Self` using the provided configuration.

        Args:
            cfg (NodeConfig): The configuration to use to build the node.

        Returns:
            Self: A new instance of `Self`.
        """
        name = cfg.name
        content: AnyCallable = hz.instantiate(cfg.content)
        return cls(name=name, content=content)

    def to_config(self) -> NodeConfig:
        """
        Converts the current node instance to a configuration.

        Returns:
            NodeConfig: The configuration for the current node instance.
        """
        return make_node_config(self)

    def set_storage(self, storage: Storage) -> None:
        """
        Sets the storage for the current node.

        Args:
            storage (Storage): The storage to set for the current node.

        Returns:
            None
        """
        self.storage = storage

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

    @abc.abstractmethod
    async def run(self):
        """
        Runs the current node by retrieving inputs from storage, running the
        node's content, and storing the outputs.
        """
