from typing import Annotated, List, Optional, Union
from datagen.generators.boolean import BoolConfig
from datagen.generators.datetime import DateConfig, DateTimeConfig
from datagen.generators.number import IntConfig, RealConfig
from datagen.generators.text import TextConfig
from datagen.write.models import JDBCWriterConfig
from datagen.write.csv import CSVWriterConfig
from pydantic import BaseModel, Field


GeneratorConfig = Annotated[
    Union[DateConfig, DateTimeConfig, BoolConfig, IntConfig, RealConfig, TextConfig], Field(discriminator="type")
]

WriterConfig = Annotated[Union[JDBCWriterConfig, CSVWriterConfig], "type"]


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
