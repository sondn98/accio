import yaml
from pydantic import BaseModel
from typing import List, Optional

from datagen.models import Dataset, WriterConfig


class Configuration(BaseModel):
    datasets: List[Dataset]
    outputs: List[WriterConfig]
    seed: Optional[int] = None


def read_config(path: str) -> Configuration:
    with open(path, "r") as f:
        try:
            raw_cf = yaml.safe_load(f)
            conf = Configuration.model_validate(raw_cf)
            return conf
        except Exception as e:
            raise Exception(f"Can not load yaml config file at path {path}", e)
