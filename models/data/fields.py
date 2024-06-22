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
    params: Dict[str, Any]


class BaseField(BaseModel):
    alias: str = None
    type: DataType
    condition: List[Condition] = None
    params: Dict[str, Any] = None
