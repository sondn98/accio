from networkx import DiGraph
from typing import Dict, List, Set
from analyzers.conditions import parse
from models.condition import CondMatcher, CondNode
from models.config import BaseField


def field_to_graph_node(field_name: str, field: BaseField) -> CondNode:
    conditions = field.conditions
    matchers = []
    if conditions:
        for cond in conditions:
            mat = parse(cond)
            matchers.append(mat)

    return CondNode(field_name=field_name, matchers=matchers)


def deps(matchers: List[CondMatcher]) -> Set[str]:
    field_deps: Set[str] = set()
    for mat in matchers:
        mat_deps = mat.deps
        field_deps.update(mat_deps)

    return field_deps


def field_graph(dataset: str, fields: Dict[str, BaseField]) -> DiGraph:
    G = DiGraph()
    for field_name, field_spec in fields.items():
        node_name = f"{dataset}.{field_name}"
        node_data = field_to_graph_node(field_name, field_spec)
        node_deps = deps(node_data.matchers)

        G.add_node(node_name, data=node_data)
        for dep in node_deps:
            G.add_edge(dep, node_name)

    return G
