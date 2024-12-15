from queue import Queue

from networkx import DiGraph
from typing import List


def bfs_travel(g: DiGraph, base_nodes: List[str]) -> List[str]:
    visited_nodes = []

    visited = {node: False for node in g.nodes}
    visit_queue = Queue(maxsize=-1)
    for node in base_nodes:
        visit_queue.put(node)

    while not visit_queue.empty():
        node = visit_queue.get()
        if visited[node]:
            continue

        visited[node] = True
        visited_nodes.append(node)
        successors = g.successors(node)
        for s in successors:
            if not visited[s]:
                visit_queue.put(s)

    return visited_nodes


def bfs_from_sources(g: DiGraph) -> List[str]:
    source_nodes = [node for node, degree in g.in_degree() if degree == 0]
    visited = bfs_travel(g, source_nodes)

    return visited


def travel(g: DiGraph, traverse: str = "bfs") -> List[str]:
    if traverse == "bfs":
        return bfs_from_sources(g)
    else:
        raise ValueError(f"Traverse {traverse} has not yet supported")
