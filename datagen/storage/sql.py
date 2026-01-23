from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Dict, Iterable, List, Type, TypeVar

from sqlalchemy import ColumnExpressionArgument, Executable, create_engine, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.pool import StaticPool

T = TypeVar("T", bound=DeclarativeBase)


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


class SqlLite(SQLCli):
    def __init__(self):
        self._engine = create_engine(url="sqlite:///:memory:", poolclass=StaticPool)

    def create_table(self, table: Type[DeclarativeBase]):
        return table.metadata.create_all(self._engine)

    @property
    def _execute(self):
        def do_execute(stmt: Executable, *args, **kwargs):
            with self._engine.begin() as conn:
                return conn.execute(stmt, *args, **kwargs)

        return do_execute

    def insert(self, item: T):
        with Session(self._engine) as session:
            session.add(item)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()

    def update(self, table: Type[T], *where_clauses: ColumnExpressionArgument[bool], **column_values_mapping):
        upd = update(table).where(*where_clauses).values(**column_values_mapping)
        self._execute(upd)

    def select(
        self,
        table: Type[T],
        *where_clauses: ColumnExpressionArgument[bool],
        batch_size: int = 100,
        sort_col: str = None,
    ) -> Iterable[List[T]]:
        sel = select(table).where(*where_clauses)
        if sort_col:
            sel = sel.order_by(sort_col)
        cursor = self._execute(sel)
        while batch := cursor.fetchmany(batch_size):
            yield batch

    def delete(self, table: Type[T], *where_clauses: ColumnExpressionArgument[bool]):
        dlt = delete(table).where(*where_clauses)
        self._execute(dlt)

    def count(self, table: Type[T], *where_clauses: ColumnExpressionArgument[bool]):
        cnt = select(func.count()).select_from(table).where(*where_clauses)
        return self._execute(cnt).scalar_one()
