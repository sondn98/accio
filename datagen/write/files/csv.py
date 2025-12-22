import csv
from functools import partial
from pathlib import Path
from time import time_ns
from typing import Iterable

from pydantic import BaseModel

from models.write.files import CSVSerde


def build_filename(filename_prefix: str = None):
    prefix = "data" if not filename_prefix else f"{filename_prefix}"
    now_ns = str(time_ns() // 1_000)
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

    def write_batch(self, rows: Iterable[BaseModel], *args, **kwargs):
        csv_setting = self.serde.model_dump(
            include={
                "delimiter",
                "quotechar",
                "escapechar",
                "doublequote",
                "skipinitialspace",
                "lineterminator",
                "quoting",
            },
            exclude_none=True,
        )
        encoding = self.serde.encoding
        item_cls = kwargs["item_cls"]

        with open(self.filepath_builder(), "w", newline="", encoding=encoding) as f:
            header = [f.alias for _, f in item_cls.model_fields.items()]
            writer = csv.DictWriter(f, fieldnames=header, **csv_setting)
            if self.serde.header:
                writer.writeheader()

            for r in rows:
                line = r.model_dump(by_alias=True)
                writer.writerow(line)
