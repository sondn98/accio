import csv
from typing import Iterable

from datagen.items import Item
from models.write.files import CSVSerde
from functools import partial
from pathlib import Path
from time import time_ns

def build_filename(filename_prefix: str = None):
    prefix = "" if not filename_prefix else f"{filename_prefix}"
    now_ns = time_ns() // 1_000
    return "-".join([prefix, now_ns]) + ".csv"


class CSVWriter:
    def __init__(self, folder: str, filename_prefix: str, serde: CSVSerde):
        self.serde = serde
        data_dir = Path(folder)
        data_dir.mkdir(parents=True, exist_ok=True)
        if any(data_dir.iterdir()):
            raise FileExistsError("Output dir is not empty")
        filename = partial(build_filename, filename_prefix)
        self.filepath_builder = lambda: Path(folder) / filename()


    def write_batch(self, rows: Iterable[Item], *args, **kwargs):
        csv_setting = self.serde.model_dump(
            include={"delimiter", "quotechar", "escapechar", "doublequote", "skipinitialspace", "lineterminator", "quoting"},
            exclude_none=True
        )
        encoding = self.serde.encoding

        with open(self.filepath_builder(), "w", newline="", encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=Item.model_fields.keys(), **csv_setting)
            if self.serde.header:
                writer.writeheader()

            for r in rows:
                writer.writerow(r.model_dump())
