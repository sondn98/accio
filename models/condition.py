from pydantic import BaseModel
from models.config import DataType
from typing import Any, Callable, Dict, List, Set


class CondMatcher(BaseModel):
    deps: Set[str]
    generator_params: Dict[str, Any]
    evaluator: Callable


class CondNode(BaseModel):
    field_name: str
    dtype: DataType
    matchers: List[CondMatcher]
