import asyncio
from typing import Any

import nest_asyncio
import uvloop
from omegaconf import OmegaConf

from scidag.core.node import build_node
from scidag.core.base import AGraph, ANode
from scidag.storage import Storage, build_storage
from scidag.storage.csv_storage import CSVStorage
from scidag.utils.configurable import DagConfig, make_dag_config
from scidag.utils.types import AnyCallable

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def build_nodes(cfg) -> dict[str, ANode]:
    nodes = {}
    for name, node_cfg in cfg.dag.items():
        nodes[name] = build_node(node_cfg)
    return nodes


def build_edges(cfg) -> dict[str, Any]:
    edges = {}
    for name, node in cfg.dag.items():
        edges[name] = node.edges
    return edges


class DAG(AGraph):
    """
    Directed Acyclic Graph
    """

    def __init__(
        self,
        nodes: dict[str, ANode] | None = None,
        edges: dict[str, Any] | None = None,
        storage: Storage | None = None,
    ) -> None:
        self.nodes = nodes if nodes is not None else {}
        self.edges = edges if edges is not None else {}
        self.storage = storage if storage is not None else CSVStorage()
        for node in self.nodes.values():
            node.storage = self.storage

    @classmethod
    def from_config(cls, cfg: DagConfig) -> "DAG":
        nodes = build_nodes(cfg)
        edges = build_edges(cfg)
        storage = build_storage(cfg)
        return DAG(nodes, edges, storage)

    def to_config(self) -> DagConfig:
        return OmegaConf.structured(make_dag_config(self))

    @property
    def all_nodes(self) -> list[str]:
        return list(self.nodes.keys())

    @property
    def all_edges(self):
        pass

    def get_node(self, node_name: str) -> ANode:
        if node_name not in self.nodes.keys():
            raise KeyError(
                f"Node named {node_name} is not present in this DAG. Try `dag.all_nodes` to see all available nodes"
            )
        return self.nodes[node_name]

    def _add(self, obj: AnyCallable):
        # TODO: add wrapper
        pass

    def add(self, node: ANode) -> None:
        if node.name in self.nodes.keys():
            raise KeyError(
                f"This node_name = {node.name} is already reserved for {self.nodes[node.name]}"
            )
        node.storage = self.storage
        self.nodes[node.name] = node
        self.edges[node.name] = []

    def remove(self, node: ANode) -> None:
        if node.name not in self.nodes:
            KeyError(f"Node with name {node.name} not stored in this dag.")
        del self.nodes[node.name]

    def connect(self, source: str, target: str) -> None:
        # get nodes
        target, variable = target.split(".")
        source_node = self.get_node(source)
        target_node = self.get_node(target)

        if target_node.inputs is None:
            raise KeyError

        in_type = target_node.inputs[variable].type
        out_type = source_node.outputs.type

        if out_type != in_type:
            raise TypeError(
                f"Node with outputs of type:{out_type} can't be connected to {in_type}"
            )

        # add edge to graph
        self.edges[source].append(target + "." + variable)

        self.storage.add_dependency(target, variable, source)

    def disconnect(self, source: str, target: str) -> None:
        # get nodes
        target, variable = target.split(".")

        # remove edge from self.graph
        if not (self.nodes[source] or self.nodes[target]):
            KeyError(f"Node with name {source} or {target} not stored in this dag.")
        self.storage.remove_dependency(target, variable, source)

    def __call__(self) -> None:
        asyncio.run(self.run())

    def nb_run(self) -> None:
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())

    async def run(self) -> None:
        try:
            await asyncio.gather(*[node.run() for node in self.nodes.values()])
        except Exception as exc:
            exc.add_note(f"Dag was failed due to {exc}")
        finally:
            self.save()

    def save(self):
        OmegaConf.save(self.to_config(), "cfg.yaml")
        self.storage.save()

    def get_available_nodes(self, node_name: str) -> list[str] | None:
        # Find things in StorageGraph that
        # 1. Find disconnected notes
        # 2. Match it dependencies type with node_name
        pass
