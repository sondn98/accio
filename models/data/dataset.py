from typing import Dict, List
from models.data.fields import BaseField
from pydantic import BaseModel


class Dataset(BaseModel):
    alias: str = None
    population: int
    output: List[str]
    fields: Dict[str, BaseField]
