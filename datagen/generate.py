from typing import Any, Dict, Generator
from datagen.generators import find_generator
from analyzers.plan import field_graph
from analyzers.travel import travel
from datagen.models import Dataset, GeneratorConfig


Item = Dict[str, Any]


class DataGen:
    def __init__(self, dataset: Dataset):
        self._fields = dataset.fields
        self._size = dataset.size
        cond_graph = field_graph(self._fields)
        node_visited_ordered = travel(cond_graph)
        self._node_matchers = [(node, cond_graph.nodes[node].matchers) for node in node_visited_ordered]

    @staticmethod
    def _generate_single_value(cfg: GeneratorConfig, **kwargs):
        generator = find_generator(cfg, **kwargs)
        return generator.generate()

    def generate(self) -> Generator[Item]:
        def _do_generate() -> Item:
            data: Dict[str, Any] = {}

            for node, matchers in self._node_matchers:
                satisfied = False
                for matcher in matchers:
                    satisfied = matcher.evaluator(**data)
                    if satisfied:
                        data[node] = self._generate_single_value(matcher.generator_config)
                        break
                if not satisfied:
                    field_spec = self._fields[node].spec
                    data[node] = self._generate_single_value(field_spec)

            return data

        for i in range(self._size):
            yield _do_generate()
