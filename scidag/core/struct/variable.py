import inspect
from dataclasses import dataclass
from functools import cache
from typing import Any, Self

from scidag.utils.configurable import VariableConfig, make_variables_config


@dataclass
class Variable:
    type: str
    _value: Any | None = None

    @classmethod
    def from_config(cls, cfg) -> Self:
        return build_variable(cfg)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        # TODO: Fix this
        # if type(value) != self.type:
        #     raise TypeError(
        #         f"Type of this variable should be {self.type} not {type(value)}"
        # )
        self._value = value


def build_variable(cfg: VariableConfig) -> Variable:
    var = Variable(type=cfg.type)
    var.value = cfg.value
    return var


def build_io(obj) -> tuple[dict[str, Variable] | None, Variable]:
    sig = inspect.signature(obj)
    inputs = {}
    for param_name, param in sig.parameters.items():
        if param.default is inspect.Signature.empty:
            param_type = (
                param.annotation if param.annotation is not inspect._empty else None
            )
            inputs[param_name] = Variable(type=str(param_type))
    output = Variable(str(sig.return_annotation))
    if len(inputs) == 0:
        return None, output
    return inputs, output
