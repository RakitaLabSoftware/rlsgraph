# import inspect
from omegaconf import OmegaConf
from typing import Any, Callable, Type
import inspect
from dataclasses import dataclass, field, make_dataclass

__all__ = ["DynamicDataClassFactory"]


@dataclass
class NodeConfig:
    __target__: str
    arguments: dict[str, Any] = field(default_factory=lambda: {"none": None})


class DynamicDataClassFactory:
    def __init__(
        self,
        obj: Type[Callable[..., Any]] | Type[object],
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
        fields: list[Any] = [("__target__", Any, self.obj.__module__)]
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

        return make_dataclass("Config", fields=fields, bases=(NodeConfig,))


if __name__ == "__main__":

    def dummy(a: Any, b: int, mode: str = "sum"):
        if mode == "sum":
            return a + b

    Config = DynamicDataClassFactory(dummy).create_dataclass()
    cfg = Config()
    print("cfg:", type(cfg))
    new_cfg = OmegaConf.structured(cfg)
    new_cfg.mode = 10
    print(new_cfg)
