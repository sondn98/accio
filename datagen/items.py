from typing import List, Optional

from pydantic import BaseModel, Field, create_model

from models.config import Dataset
from models.types import TYPE_MAP


class ItemBuilder:
    def __init__(self):
        self.datasets: List[Dataset] = []
        pass

    def with_dataset(self, dataset: Dataset):
        self.datasets.append(dataset)


class Item(BaseModel):
    model_config = {"populate_by_name": True}

    @classmethod
    def from_config(cls, dataset: Dataset, *args, **kwargs):
        def _dtype(type_str: str, optional: bool):
            python_dtype = TYPE_MAP[type_str]
            return Optional[python_dtype] if optional else python_dtype

        fields = {
            f"{dataset.name}.{column.name}": (_dtype(column.spec.type, True), Field(..., alias=column.name))
            for column in dataset.columns
        }
        return create_model(dataset.name, __base__=cls, **fields)

    def serialize(self, *args, **kwargs):
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes, *args, **kwargs) -> "Item":
        return cls.model_validate_json(data)
