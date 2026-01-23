from abc import ABC, abstractmethod
from uuid import uuid4

from datagen.coordinator import BaseCoordinator
from datagen.storage.engine import InMemorySQLEngine
from datagen.write.writer import BaseWriterFactory
from models.config import Configuration


class Executor(ABC):
    @abstractmethod
    def run(self):
        pass


class SingleDatasetExecutor(Executor):
    def __init__(self, config: Configuration):
        self.dataset = config.datasets[0]
        self.writer_factory = BaseWriterFactory(*config.outputs)
        self.storage = InMemorySQLEngine()

    def run(self):
        coordinator_name = str(uuid4())
        coordinator = BaseCoordinator(coordinator_name, self.storage, self.writer_factory)
        coordinator.initialize(self.dataset)

        # Generate data
        coordinator.materialize(self.dataset.size)
        coordinator.export()
