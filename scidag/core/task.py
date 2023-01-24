from scidag.core._runnable import Runnable
from omegaconf import DictConfig
from scidag.utils.storage import Storage


class Task(Runnable):
    def __init__(self, cfg: DictConfig) -> None:
        self.cfg = cfg
        self.storage = Storage(cfg)

    def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """

    @property
    def available_tasks(self) -> list[str]:
        r"""
        Shows available tasks to add after this task

        Returns
        -------
        list[str]
            Available tasks after this task
        Example
        -------
        """
        # Find things in StorageGraph that
