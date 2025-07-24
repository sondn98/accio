from datagen.storage.core import BaseSQLCli, FieldDef
from datagen.models import Dataset, Column
from datagen.generate import DataGen


def define_column(column_name, column: Column) -> FieldDef:
    spec = column.spec
    return FieldDef(
        name=column_name, dtype=spec.type, nullable=spec.nullable, unique=spec.unique, is_pkey=False, default=None
    )


class Engine:
    def __init__(self, ds_name: str, ds: Dataset, sql_cli: BaseSQLCli):
        self.sql_cli = sql_cli
        self.ds_name = ds_name
        self.ds = ds
        self.data_gen = DataGen(ds)

    def initialize(self):
        self.sql_cli.create_table(
            table_name=self.ds_name,
            field_def=[define_column(col_name, col) for col_name, col in self.ds.fields.items()],
        )

    def run(self):
        items = self.data_gen.generate()
        self.sql_cli.insert(self.ds_name, *items)
