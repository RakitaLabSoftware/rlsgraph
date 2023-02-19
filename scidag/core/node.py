import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable

from hydra.utils import instantiate
from omegaconf import DictConfig

from scidag.utils.conf import make_node_config
from scidag.utils.runnable import BaseElement
from scidag.utils.storage import Data


@dataclass
class NodeConfig:
    name: str
    content: Any
    dependencies: Any


class Node(BaseElement):
    """
    Node of DAG
    """

    def __init__(self, name: str, content: Callable[..., Any]) -> None:
        """
        Parameters
        ----------
        content : Any
            _description_
        """
        self.name = name
        self.content = content
        self.cfg = make_node_config(content)
        self.data = Data.from_config(self.cfg)

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> "Node":
        name = cfg.name
        content: Callable[..., Any] = instantiate(cfg.content)
        return Node(name=name, content=content)

    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """
        # TODO: Check if input values is same as specified in dependencies
        # await for value to be present in Storage
        await self.data.update(self)
        data = self.content(**self.data)
        self.data.update(self, data, name)


if __name__ == "__main__":

    # example function that will be run by the node
    def example_func(a, b, c=10):
        return a + b - c

    # example of class that we will use inside node.run()
    class ExampleClass:
        def __init__(self, c) -> None:
            self.c = c

        def __call__(self, a, b) -> Any:
            return a + b - self.c

    func = example_func
    func = ExampleClass.__call__()

    # loading dag from configuration file stored in path.yaml
    dag = DAG.from_config("path.yaml")

    # create
    new_node = Node(content=func)

    new_node.run()

    dag.append(
        new_node,
        dependecies={"parent": [old_node], "child": [child_node_1, child_node_2]},
    )

    ## Use case: Building From Scratch
    # instantiating dag
    dag = DAG()

    # create a new node (node_1)
    node_1 = Node(content=example_func)
    # append node to dag
    dag.append(node_1)

    # TODO: Create connect and disconnect functions
    # dag.connect(node1_name, node2_name.a, node3_name.b)
    # create a second node (node_2)
    node_2 = Node(content=ExampleClass)

    # append node_2 to node_1 inside a dag (will throw an error if nodes are not compatible)
    dag.append(node_2, dependecies={"parent": "node_1_id"})

    dag.extend(dag_2, **kwargs)
    #
    dag.get_nodes()
