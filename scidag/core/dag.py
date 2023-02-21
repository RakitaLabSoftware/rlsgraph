import asyncio
from typing import Any, Literal

from hydra_zen import to_yaml
from omegaconf import DictConfig, OmegaConf

from scidag.core.base import ANode
from scidag.storage.build import build_storage
from scidag.utils.algo import topological_sort
from scidag.utils.configurable import make_dag_config, DagConfig


def build_nodes(cfg) -> dict[str, ANode]:
    nodes = {}
    for name, node in cfg.dag:
        nodes[name] = ANode.from_config(node)
    return nodes


def build_edges(cfg) -> dict[str, Any]:
    edges = {}
    for name, node in cfg.dag:
        edges[name] = node.edges
    return edges


class DAG:
    """
    Directed Acyclic Graph
    """

    def __init__(
        self,
        nodes: dict[str, ANode] | None = None,
        edges: dict[str, Any] | None = None,
        storage_type: Literal["CSV", "Dict", "DB"] = "CSV",
    ) -> None:
        self.nodes = nodes if nodes is not None else {}
        self.edges = edges if edges is not None else {}
        self.storage = build_storage(storage_type)

    @classmethod
    def from_config(cls, cfg: DagConfig) -> "DAG":
        nodes = build_nodes(cfg)
        edges = build_edges(cfg)
        return DAG(nodes, edges)

    def to_config(self) -> DagConfig:
        return make_dag_config(self)
        return OmegaConf.structured(make_dag_config(self))

    @property
    def all_nodes(self) -> list[str]:
        return list(self.nodes.keys())

    def get_node(self, node_name: str) -> ANode:
        if node_name not in self.nodes.keys():
            raise KeyError(
                f"Node named {node_name} is not present in this DAG. Try `dag.all_nodes` to see all available nodes"
            )
        return self.nodes[node_name]

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
        # TODO: TypeCheck
        # add edge to graph
        self.edges[source].append(target)

        target, variable = target.split(".")
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

    def topological_sort(self):
        self.nodes = {
            key: self.nodes[key]
            for key in topological_sort(self.nodes, self.edges)
            if key in self.nodes
        }

    async def run(self) -> None:
        # self.topological_sort()
        # await asyncio.gather(*[task.run() for task in self.nodes.values()])
        try:
            await asyncio.gather(*[task.run() for task in self.nodes.values()])
        except Exception as exc:
            exc.add_note(f"Dag was failed due to {exc}")
        finally:
            self.save()

    def save(self):
        self.storage.save()

    def get_available_nodes(self, node_name: str) -> list[str] | None:
        # Find things in StorageGraph that
        # 1. Find disconnected notes
        # 2. Match it dependencies type with node_name
        pass
