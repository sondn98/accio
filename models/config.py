from pydantic import BaseModel
from typing import Any, Dict, List
from enum import Enum


class DataType(str, Enum):
    INTEGER = "integer"
    REAL = "real"
    TEXT = "text"
    BOOLEAN = "boolean"
    DATE = "date"
    DATE_TIME = "datetime"


class Condition(BaseModel):
    predicate: str
    params: Dict[str, Any] = dict()


class BaseField(BaseModel):
    alias: str = None
    type: DataType
    conditions: List[Condition] = None
    params: Dict[str, Any] = None


class Dataset(BaseModel):
    alias: str = None
    population: int
    output: List[str]
    fields: Dict[str, BaseField]


class OutputType(str, Enum):
    CSV = "csv"
    JSON = "json"


class Output(BaseModel):
    format: OutputType
    params: Dict[str, Any]


class Configuration(BaseModel):
    datasets: Dict[str, Dataset]
    outputs: Dict[str, Output]
    seed: int = None
