from typing import Any

from omegaconf import DictConfig

from scidag.core._runnable import Runnable
from scidag.core.task import Task


class DAG(Runnable):
    """
    Class to manupulate dags
    """

    def __init__(self, cfg: DictConfig) -> None:
        """
        Parameters
        ----------
        cfg : DictConfig
            _description_
        """
        self.tasks: dict[str, Task] = build_tasks()

    @classmethod
    def build_from_cfg(cls, cfg: DictConfig):
        """
        Build `DAG` by provided config

        Parameters
        ----------
        cfg : DictConfig
            _description_
        """

    def get_task(self, name: str) -> Task:
        """Get Task by its name"""
        return self.tasks[name]

    def append(self, task: Task, dependencies: dict[str, Any]):
        """
        Append New Task To current Dag with edges specified in dependencies

        Parameters
        ----------
        task : Task
            _description_
        dependencies : dict[str, Any]
            _description_
        """
        # Check if task can be appended to parent nodes and its outputs is also specified

    def run(self) -> None:
        """run dag with logging and saving in hydra"""
        for task in self.tasks.values():
            task.run()
