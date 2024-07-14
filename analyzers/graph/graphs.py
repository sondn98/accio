from abc import ABC, abstractmethod
from queue import Queue

from networkx import DiGraph
from typing import List


def bfs_travel(G: DiGraph, base_nodes: List[str]) -> List[str]:
    visited_nodes = []

    visited = {node: False for node in G.nodes}
    visit_queue = Queue(maxsize=-1)
    for node in base_nodes:
        visit_queue.put(node)

    while not visit_queue.empty():
        node = visit_queue.get()
        if visited[node]:
            continue

        visited[node] = True
        visited_nodes.append(node)
        successors = G.successors(node)
        for s in successors:
            if not visited[s]:
                visit_queue.put(s)

    return visited_nodes


def bfs_from_sources(G: DiGraph) -> List[str]:
    source_nodes = [node for node, degree in G.in_degree() if degree == 0]
    visited = bfs_travel(G, source_nodes)

    return visited
