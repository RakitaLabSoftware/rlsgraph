from dataclasses import dataclass, field
from typing import Any, Optional

import hydra_zen as hz
import numpy as np
from omegaconf import ListConfig, OmegaConf

import inspect


@dataclass(slots=True)
class VariableConfig:
    type: str
    value: Any | None = None


def make_variables_config(
    variables: dict[str, Any]
) -> dict[str, VariableConfig] | None:
    if variables is None:
        return None
    variable_dict = {}
    for name, variable in variables.items():
        value = variable.value
        if isinstance(value, np.ndarray):
            value = ListConfig(value.tolist())
            value.pretty(multiline=False)
        variable_dict[name] = VariableConfig(variable.type, value)
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


def get_nested_params(obj):
    params = {}
    for param_name, param in inspect.signature(obj).parameters.items():
        # FIXME rewrite
        if (
            param.default != inspect.Parameter.empty
            and inspect.isclass(param.default.__class__)
            and not isinstance(param.default, (int, float, str, bool))
        ):
            inner_params = {}
            for inner_param_name in list(
                inspect.signature(param.default.__init__).parameters.keys()
            ):
                inner_params[inner_param_name] = getattr(
                    param.default, inner_param_name
                )
            params[param_name] = OmegaConf.structured(
                hz.builds(
                    param.default.__class__,
                    **inner_params,
                    populate_full_signature=True,
                )
            )
    return params


def make_node_config(node) -> NodeConfig:
    name = node.name
    params = get_nested_params(node.content)
    try:
        obj_cfg = hz.builds(
            node.content,
            **params,
            populate_full_signature=True,
            zen_partial=True,
        )
    except AttributeError:
        obj_cfg = hz.builds(
            node.content.__class__, **params, populate_full_signature=True
        )
    cfg = OmegaConf.structured(obj_cfg)
    # append  to node_sig
    variables = make_variables_config(node.inputs)
    return NodeConfig(name, cfg, variables)


def make_dag_config(obj) -> DagConfig:
    cfg = DagConfig(info="")
    cfg.info = obj.meta
    # FIXME: Bad naming for node pairs
    for node_name, node in obj.nodes.nodes.items():
        node_cfg = make_node_config(node)
        node_cfg.edges = obj.all_edges[node_name]
        cfg.dag[node_name] = node_cfg
    return cfg
