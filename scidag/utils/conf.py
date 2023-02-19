import inspect
from dataclasses import dataclass
from typing import Any, Callable, Type

import hydra_zen as hz
from omegaconf import OmegaConf

__all__ = ["make_node_config"]

AnyCallable = Type[Callable[..., Any]]


@dataclass
class CallableConfig:
    callable: type
    values: dict[str, str] | None = None


def make_node_config(obj: AnyCallable) -> CallableConfig:
    obj_cfg = OmegaConf.structured(
        hz.builds(obj, populate_full_signature=True, zen_partial=True)
    )
    sig = inspect.signature(obj)
    values = {}
    for param_name, param in sig.parameters.items():
        if param.default is inspect.Signature.empty:
            param_type = (
                param.annotation if param.annotation is not inspect._empty else None
            )
            values[param_name] = param_type

    return CallableConfig(obj_cfg, values=values)


if __name__ == "__main__":

    def my_func(a: Any, b: int, mode: str = "sum", dummy: str = "hi") -> int:
        return a + b

    func_cfg = make_node_config(my_func)
    print(func_cfg)

    class MyClass:
        def __init__(self, mode: str = "sum", dummy: str = "hi") -> None:
            self.mode = mode
            self.dummy = dummy

        def __call__(self, a: int, b: int) -> int:
            return a + b

    class_cfg = make_node_config(MyClass)
    print(class_cfg)
