from typing import Dict
from models.data.fields import BaseField
from pydantic import BaseModel


class Dataset(BaseModel):
    alias: str = None
    population: int
    columns: Dict[str, BaseField]
