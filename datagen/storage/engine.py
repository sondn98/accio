from typing import Generic, Iterable, TypeVar, Type
from datagen.storage.sql import BaseSQLCli
from datagen.storage.serde import Serializable
from itertools import chain
from abc import ABC, abstractmethod
from sqlalchemy import (
    Table,
    Index,
    Column,
    String,
    BLOB,
    BigInteger,
)


T = TypeVar("T")


class StorageEngine(Generic[T], ABC):
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
    def stream(self, dataset: str, *args, **kwargs) -> Iterable[Serializable]:
        """
        Stream items from a dataset
        :param dataset: Dataset to stream data
        :param args:
        :param kwargs:
        :return:
        """
        pass


def storage_table(metadata):
    storage = Table(
        "storage",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("dataset", String, nullable=False),
        Column("data", BLOB, nullable=False),
        Column("order", BigInteger, nullable=True),
    )
    Index("idx_storage_dataset", storage.c.dataset)
    return storage


class InMemorySQLEngine(StorageEngine[T]):
    def __init__(self):
        self.cli = BaseSQLCli()
        self._storage_table = self.cli.register_table(storage_table)

    def initialize(self):
        self.cli.initialize()

    def store(self, dataset: str, item: Serializable, **kwargs):
        self.cli.insert(
            self._storage_table,
            {
                "dataset": dataset,
                "data": item.serialize(),
            },
        )

    def stream(self, dataset: str, **kwargs) -> Iterable[Serializable]:
        while batches := self.cli.select(self._storage_table, **kwargs):
            for batch in batches:
                yield chain.from_iterable(batch)

    def count(self, dataset: str):
        return self.cli.count(self._storage_table, self._storage_table.c.dataset == dataset)  # type: ignore
