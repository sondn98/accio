from pydantic import BaseModel
from typing import Callable, List, Set

from datagen.models import GeneratorConfig


class CondMatcher(BaseModel):
    deps: Set[str]
    generator_config: GeneratorConfig
    evaluator: Callable


class CondNode(BaseModel):
    field_name: str
    matchers: List[CondMatcher]
