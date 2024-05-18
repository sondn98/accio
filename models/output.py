from typing import Any, Dict
from pydantic import BaseModel
from enum import Enum


class OutputType(str, Enum):
    CSV = 'csv'
    JSON = 'json'


class Output(BaseModel):
    kind: OutputType
    params: Dict[str, Any]
