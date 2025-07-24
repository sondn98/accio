import sys
from typing import Optional, Literal
from pydantic import BaseModel, model_validator

from utils.assertions import assert_gt, assert_ge
from utils.assertions import assert_types
from datagen.generators.base import Generator


class IntConfig(BaseModel):
    type: Literal["integer"]
    const: Optional[int] = None
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    max: Optional[int] = sys.maxsize
    min: Optional[int] = -sys.maxsize

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(int, self.max, self.min, self.const)

        if self.max and self.min:
            assert_gt(self.max, self.min, 'Param "min" must be less then param "max"')
        return self


class IntGenerator(Generator):

    def generate(self) -> int:
        return self._cfg.const if self._cfg.const else self._rd.randint(self._cfg.min, self._cfg.max)


class RealConfig(BaseModel):
    type: Literal["real"]
    const: Optional[float] = None
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    max: Optional[float] = float("inf")
    min: Optional[float] = float("-inf")
    round: Optional[int] = 6

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(float, self.max, self.min, self.const)

        assert_ge(6, self.round, 'Param "round" in real generator must not be greater than 6')
        if self.max and self.min:
            assert_gt(self.max, self.min, 'Param "min" must be less then param "max"')

        return self


class RealGenerator(Generator):

    def generate(self) -> float:
        cfg = self._cfg
        return cfg.const if cfg.const else round(cfg.min + (cfg.max - cfg.min) * self._rd.random(), cfg.round)
