from pydantic import BaseModel
from models.condition import CondMatcher
from typing import Dict


class Iteration(BaseModel):
    idx: int
    ordered_field_cond_matchers: Dict[str, CondMatcher]