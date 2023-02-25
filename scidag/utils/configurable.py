import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Type, Optional

import hydra_zen as hz
from omegaconf import OmegaConf


__all__ = ["make_node_config", "make_dag_config"]


@dataclass(slots=True)
class VariableConfig:
    type: str
    value: Optional[Any] = None


def make_variables_config(
    variables: dict[str, Any]
) -> dict[str, VariableConfig] | None:
    if variables is None:
        return None
    variable_dict = {}
    for name, variable in variables.items():
        variable_dict[name] = VariableConfig(variable.type, variable.value)
    return variable_dict


@dataclass(slots=True)
class NodeConfig:
    name: str
    content: Any
    variables: Optional[dict[str, VariableConfig]] = field(default_factory=dict)
    edges: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DagConfig:
    info: Any
    dag: dict[str, NodeConfig] = field(default_factory=dict)


def make_node_config(node) -> NodeConfig:
    name = node.name
    obj_cfg = OmegaConf.structured(
        hz.builds(node.content, populate_full_signature=True, zen_partial=True)
    )
    variables = make_variables_config(node.inputs)
    return NodeConfig(name, obj_cfg, variables)


def make_dag_config(obj) -> DagConfig:
    cfg = DagConfig(info="")
    for node_name, node in obj.nodes.items():
        node_cfg = make_node_config(node)
        node_cfg.edges = obj.edges[node_name]
        cfg.dag[node_name] = node_cfg
    return cfg
