from datetime import date, datetime
from typing import Optional

import pytz

from datagen.generators.base import Generator


class DateGenerator(Generator):

    def generate(self) -> Optional[date]:
        null = self._rd.random()
        if null < self._cfg.nullability:
            return None
        elif not self._cfg.dialect:
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


class DatetimeGenerator(Generator):

    def generate(self) -> Optional[datetime]:
        cfg = self._cfg
        null = self._rd.random()
        if null < cfg.nullability:
            return None

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
