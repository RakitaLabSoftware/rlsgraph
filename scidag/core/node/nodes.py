from dataclasses import dataclass, field

from scidag.core.base import ANode
from scidag.core.node.end_node import EndNode
from scidag.core.node.node import Node
from scidag.core.node.start_node import StartNode
from scidag.storage.base import Storage
from scidag.utils.configurable import NodeConfig


def build_node(cfg: NodeConfig):
    if cfg.variables is None:
        return StartNode.from_config(cfg)
    if cfg.edges is None:
        return EndNode.from_config(cfg)
    return Node.from_config(cfg)


@dataclass(slots=True)
class Nodes:
    storage: Storage = field(repr=False)
    nodes: dict[str, ANode] = field(default_factory=dict)

    def __post_init__(self):
        self.set_storage(self.storage)

    def add(self, node):
        if node.name in self.nodes.keys():
            raise KeyError(
                f"This node_name = {node.name} is already reserved for {self.nodes[node.name]}"
            )
        node.storage = self.storage
        self.nodes[node.name] = node

    def remove(self, node):
        if node.name not in self.nodes:
            KeyError(f"Node with name {node.name} not stored in this dag.")
        del self.nodes[node.name]

    def set_storage(self, storage):
        for node in self.nodes.values():
            node.storage = storage

    def get_node(self, node_name: str) -> ANode:
        if node_name not in self.nodes.keys():
            raise KeyError(
                f"Node named {node_name} is not present in this DAG. Try `dag.all_nodes` to see all available nodes"
            )
        return self.nodes[node_name]

    @property
    def names(self) -> list[str]:
        return list(self.nodes.keys())

    @property
    def objects(self) -> list[ANode]:
        return list(self.nodes.values())

    @classmethod
    def from_config(cls, cfg, storage):
        nodes = {}
        for name, node_cfg in cfg.dag.items():
            nodes[name] = build_node(node_cfg)
        return Nodes(storage, nodes)
