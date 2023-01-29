from typing import Any

from omegaconf import DictConfig

from scidag.core.task import Task
from scidag.utils.runnable import Runnable


class DAG(Runnable):
    """
    Directed Acyclic Graph
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
    def from_config(cls, cfg: DictConfig):
        r"""
        Build :class:`DAG` by provided config

        Parameters
        ----------
        cfg : DictConfig
            _description_
        """
        # TODO: Unpack config to the DAG
        return DAG()

    def get_task(self, task_name: str) -> Task:
        """Get Task by its name"""
        return self.tasks[task_name]

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

    def get_available_tasks(self, task_name: str) -> list[str] | None:
        r"""
        Shows available tasks to add after this task

        Returns
        -------
        list[str] | None
            Available tasks after this task
        Example
        -------
        """
        # Find things in StorageGraph that

    def run(self) -> None:
        """Run dag with logging and saving configuration file"""
        for task in self.tasks.values():
            task.run()

    def save(self):
        """Save DAG configuration to specific format"""
        for task in self.task.values():
            task.save()
