from dataclasses import dataclass
from typing import Any, Self
from scidag.utils.configurable import VariableConfig, make_variables_config
from functools import cache


@dataclass
class Variable:
    type: str
    value: Any | None = None

    @classmethod
    def from_config(cls, cfg) -> Self:
        return build_variable(cfg)

    # @property
    # def value(self) -> Any:
    #     return self._value

    # @value.setter
    # def value(self, value) -> None:
    #     if type(value) != self.type:
    #         raise TypeError(
    #             f"Type of this variable should be {self.type} not {type(value)}"
    #         )
    #     self.value = value


def build_variable(cfg: VariableConfig) -> Variable:
    return Variable(type=cfg.type, value=cfg.value)
