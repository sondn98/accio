from typing import Optional, Literal
from utils.assertions import assert_between, assert_types
from datagen.generators.base import Generator
from pydantic import BaseModel, model_validator


class BoolConfig(BaseModel):
    type: Literal["bool"]
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    ratio: float = 0.5
    const: Optional[str] = None

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(float, self.ratio, self.const)
        assert_between(self.ratio, 1.0, 0.0, 'Param "ratio" in bool generator must be in exclusive (0, 1)')
        return self


class BoolGenerator(Generator):

    def __init__(self, config: BoolConfig, seed: int = None, **kwargs):
        super().__init__(config, seed, **kwargs)

    def generate(self):
        n = self._rd.random()
        return n < self._cfg.ratio
