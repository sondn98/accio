import os
import time
import sqlite3
import threading

from typing import Any, Dict, List, Literal, Tuple
from collections import namedtuple
from utils.log import get_logger
from datagen.generate import Item


LOGGER = get_logger(__file__)
FieldDef = namedtuple("FieldDef", ["name", "dtype", "nullable", "unique", "is_pkey", "default"])


class BaseSQLCli:
    def __init__(self):
        self._local = threading.local()

    @property
    def _conn(self):
        # Check process ID to support process forking. If the process
        # ID changes, close the connection and update the process ID.
        local_pid = getattr(self._local, "pid", None)
        pid = os.getpid()
        if local_pid != pid:
            self._disconnect()
            self._local.pid = pid

        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = self._local.conn = sqlite3.connect(":memory:")

        return conn

    @property
    def _execute(self):
        conn = self._conn

        def _execute_with_retry(statement, *args, **kwargs):
            """Retry execution if database is locked"""
            start = time.time()
            retry_duration_secs = kwargs.get("retry_duration", 10)
            retry_delay_secs = kwargs.get("retry_duration", 1)
            execute_many = kwargs.get("execute_many", False)
            dry_run = kwargs.get("dry_run", False)
            while True:
                try:
                    if dry_run:
                        LOGGER.info(f"Execute: {statement}")
                        return statement
                    if execute_many:
                        return conn.executemany(statement, *args, **kwargs)
                    else:
                        return conn.execute(statement, *args, **kwargs)
                except sqlite3.OperationalError as exc:
                    if str(exc) != "database is locked":
                        raise
                    diff = time.time() - start
                    if diff > retry_duration_secs:
                        raise
                    time.sleep(retry_delay_secs)

        return _execute_with_retry

    def _disconnect(self):
        conn = getattr(self._local, "conn", None)

        if conn:
            conn.close()
            delattr(self._local, "conn")

    def create_table(
        self,
        table_name: str,
        field_def: List[FieldDef],
        temporary: bool = False,
        without_row_id: bool = False,
    ):
        temp = "TEMPORARY" if temporary else ""
        sql_create = f"CREATE {temp} TABLE IF NOT EXISTS {table_name}"

        def __column_def(
            field_name: str, field_type: str, nullable: bool = False, unique: bool = False, default: Any = None
        ):
            nullability_constraint = "NOT NULL" if not nullable else ""
            unique_constraint = "UNIQUE" if unique else ""
            default_value = f"DEFAULT {default}" if default else ""
            return f"{field_name} {field_type} {nullability_constraint} {unique_constraint} {default_value}"

        column_def = [
            __column_def(field.name, field.dtype, field.nullable, field.unique, field.default) for field in field_def
        ]
        sql_column_def = ",".join(column_def)

        key_cols = [field.name for field in field_def if field.is_pkey]
        sql_pkey = f"PRIMARY KEY ({",".join(key_cols)})" if key_cols else ""
        include_row_id = "WITHOUT ROWID" if without_row_id else ""

        sql_create_table = f"""
            {sql_create}
            {sql_column_def}
            {sql_pkey}
            {include_row_id}
        """

        self._execute(sql_create_table)

    def insert(self, table_name: str, cols: List[str] = None, *values: Tuple):
        cols = ",".join(cols)
        params = ",".join(["?"] * len(cols))
        sql_insert = f"""
            INSERT INTO {table_name} ({cols}) VALUES ({params})
        """
        self._execute(sql_insert, values, execute_many=True)

    def create_trigger(
        self,
        trigger_name: str,
        table_name: str,
        when: Literal["BEFORE", "AFTER", "INSTEAD OF"],
        op: Literal["DELETE", "INSERT", "UPDATE"],
        stmts: List[str],
    ):
        sql_create_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS {trigger_name}
            {when} {op} ON {table_name}
            FOR EACH ROW
            BEGIN
            {",".join(stmts)}
            END
        """
        self._execute(sql_create_trigger)

    def truncate(self, table_name):
        sql_truncate = f"""
            DELETE FROM {table_name}
        """

        self._execute(sql_truncate)
