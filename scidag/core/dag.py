import asyncio
from typing import Any

import uvloop
from omegaconf import DictConfig

from scidag.core.node import Node
from scidag.utils.runnable import BaseElement

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DAG(BaseElement):
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
        self.nodes: dict[str, Node] = build_nodes()

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

    def get_node(self, task_name: str) -> Node:
        """Get Task by its name"""
        return self.nodes[task_name]

    def append(self, node: Node, *, dependencies: dict[str, Any]):
        r"""
        Append New Task To current Dag with edges specified in dependencies

        Parameters
        ----------
        task : Task
            _description_
        dependencies : dict[str, Any]
            _description_
        """
        # TODO: Make also possible to add stuff by wrappers
        # Check if task can be appended to parent nodes and its outputs is also specified
        # IF dependencies are multiple then await asyncio.gather(*all tasks)

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

    async def run(self):
        """Run dag with logging and saving configuration file"""
        # TODO: CREATE AN EVENTLOOP AND RUN IT ASYNCRONIOUSLY
        # initialise eventloop
        loop = asyncio.get_event_loop()
        loop.run()
        for task in self.tasks.values():
            await task.run()
        asyncio.run(self._main())

    def save(self):
        """Save DAG configuration to specific format"""
        for task in self.task.values():
            task.save()

    def show(self):
        """Visualise Graph"""
