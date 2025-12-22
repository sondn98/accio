from abc import ABC, abstractmethod
from typing import Callable

from pydantic import BaseModel

from analysis.plan import BaseFieldGraph
from datagen.generators import find_generator
from datagen.items import Item
from datagen.storage.engine import StorageEngine
from datagen.write.writer import WriterFactory
from models.config import Dataset


class Coordinator(ABC):
    @abstractmethod
    def initialize(self, *args, **kwargs):
        """
        Initialize the coordinator
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def materialize(self, *args, **kwargs):
        """
        Generate data and store it
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def export(self, *args, **kwargs):
        """
        Write to outputs
        :return:
        """
        pass


class BaseCoordinator(Coordinator):
    def __init__(self, dataset: Dataset, storage: StorageEngine, writer_factory: WriterFactory):
        self.storage = storage
        self.dataset = dataset
        self.writer = writer_factory.new_instance(*dataset.output)
        self._graph = BaseFieldGraph(self.dataset.name, self.dataset.columns)

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

    def materialize(self, max_attempts: int = 10):
        population = self.dataset.size
        attempts = max_attempts
        while remaining := population - self.storage.count(self.dataset.name):
            if not attempts:
                break
            attempts -= 1
            for i in range(remaining):
                item = self._do_generate()
                self.storage.store(self.dataset.name, item)

    def export(self, deserializer: Callable[..., BaseModel] = Item.deserialize, *args, **kwargs):
        for batch in self.storage.stream(self.dataset.name, *args, **kwargs):
            self.writer.write_batch(batch)  # type: ignore
