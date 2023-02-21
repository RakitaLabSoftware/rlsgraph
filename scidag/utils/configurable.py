import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Type

import hydra_zen as hz
from omegaconf import OmegaConf

__all__ = ["make_node_config", "make_dag_config"]


@dataclass
class NodeConfig:
    name: str
    content: type
    edges: list[str] = field(default_factory=list)


def make_node_config(node) -> NodeConfig:
    name = node.name
    obj_cfg = OmegaConf.structured(
        hz.builds(node.content, populate_full_signature=True, zen_partial=True)
    )
    return NodeConfig(name, obj_cfg)


@dataclass
class DagConfig:
    info: Any
    nodes: dict[str, NodeConfig] = field(default_factory=dict)


def make_dag_config(obj) -> DagConfig:
    cfg = DagConfig(info="")
    for node_name, node in obj.nodes.items():
        node_cfg = make_node_config(node)
        node_cfg.edges = obj.edges[node_name]
        cfg.nodes[node_name] = node_cfg
    return cfg
