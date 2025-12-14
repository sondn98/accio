from sqlalchemy import Table, Column, String, BLOB, BigInteger, Index


def test_create_table(sql_cli):
    storage = Table(
        "storage",
        sql_cli.meta,
        Column("id", BigInteger, primary_key=True),
        Column("dataset", String, nullable=False),
        Column("data", BLOB, nullable=False),
        Column("order", BigInteger, nullable=True),
    )
    Index("idx_storage_dataset", storage.c.dataset)

    sql_cli.initialize()
