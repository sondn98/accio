import pytz
import sys
from typing import Optional, Union, Literal, List
from pydantic import BaseModel, model_validator
from datetime import date, datetime

from utils.assertions import assert_between, assert_types, assert_gt, assert_in, assert_ge


TYPE_MAP = {
    "bool": bool,
    "datetime": datetime,
    "date": date,
    "integer": int,
    "real": float,
    "text": str,
}


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


class DateTimeConfig(BaseModel):
    type: Literal["datetime"]
    const: Optional[datetime] = None
    timezone: Optional[str] = "UTC"
    nullable: Optional[bool] = False
    max: Union[datetime] = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.timezone(timezone))
    min: Union[datetime] = datetime.now(pytz.timezone(timezone))
    dialect: Optional[str] = None

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(datetime, self.const, self.min, self.max)
        assert_in(self.timezone, pytz.all_timezones, f"Unknown timezone {self.timezone}")

        if self.min and self.max:
            assert_gt(
                self.max,
                self.min,
                'Param "max" must be someday after "min"',
            )
        return self


class DateConfig(BaseModel):
    type: Literal["date"]
    const: Optional[date] = None
    dialect: Optional[str] = None
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    min: Union[date, int] = date(1970, 1, 1)
    max: Union[date, int] = date.today()

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(str, self.const)
        if self.dialect == "date_of_birth":
            assert_types(int, self.min, self.max)

        assert_gt(self.max, self.min, 'Dialect param "max" must be greater than "min"')
        return self


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


class TextConfig(BaseModel):
    type: Literal["text"]
    max_length: int = 100
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    allowed_values: List[str] = None
    const: Optional[str] = None
    dialect: Optional[str] = None

    @model_validator(mode="after")
    def validate_params(self):
        if self.max_length:
            assert_gt(self.max_length, 0, 'Param "max_length" must be a positive number')
        return self
