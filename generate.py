from typing import Any, Dict, List, Generator
from generators import generator
from analyzers.graph import field_graph, travel
from models.config import Configuration, BaseField, Dataset


Item = Dict[str, Any]


class Synth:
    def __init__(self, ds: str, fields: Dict[str, BaseField]):
        cond_graph = field_graph(ds, fields)
        node_visited_ordered = travel(cond_graph)()
        self._node_matchers = [(node, cond_graph.nodes[node].matchers) for node in node_visited_ordered]
        self._fields = fields

    def gen_data(self) -> Item:
        data: Dict[str, Any] = {}
        for node, matchers in self._node_matchers:
            field_spec = self._fields[node]
            partial_gen = generator(field_spec.type)

            satisfied = False
            for mat in matchers:
                satisfied = mat.evaluator(**data)
                if satisfied:
                    params = mat.generator_params
                    dialect = params.get("dialect")
                    gen = partial_gen(**params)
                    value = gen.generate_with_dialect(dialect) if dialect else gen.generate()
                    data[node] = value
                    break
            if not satisfied:
                default_params = field_spec.params
                dialect = default_params.get("dialect")
                gen = partial_gen(**default_params)
                value = gen.generate_with_dialect(dialect) if dialect else gen.generate()
                data[node] = value

        return data

    def gen_data_batch(self, batch_size=1000) -> Generator[Item]:
        for i in range(batch_size):
            yield self.gen_data()
