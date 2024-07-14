from models.config import Dataset
from analyzers.graph import field_graph, travel


class Iteration:
    def __init__(self):


class Context:
    def __init__(self, ds: str, ds_spec: Dataset):
        cond_graph = field_graph(ds, ds_spec.fields)
        node_visited_ordered = travel(cond_graph)()
        self._node_matchers = [cond_graph.nodes[node].matchers for node in node_visited_ordered]


