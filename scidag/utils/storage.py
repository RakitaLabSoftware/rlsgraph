from dataclasses import dataclass, field
from functools import cache
from typing import Any, Self

from scidag.utils.conf import CallableConfig


@dataclass
class Value:
    name: str
    type: str
    _value: Any = field(init=False)

    @property
    @cache
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        if type(value) != self.type:
            raise TypeError(
                f"Type of {self.name} should be {self.type} not {type(value)}"
            )
        self.value = value


class DataStorage:
    def __init__(
        self,
        nodes: dict[str, Any] | None = None,
        edges: dict[str, dict[str, str]] | None = None,
    ) -> None:
        self.nodes: dict[str, Any] = nodes if nodes is not None else {}
        self.edges: dict[str, dict[str, str]] = edges if edges is not None else {}

    def add_node(self, node_name: str, node) -> None:
        if node_name in self.nodes.keys():
            raise KeyError(
                f"This node_name = {node_name} is already reserved for {self.nodes[node_name]}"
            )
        if node in self.nodes.values():
            raise KeyError(
                f"This node = {node} is already registered under different name."
            )
        self.nodes[node_name] = node

    def add_edge(self, u_node: str, v_node: str, target_variable: str) -> None:
        if self.edges[u_node] is None:
            self.edges[u_node]
        self.edges[u_node][v_node] = target_variable

    def remove_node(self, u_node: str) -> None:
        if not self.nodes[u_node]:
            KeyError(f"Node with name {u_node} not stored in this dag.")
        del self.nodes[u_node]

    def remove_edge(self, u_node: str, v_node: str) -> None:
        if not (self.nodes[u_node] or self.nodes[v_node]):
            KeyError(f"Node with name {u_node} or {v_node} not stored in this dag.")
        self.nodes[u_node].remove(v_node)

    async def notify(self) -> None:
        # for observers in observer notify
        self.event.set()


class Data:
    def __init__(self, values: dict[str, Value]) -> None:
        self.values = values
        self._storage = None

    @classmethod
    def from_config(cls, cfg: CallableConfig) -> Self:
        values = {}
        if cfg.values is None:
            return cls(values=values)
        for value_name, value_type in cfg.values.items():
            values[value_name] = Value(value_name, value_type)
        return cls(values)

    @property
    def storage(self) -> DataStorage:
        if self._storage is None:
            raise NameError(f"Storage is not set for current node")
        return self._storage

    @storage.setter
    def storage(self, storage: DataStorage) -> None:
        self._storage = storage

    @property
    def _check_values(self) -> bool:
        return all(value._value is not None for value in self.values.values())

    def update(self, value_name: str, value: Any) -> None:
        # update value in storage
        if self._check_values:
            self.storage.notify()
