def topological_sort(nodes, dependencies) -> list[str]:
    """
    Sort nodes topologically
    """
    visited = set()
    sorted_nodes = []

    def visit(node_name: str):
        if node_name in visited:
            return
        visited.add(node_name)
        for dep in dependencies[node_name]:
            visit(dep)
        sorted_nodes.append(node_name)

    for node_name in nodes.keys():
        visit(node_name)

    return sorted_nodes[::-1]
