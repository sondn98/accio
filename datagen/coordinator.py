from abc import ABC, abstractmethod
from collections import namedtuple
from graphlib import TopologicalSorter
from typing import Callable, Dict, List

from pydantic import BaseModel
from tqdm import tqdm

from analysis.parse import parse
from datagen.generators import find_generator
from datagen.items import Item
from datagen.storage.engine import StorageEngine
from datagen.write.writer import WriterFactory
from models.config import Dataset
from models.types import merge
from utils.log import get_logger

logger = get_logger(__name__)


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


Rule = namedtuple("Rule", ["evaluator", "gen_spec"])


class BaseCoordinator(Coordinator):
    def __init__(self, name: str, storage: StorageEngine, writer_factory: WriterFactory):
        self.name = name
        self.storage = storage
        self.writer_factory = writer_factory
        self.topo: List[str] = []
        self.gen_context: Dict[str, List[Rule]] = {}
        self.outputs: List[str] = []
        self.ready = False
        self.item_cls = None

    def initialize(self, dataset: Dataset, *args, **kwargs):
        if not dataset.output:
            self.ready = False
            return
        self.storage.initialize()
        self.item_cls = Item.from_config(dataset)
        sorter = TopologicalSorter()
        normalize_id = lambda x: (x if x.startswith(f"{dataset.name}.") else f"{dataset.name}.{x}")

        for column in dataset.columns:
            dependencies = set()
            node_id = f"{dataset.name}.{column.name}"
            default_spec = column.spec
            rules = []
            for condition in column.conditions:
                # Parse condition
                root, predecessors = parse(condition.predicate)
                gen_config = merge(default_spec, condition.spec)

                # Build rule
                rule = Rule(evaluator=root, gen_spec=gen_config)
                rules.append(rule)

                # Add node predecessors for topo-sort
                normalized_predecessors = [normalize_id(p) for p in predecessors]
                dependencies.update(normalized_predecessors)

            # Fallback to default if there's no satisfied condition
            default_rule = Rule(evaluator=parse("true")[0], gen_spec=default_spec)
            rules.append(default_rule)

            self.gen_context[node_id] = rules
            sorter.add(node_id, *dependencies)

        self.topo = list(sorter.static_order())
        self.outputs = dataset.output
        self.ready = True

    def _do_generate(self) -> Item:
        import copy

        data = {}
        for node_id in self.topo:
            values = copy.deepcopy(data)
            for rule in self.gen_context[node_id]:
                evaluator = rule.evaluator
                if evaluator.evaluate(**values):
                    generator = find_generator(rule.gen_spec)
                    data[node_id] = generator.generate()
                    break
        return self.item_cls.model_validate(data)

    def materialize(self, size, max_attempts: int = 10):
        if not self.ready:
            return
        attempts = max_attempts
        while remaining := size - self.storage.count(self.name):
            print("Attempts: %d, remaining: %d", attempts, remaining)
            if not attempts:
                break
            attempts -= 1
            for _ in tqdm(range(remaining)):
                item = self._do_generate()
                self.storage.store(self.name, item)

    def export(self, *args, **kwargs):
        deserializer = self.item_cls.deserialize
        writer = self.writer_factory.new_instance(self.outputs)
        for batch in self.storage.stream(self.name, deser=deserializer, *args, **kwargs):
            writer.write_batch(batch, item_cls=self.item_cls)  # type: ignore
