from pydantic import BaseModel
from typing import Dict
from models.data.dataset import Dataset
from models.output import Output


class Configuration(BaseModel):
    datasets: Dict[str, Dataset]
    outputs: Dict[str, Output]
