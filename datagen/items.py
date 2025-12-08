from typing import Optional
from datetime import date, datetime
from pydantic import Field, create_model, BaseModel
from models.config import Dataset
from models.types import TYPE_MAP


class Item(BaseModel):
    @classmethod
    def from_config(cls, dataset: Dataset):
        def _dtype(type_str: str, optional: bool):
            python_dtype = TYPE_MAP[type_str]
            return Optional[python_dtype] if optional else python_dtype

        fields = {column.name: (_dtype(column.spec.type, True), ...) for column in dataset.columns}
        return create_model(dataset.name, __base__=cls, **fields)


class SqlCompatibleItem(Item):
    def serialize(self, *args, **kwargs):
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes, *args, **kwargs) -> "SqlCompatibleItem":
        return cls.model_validate_json(data)
