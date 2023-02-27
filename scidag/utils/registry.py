from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator

from .types import AnyCallable

__all__ = ["Registry"]


@dataclass(frozen=True, slots=True)
class Registry:
    name: str
    obj_map: dict[str, AnyCallable] = field(init=False, default_factory=dict)

    def _reg(self, name: str, factory: AnyCallable) -> None:
        try:
            self.obj_map[name] = factory
        except KeyError as e:
            raise KeyError(e)

    def register(self, factory: AnyCallable | None = None) -> Any:
        """
        Add an object to current registry

        Parameters
        ----------
        obj : Any, optional
            Object to be registered, if None, then used as decorator

        Returns
        -------
        Callable[..., Any]|None
            Returns either the decorator of a function or None
        """
        if factory is None:
            # used as a decorator
            def deco(func_or_class: Any) -> Any:
                name = func_or_class.name
                self._reg(name, func_or_class)
                return func_or_class

            return deco

        # used as a function call
        name = factory.name
        self._reg(name, factory)

    def get(self, key: str) -> AnyCallable:
        r"""Get :class:`FactoryType` by key

        Args:
            key (str): key in

        Returns:
            FactoryType: _description_
        """
        ret = self.obj_map.get(key)
        if ret is None:
            raise KeyError(
                "No object named '{}' found in '{}' registry!".format(key, self.name)
            )
        return ret

    def list(self) -> Iterable[str]:
        """Returns list with names of all registered items."""
        return self.obj_map.keys()

    def __str__(self) -> str:
        """Returns a string of registered items."""
        return self.list().__str__()

    def __repr__(self) -> str:
        """Returns a string representation of registered items."""
        return self.list().__str__()

    def __len__(self) -> int:
        """Returns length of registered items."""
        return len(self.obj_map)

    def __getitem__(self, name: str) -> Any:
        """Returns a value from the registry by name."""
        return self.get(name)

    def __iter__(self) -> Iterator[str]:
        """Iterates over all registered items."""
        return self.obj_map.__iter__()

    def __contains__(self, name: str) -> bool:
        """Check if a particular name was registered."""
        return self.obj_map.__contains__(name)

    def __delitem__(self, name: str) -> None:
        """Removes object by giving name."""
        self.obj_map.pop(name)
