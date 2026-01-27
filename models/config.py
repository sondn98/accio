from typing import Annotated, List, Optional, Union

import yaml
from pydantic import BaseModel

from models.types import GeneratorConfig
from models.write.database import JDBCWriterConfig
from models.write.files import FileWriterConfig

WriterConfig = Annotated[Union[JDBCWriterConfig, FileWriterConfig], "type"]


class Condition(BaseModel):
    predicate: str
    generate: GeneratorConfig


class Column(BaseModel):
    name: str
    generate: GeneratorConfig
    conditions: Optional[List[Condition]] = []


class Dataset(BaseModel):
    name: str
    size: int
    output: List[str]
    columns: List[Column]


class Configuration(BaseModel):
    datasets: List[Dataset]
    outputs: List[WriterConfig]
    seed: Optional[int] = None


def read_config(path: str) -> Configuration:
    with open(path, "r") as f:
        try:
            raw_cf = yaml.safe_load(f)
            conf = Configuration.model_validate(raw_cf)
            return conf
        except Exception as e:
            raise Exception(f"Can not load yaml config file at path {path}", e)
