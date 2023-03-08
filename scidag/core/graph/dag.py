import asyncio
import os
from datetime import datetime

import uvloop
from omegaconf import OmegaConf

from scidag.core.base import AGraph, ANode
from scidag.core.edge.edge import Edges
from scidag.core.hooks.hook import Hooks
from scidag.core.node.nodes import Nodes
from scidag.storage import Storage, build_storage
from scidag.storage.csv_storage import CSVStorage
from scidag.utils.configurable import DagConfig, make_dag_config
from scidag.utils.funcs import is_interactive

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DAG(AGraph):
    """
    Directed Acyclic Graph
    """

    def __init__(
        self,
        nodes: Nodes | None = None,
        edges: Edges | None = None,
        storage: Storage | None = None,
        settings: dict | None = None,
    ) -> None:
        self.storage = storage if storage is not None else CSVStorage()
        self.nodes = nodes if nodes is not None else Nodes(self.storage)
        self.edges = edges if edges is not None else Edges(self.storage)
        self.hooks = Hooks()
        self.meta = dict()

    @classmethod
    def from_config(cls, cfg: DagConfig) -> "DAG":
        storage = build_storage(cfg)
        nodes = Nodes.from_config(cfg, storage)
        edges = Edges.from_config(cfg, storage)
        return DAG(nodes, edges, storage)

    def to_config(self) -> DagConfig:
        return OmegaConf.structured(make_dag_config(self))

    # NODES
    @property
    def all_nodes(self) -> list[str]:
        return list(self.nodes.names)

    def add(self, node: ANode) -> None:
        self.nodes.add(node)

    def remove(self, node: ANode) -> None:
        self.nodes.remove(node)

    # EDGES
    @property
    def all_edges(self):
        return self.edges.adjacency_list

    def get_node(self, node_name: str) -> ANode:
        return self.nodes.get_node(node_name)

    def connect(self, source: str, target: str, variable: str) -> None:
        # get nodes
        source_node = self.get_node(source)
        target_node = self.get_node(target)

        # FIXME Make this code less ugly
        if target_node.inputs is None:
            raise KeyError(f"{target_node} have no inputs")

        try:
            in_type = target_node.inputs[variable].type
        except KeyError as e:
            e.add_note(f"There is no {variable=} in target node")
            raise e

        out_type = source_node.outputs.type
        # if out_type is not in_type:
        #     raise TypeError(
        #         f"Node with outputs of type = {out_type} can't be connected to {in_type}"
        #     )
        # add edge to graph
        self.edges.add(source=source, target=target, variable=variable)
        self.storage.add_dependency(target, variable, source)

    def disconnect(self, source: str, target: str) -> None:
        # get nodes
        target, variable = target.split(".")
        # remove edge from self.graph
        if not (self.nodes.get_node(source) or self.nodes.get_node(target)):
            KeyError(f"Node with name {source} or {target} not stored in this dag.")
        self.edges.remove(target=target, source=source, variable=variable)
        self.storage.remove_dependency(target, variable, source)

    # HOOKS
    def add_hook(self, hook) -> None:
        self.hooks.add(hook)

    def remove_hook(self, hook) -> None:
        self.hooks.remove(hook)

    def connect_hook(self, source: str):
        self.hooks.connect(source)

    def disconnect_hook(self, source: str):
        self.hooks.disconnect(source)

    # RUNS
    def run(self, start: str | None = None) -> None:
        if is_interactive():
            try:
                import nest_asyncio
            except Exception:
                raise
            nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self(start))

    async def __call__(self, start: str | None = None) -> None:
        # TODO implement start from a specific node
        # nodes = self.get_tasks(start)
        try:
            await asyncio.gather(*[node.run() for node in self.nodes.objects])
        except Exception as exc:
            exc.add_note(f"Execution of DAG was failed due to {exc} ")
            raise
        finally:
            self.save()

    # UTILS
    def save(self) -> None:
        dtm = datetime.now().strftime("%d-%m-%Y_%H-%M")
        path_dir = os.path.join("configs", str(dtm))
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        OmegaConf.save(
            self.to_config(), os.path.join(path_dir, "config.yaml"), resolve=True
        )
        self.storage.save(path_dir)

    def get_available_nodes(self, node_name: str) -> list[str] | None:
        # Find things in StorageGraph that
        # 1. Find disconnected notes
        # 2. Match it dependencies type with node_name
        pass

    def find_all_children(self, node: str) -> list[str] | None:
        """
        find all children nodes to specific node
        """
        children = self.edges.get_children(node)
        return children
