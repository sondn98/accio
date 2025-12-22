from pytest import fixture
from sqlalchemy import create_engine

from datagen.storage.sql import SqlLite


@fixture
def sql_cli() -> SqlLite:
    return SqlLite()
