# import inspect
import inspect
import typing
from dataclasses import dataclass, field, make_dataclass
from typing import Any, Callable, Type

import hydra_zen as hz
from omegaconf import DictConfig, OmegaConf

__all__ = ["make_config"]

ClassOrFunc = Type[Callable[..., Any]] | Type[object]


@dataclass
class NodeConfig:
    _target_: str
    arguments: dict[str, Any] = field(default_factory=lambda: {"none": None})


class DynamicDataClassFactory:
    def __init__(
        self,
        obj: ClassOrFunc,
        override: dict[str, Any] | None = None,
    ):
        self.obj = obj
        if inspect.isfunction(obj):
            self.sig = inspect.signature(obj)
        elif inspect.isclass(obj):
            self.sig = inspect.signature(obj.__init__)
        else:
            raise ValueError("obj must be a function or a class")

    def create_dataclass(self):

        # Add fields for required parameters
        fields: list[Any] = [("_target_", Any, "path.to.module")]
        arguments: dict[str, Any] = {}
        for name, param in self.sig.parameters.items():
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                annotation = param.annotation
                if param.annotation == inspect._empty:  # ignore
                    annotation = Any

                if param.default == inspect._empty:
                    arguments[name] = str(param.annotation)  # ignore
                    continue
                else:
                    default = param.default

                fields.append((name, annotation, field(default=default)))
        fields.append(
            ("arguments", dict[str, str], field(default_factory=lambda: arguments))
        )
        if "kwargs" in self.sig.parameters:
            fields.append(("kwargs"))
        ret = make_dataclass("Config", fields=fields, bases=(NodeConfig,))
        return ret


def make_config(obj: ClassOrFunc):
    cfg = DynamicDataClassFactory(obj).create_dataclass()
    return cfg()


if __name__ == "__main__":

    def dummy(a: Any, b: int, mode: str = "sum", example: int = 43):
        if mode == "sum":
            return a + b

    # cfg = make_config(dummy)
    # print(cfg)
    # new = OmegaConf.structured(cfg)
    cfg = hz.builds(dummy, zen_partial=True, populate_full_signature=True)
    print(hz.to_yaml(cfg))
    dummy = hz.instantiate(cfg)
    val = dummy()
