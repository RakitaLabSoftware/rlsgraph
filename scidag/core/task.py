from hydra.utils import instantiate
from omegaconf import DictConfig
from typing import Any
from scidag.utils.runnable import Runnable
from scidag.utils.storage import Storage


class Task(Runnable):
    """
    Task
    """

    def __init__(self, content: Any) -> None:
        """
        _summary_

        Parameters
        ----------
        content : Any
            _description_
        """
        self.content = content
        self.cfg = self.create_config(self)
        self.storage = Storage(self.cfg)

    @classmethod
    def from_config(cls, cfg: DictConfig, **kwargs) -> "Task":
        content = instantiate(cfg.content, kwargs)
        return Task(
            content,
        )

    def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """
        # TODO: Check if input values is same as specified in dependencies
        inputs = self.storage.get(self.cfg.dependencies)
        res = self.content(*inputs)
        self.storage.put(res)

    def save(self):
        return self.cfg
