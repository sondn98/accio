import yaml
from typing import Annotated, List, Optional, Union
from models.write.database import JDBCWriterConfig
from models.write.files import FileWriterConfig
from models.types import DateConfig, DateTimeConfig, BoolConfig, IntConfig, RealConfig, TextConfig
from pydantic import BaseModel, Field


GeneratorConfig = Annotated[
    Union[DateConfig, DateTimeConfig, BoolConfig, IntConfig, RealConfig, TextConfig], Field(discriminator="type")
]

WriterConfig = Annotated[Union[JDBCWriterConfig, FileWriterConfig], "type"]


class Condition(BaseModel):
    predicate: str
    spec: GeneratorConfig


class Column(BaseModel):
    name: str
    spec: GeneratorConfig
    conditions: Optional[List[Condition]] = None


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
