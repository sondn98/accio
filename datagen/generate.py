from typing import Any, Dict, Generator
from datagen.generators import find_generator
from analyzers.plan import BaseFieldGraph
from datagen.models import Dataset, GeneratorConfig


Item = Dict[str, Any]


class DataGen:
    def __init__(self, dataset: Dataset):
        self._cols = {col.name: col for col in dataset.columns}
        self._size = dataset.size
        self._graph = BaseFieldGraph(dataset.name, dataset.columns)

    @staticmethod
    def _generate_single_value(cfg: GeneratorConfig, **kwargs):
        generator = find_generator(cfg, **kwargs)
        return generator.generate()

    def _do_generate(self) -> Item:
        data: Item = {}

        for node_id in self._graph.topo():
            satisfied = False
            for ctx in self._graph.node_data(node_id)["contexts"]:
                satisfied = ctx.evaluator(**data)
                if satisfied:
                    data[node_id] = self._generate_single_value(ctx.generator_config)
                    break
            if not satisfied:
                field_spec = self._cols[node_id].spec
                data[node_id] = self._generate_single_value(field_spec)

        return data

    def generate(self) -> Generator[Item]:
        for i in range(self._size):
            yield self._do_generate()
