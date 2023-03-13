from dataclasses import dataclass, field
from typing import Dict, List
from scidag.storage.base import Storage


@dataclass(slots=True)
class Edge:
    source: str
    target: str
    variable: str

    def to_config(self):
        pass


@dataclass(slots=True)
class Edges:
    storage: Storage = field(repr=False)
    adjacency_list: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, cfg, storage):
        # TODO make an adjacency list
        edges = {}
        for name, node in cfg.dag.items():
            edges[name] = node.edges
        return Edges(storage, edges)

    def add(self, source: str, target: str, variable: str) -> None:
        self.adjacency_list.setdefault(source, []).append(target + "." + variable)
        self.adjacency_list.setdefault(target, [])

    def remove(self, source: str, target: str, variable: str) -> None:
        if target in self.adjacency_list.get(source, []):
            self.adjacency_list[source].remove(target + "." + variable)

    def to_adjacency_matrix(self) -> List[List[int]]:
        nodes = sorted(self.adjacency_list.keys())
        node_indices = {node: i for i, node in enumerate(nodes)}
        adj_matrix = [[0] * len(nodes) for _ in range(len(nodes))]
        for source, targets in self.adjacency_list.items():
            for target in targets:
                source_idx = node_indices[source]
                target_idx = node_indices[target]
                adj_matrix[source_idx][target_idx] = 1
        return adj_matrix

    def topological_sort(self) -> List[str]:
        visited = set()
        result = []

        def dfs(node: str):
            visited.add(node)
            for neighbor in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            result.append(node)

        for node in self.adjacency_list.keys():
            if node not in visited:
                dfs(node)

        return result[::-1]

    def get_children(self, node_name: str):
        children = []
        for node, neighbors in self.adjacency_list.items():
            if node == node_name:
                children = [n.split(".")[0] for n in neighbors]
                break
        return children
