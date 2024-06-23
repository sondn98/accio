from pydantic import BaseModel
from typing import Callable, Dict, Set


class Evaluator(BaseModel):
    deps: Set[str]
    evaluate: Callable


class FieldsEvaluator(BaseModel):
    dataset: str
    fields_eval: Dict[str, Evaluator]
