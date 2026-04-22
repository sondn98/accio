from typing import Optional, Type

from pydantic import BaseModel, Field, create_model

from models.config import Dataset
from models.types import TYPE_MAP


def build_item(name, cls: Type[BaseModel], *datasets: Dataset):
    def _dtype(type_str: str, optional: bool):
        python_dtype = TYPE_MAP[type_str]
        return Optional[python_dtype] if optional else python_dtype

    fields = {}
    for ds in datasets:
        fields.update(
            {
                f"{ds.name}.{column.name}": (_dtype(column.generate.type, True), Field(..., alias=column.name))
                for column in ds.columns
            }
        )
    return create_model(name, __base__=cls, **fields)


class Item(BaseModel):
    model_config = {"populate_by_name": True}

    def serialize(self, *args, **kwargs):
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes, *args, **kwargs) -> "Item":
        return cls.model_validate_json(data)
