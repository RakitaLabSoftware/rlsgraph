import asyncio
from typing import Any

from hydra.utils import instantiate
from omegaconf import DictConfig

from scidag.utils.runnable import BaseElement
from scidag.utils.storage import Storage
from scidag.utils.configurable import create_config


class Node(BaseElement):
    """
    Node of DAG
    """

    def __init__(
        self,
        content: Any,
    ) -> None:
        """
        Parameters
        ----------
        content : Any
            _description_
        """
        self.content = content
        self.cfg = build_config(self)
        self.storage = Storage(self.cfg)

    @classmethod
    def from_config(cls, cfg: DictConfig, **kwargs) -> "Node":
        content = instantiate(cfg.content, kwargs)
        return Node(content)

    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """
        # TODO: Check if input values is same as specified in dependencies
        inputs = self.storage.get(self.cfg.dependencies)
        res = self.content(*inputs)
        self.storage.put(res)

    def save(self):
        return self.cfg
