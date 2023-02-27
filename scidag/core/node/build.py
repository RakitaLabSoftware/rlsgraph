from scidag.utils.configurable import NodeConfig

from .end_node import EndNode
from .node import Node
from .start_node import StartNode


def build_node(cfg: NodeConfig):
    if cfg.variables is None:
        return StartNode.from_config(cfg)
    if cfg.edges is None:
        return EndNode.from_config(cfg)
    return Node.from_config(cfg)
