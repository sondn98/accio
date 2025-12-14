from abc import ABC, abstractmethod
from itertools import chain
from typing import Generator, Iterable, List, TypeVar

from datagen.storage.repository import Storage
from datagen.storage.serde import Serializable
from datagen.storage.sql import SqlLite

T = TypeVar("T")


class StorageEngine(ABC):
    @abstractmethod
    def initialize(self, *args, **kwargs):
        """
        Initialize engine
        """
        pass

    @abstractmethod
    def store(self, dataset: str, item: Serializable, *args, **kwargs):
        """
        Store an item
        :param dataset: Dataset that the item belongs to
        :param item: Stored item must be serializable
        """
        pass

    @abstractmethod
    def count(self, dataset: str, *args, **kwargs):
        """
        Count the number of items that belong to a dataset
        :param dataset: Dataset on which this function performs a count
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def stream(self, dataset: str, *args, **kwargs) -> Iterable[List[Serializable]]:
        """
        Stream items from a dataset
        :param dataset: Dataset to stream data
        :param args:
        :param kwargs:
        :return:
        """
        pass


class InMemorySQLEngine(StorageEngine):
    def __init__(self):
        self.cli = SqlLite()

    def initialize(self):
        self.cli.create_table(Storage)

    def store(self, dataset: str, item: Serializable, **kwargs):
        self.cli.insert(
            Storage,
            {
                "dataset": dataset,
                "data": item.serialize(),
            },
        )

    def stream(self, dataset: str, *args, **kwargs) -> Iterable[List[Serializable]]:
        for batch in self.cli.select(Storage, **kwargs):
            yield [
                Serializable.deserialize(item.data)
                for item in batch
            ]

    def count(self, dataset: str, **kwargs):
        return self.cli.count(self._storage_table, Storage.dataset == dataset)  # type: ignore
