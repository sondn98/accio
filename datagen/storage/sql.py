from typing import Any, Callable, Dict, Iterator, List

from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import Row
from abc import ABC, abstractmethod
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    BLOB,
    BigInteger,
    select,
    update,
    delete,
    func,
    Executable,
    ColumnExpressionArgument,
)


def storage_table(metadata):
    return Table(
        "storage",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("dataset", String, nullable=False),
        Column("data", BLOB, nullable=False),
        Column("order", BigInteger, nullable=True),
    )


class SQLCli(ABC):
    @abstractmethod
    def select(self, *args, **kwargs):
        """
        Read data
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def insert(self, *args, **kwargs):
        """
        Insert rows
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Update rows
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Delete rows
        :param args:
        :param kwargs:
        :return:
        """
        pass


class BaseSQLCli(SQLCli):
    def __init__(self):
        self._engine = create_engine(url="sqlite:///:memory:", poolclass=StaticPool)
        self._metadata = MetaData()

    def initialize(self):
        self._metadata.create_all(self._engine)

    def register_table(self, table_creator: Callable[[MetaData], Table]) -> Table:
        return table_creator(self._metadata)

    @property
    def meta(self):
        return self._metadata

    @property
    def _execute(self):
        def do_execute(stmt: Executable, *args, **kwargs):
            with self._engine.begin() as conn:
                return conn.execute(stmt, *args, **kwargs)

        return do_execute

    def insert(self, table: Table, *values: Dict[str, Any]):
        from sqlalchemy.dialects.sqlite import insert

        ins = insert(table).values(*values).on_conflict_do_nothing()
        self._execute(ins)

    def update(self, table: Table, *where_clauses: ColumnExpressionArgument[bool], **column_values_mapping):
        upd = update(table).where(*where_clauses).values(**column_values_mapping)
        self._execute(upd)

    def select(
        self, table: Table, *where_clauses: ColumnExpressionArgument[bool], batch_size: int = 100, sort_col: str = None
    ) -> Iterator[List[Row]]:
        sel = select(table).where(*where_clauses)
        if sort_col:
            sel = sel.order_by(sort_col)
        cursor = self._execute(sel)
        while batch := cursor.fetchmany(batch_size):
            yield batch

    def delete(self, table: Table, *where_clauses: ColumnExpressionArgument[bool]):
        dlt = delete(table).where(*where_clauses)
        self._execute(dlt)

    def count(self, table: Table, *where_clauses: ColumnExpressionArgument[bool]):
        cnt = select(func.count()).select_from(table).where(*where_clauses)
        return self._execute(cnt).scalar_one()
