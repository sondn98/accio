from pytest import fixture
from datagen.storage.sql import BaseSQLCli
from sqlalchemy import create_engine


@fixture
def sql_cli() -> BaseSQLCli:
    return BaseSQLCli()
