import math

from scidag import DAG, Node, StartNode


def my_sum(x, y) -> float:
    return x + y


def double(x) -> float:
    return x * 2


def cos(x) -> float:
    return math.cosh(x)


def pow(x, base: int = 2) -> float:
    return pow(x, base)


def test_dag_from_scratch():
    import random

    dag = DAG()

    dag.add(StartNode("node_a", random.random))
    dag.add(Node("node_b", double))
    dag.add(Node("node_c", cos))
    dag.add(Node("node_d", my_sum))

    # FIXME
    dag.connect("node_a", "node_b", "x")
    dag.connect("node_a", "node_c", "x")
    dag.connect("node_b", "node_d", "x")
    dag.connect("node_c", "node_d", "y")
    dag.run()
