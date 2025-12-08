from abc import ABC, abstractmethod
from datagen.generators import find_generator
from datagen.storage.engine import StorageEngine
from datagen.items import SqlCompatibleItem as Item
from analysis.plan import BaseFieldGraph
from models.config import Dataset


class GenerativeEngine(ABC):
    @abstractmethod
    def initialize(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def materialize(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def export(self, *args, **kwargs):
        """

        :return:
        """
        pass


class BaseGenerativeEngine(GenerativeEngine):
    def __init__(self, dataset: Dataset, storage: StorageEngine):
        self.storage = storage
        self.dataset = dataset
        self._graph = BaseFieldGraph(dataset.name, dataset.columns)

    def initialize(self, *args, **kwargs):
        self.storage.initialize()

    def _do_generate(self) -> Item:
        gen_value = lambda cfg: find_generator(cfg).generate()

        data = {}
        for node_id in self._graph.topo():
            node_data = self._graph.node_data(node_id)
            index = node_data["index"]
            for ctx in node_data["contexts"]:
                if ctx.evaluator(**data):
                    data[node_id] = gen_value(ctx.generator_config)
                    break
            else:
                field_spec = self.dataset.columns[index].spec
                data[node_id] = gen_value(field_spec)

        return Item.model_validate(data)

    def materialize(self):
        for i in range(self.dataset.size):
            item = self._do_generate()
            self.storage.store(self.dataset.name, item)

    def export(self, *args, **kwargs):
        pass
