from utils.assertions import assert_types, assert_gt, assert_in
from datetime import date, datetime
from datagen.generators.base import Generator
from typing import Optional, Union, Literal
from pydantic import BaseModel, model_validator
import pytz


class DateConfig(BaseModel):
    type: Literal["date"]
    const: Optional[date] = None
    dialect: Optional[str] = None
    not_null: Optional[bool] = True
    min: Union[date, int] = date(1970, 1, 1)
    max: Union[date, int] = date.today()

    @model_validator(mode="after")
    def validate_params(self):
        assert_types(str, self.const)
        if self.dialect == "date_of_birth":
            assert_types(int, self.min, self.max)

        assert_gt(self.max, self.min, 'Dialect param "max" must be greater than "min"')
        return self


class DateGenerator(Generator):

    def generate(self) -> date:
        if not self._cfg.dialect:
            return self._cfg.const if self._cfg.const else self._faker.date_between_dates(self._cfg.min, self._cfg.max)
        if self._cfg.dialect == "date_of_birth":
            return self._faker.date_of_birth(maximum_age=self._cfg.max, minimum_age=self._cfg.min)
        elif self._cfg.dialect == "in_century":
            return self._faker.date_this_century()
        elif self._cfg.dialect == "in_decade":
            return self._faker.date_this_decade()
        elif self._cfg.dialect == "in_year":
            return self._faker.date_this_year()
        elif self._cfg.dialect == "in_month":
            return self._faker.date_this_month()
        else:
            raise ValueError(f"Dialect {self._cfg.dialect} has not been supported in date generator")


class DateTimeConfig(BaseModel):
    type: Literal["datetime"]
    const: Optional[datetime] = None
    timezone: Optional[str] = "UTC"
    not_null: Optional[bool] = True
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


class DatetimeGenerator(Generator):

    def generate(self) -> datetime:
        cfg = self._cfg
        tz_info = pytz.timezone(cfg.timezone)
        if not cfg.dialect:
            return cfg.const if cfg.const else self._faker.date_time_between_dates(cfg.min, cfg.max, tz_info)
        if cfg.dialect == "in_century":
            return self._faker.datetime_this_century()
        elif cfg.dialect == "in_decade":
            return self._faker.datetime_this_decade()
        elif cfg.dialect == "in_year":
            return self._faker.datetime_this_year()
        elif cfg.dialect == "in_month":
            return self._faker.datetime_this_month()
        else:
            raise ValueError(f"Dialect {cfg.dialect} has not been supported in datetime generator")
