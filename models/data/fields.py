from pydantic import BaseModel
from typing import Any, Dict
from enum import Enum


class Nullability(BaseModel):
    nullable: bool = True
    ratio: float = 0.5


class DataType(str, Enum):
    INTEGER = 'integer'
    REAL = 'real'
    TEXT = 'text'
    BOOLEAN = 'boolean'
    DATE = 'date'
    DATE_TIME = 'datetime'
    ARRAY = 'array'
    STRUCT = 'struct'


class ConditionType(str, Enum):
    UNIQUE = 'unique'
    REFER = 'refer'
    DEPEND = 'depend'


class Bound(BaseModel):
    const: Any = None
    high: Any = None
    low: Any = None


class Condition(BaseModel):
    kind: ConditionType
    params: Dict[str, Any]


class BaseField(BaseModel):
    alias: str = None
    kind: DataType
    dialect: str = None
    nullability: Nullability = Nullability()
    bound: Bound = None
    params: Dict[str, Any] = None
    condition: Condition = None
