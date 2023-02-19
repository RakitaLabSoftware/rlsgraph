import asyncio

import networkx as nx
from omegaconf import DictConfig

from scidag.core.node import Node
from scidag.utils.runnable import BaseElement
from scidag.utils.storage import DataStorage


class DAG(BaseElement):
    """
    Directed Acyclic Graph
    """

    def __init__(
        self, graph: nx.DiGraph | None = None, storage: DataStorage | None = None
    ) -> None:
        self.graph = graph if graph is not None else nx.DiGraph()
        self.storage = storage if storage is not None else DataStorage()

    @classmethod
    def from_config(cls, cfg: DictConfig) -> "DAG":
        r"""
        Build :class:`DAG` by provided config

        Parameters
        ----------
        cfg : DictConfig
            _description_
        """
        graph = build_graph(cfg)
        storage = DataStorage()
        return DAG(graph, storage)

    def get_node(self, node_name: str):
        """Get Task by its name"""
        if node_name not in self.graph.nodes.keys():
            raise KeyError(
                f"Node named {node_name} is not present in this DAG. Try `dag.all_nodes` to see all available nodes"
            )
        return self.graph.nodes[node_name]["node"]

    def add(self, node: Node) -> None:
        r"""Add :class:`scidag.Node` to pool of nodes"""
        self.graph.add_node(node.name, node=node)
        self.storage.add_node(node.name, node=node)

    def remove(self, node: Node) -> None:
        r"""Remove :class:`scidag.Node` from this dag"""
        self.graph.remove_node(node.name)
        self.storage.remove_node(node.name)

    def connect(self, u_node_name: str, v_node_name: str) -> None:
        """
        Connect dependencies of two nodes

        Parameters
        ----------
        u_node_name : str
            _description_
        v_node_name : str
            _description_
        """
        # get nodes
        v_node_name, target_variable_name = v_node_name.split(".")
        v_node = self.get_node(v_node_name)
        u_node = self.get_node(u_node_name)

        # add edge to graph
        self.graph.add_edge(
            u_node.name, v_node.name, target_variable=target_variable_name
        )
        self.storage.add_edge(
            u_node.name, v_node.name, target_variable=target_variable_name
        )

    def disconnect(self, u_node_name: str, v_node_name: str) -> None:
        # get nodes
        v_node_name, v_node_prefix = v_node_name.split(".")
        v_node = self.get_node(v_node_name)
        u_node = self.get_node(u_node_name)

        # remove edge from self.graph
        self.graph.remove_edge(u_node.name, v_node.name)
        self.storage.remove_edge(u_node.name, v_node.name)

    def get_available_nodes(self, node_name: str) -> list[str] | None:
        r"""
        Shows available tasks to add after this task

        Returns
        -------
        list[str] | None
            Available tasks after this task
        """
        # Find things in StorageGraph that
        # 1. Find disconnected notes
        # 2. Match it dependencies type with node_name
        pass

    def __call__(self) -> None:
        """Run dag with logging and saving configuration file"""
        asyncio.run(self.run())

    async def run(self) -> None:
        tasks = list(nx.topological_sort(self.graph))
        await asyncio.gather(*[task.run() for task in tasks])

    @property
    def all_nodes(self):
        return list(self.graph.nodes.keys())
