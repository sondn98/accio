from utils.assertions import assert_types, assert_gt, assert_in, validate_str_datetime
from datetime import date, datetime
from pytz import timezone
from generators.base import BaseGenerator
import pytz


DEFAULT_PARAM_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def validate_format(param, fmt):
    if param and not validate_str_datetime(param, fmt):
        raise AssertionError(f"Invalid date/datetime param format")


class DateGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kwargs):
        super().__init__(seed, **kwargs)

    @property
    def default_params(self):
        return dict(
            const=None,
            format=DEFAULT_PARAM_DATE_FORMAT,
            min=date(1970, 1, 1).strftime(DEFAULT_PARAM_DATE_FORMAT),
            max=date.today().strftime(DEFAULT_PARAM_DATE_FORMAT),
            max_age=80,
            min_age=0,
        )

    @property
    def format(self):
        return self._params["format"]

    def validate_params(self, params):
        assert_types(str, params["const"], params["format"], params["min"], params["max"])
        assert_types(int, params["max_age"], params["min_age"])

        if params["max_age"] and params["min_age"]:
            assert_gt(params["max_age"], params["min_age"], 'Dialect param "max_age" must be greater than "min_age"')

        validate_format(params["const"], DEFAULT_PARAM_DATE_FORMAT)
        validate_format(params["min"], DEFAULT_PARAM_DATE_FORMAT)
        validate_format(params["max"], DEFAULT_PARAM_DATE_FORMAT)
        if params["min"] and params["max"]:
            assert_gt(params["max"], params["min"], 'Param "to_date" must be someday after "from_date"')

    def generate(self) -> date:
        if self._params["const"]:
            datetime.strptime(self._params["const"], self._params["format"]).date()

        from_date = datetime.strptime(self._params["min"], self._params["format"])
        to_date = datetime.strptime(self._params["max"], self._params["format"])
        return self._faker.date_between_dates(from_date, to_date)

    def generate_by_dialect(self, dialect: str) -> date:
        if dialect == "date_of_birth":
            return self._faker.date_of_birth(maximum_age=self._params["max_age"], minimum_age=self._params["min_age"])
        elif dialect == "in_century":
            return self._faker.date_this_century()
        elif dialect == "in_decade":
            return self._faker.date_this_decade()
        elif dialect == "in_year":
            return self._faker.date_this_year()
        elif dialect == "in_month":
            return self._faker.date_this_month()
        else:
            raise ValueError(f"Dialect {dialect} has not been supported in date generator")


class DatetimeGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kwargs):
        super().__init__(seed, **kwargs)

    @property
    def default_params(self):
        return dict(
            const=None,
            format=DEFAULT_DATETIME_FORMAT,
            tz="UTC",
            from_datetime=datetime(1970, 1, 1, 0, 0, 0, 0, pytz.utc).strftime(DEFAULT_DATETIME_FORMAT),
            to_datetime=datetime.now(pytz.utc).strftime(DEFAULT_DATETIME_FORMAT),
        )

    @property
    def format(self):
        return self._params["format"]

    def validate_params(self, params):
        assert_types(str, params["const"], params["format"], params["from_datetime"], params["to_datetime"])
        assert_in(params["tz"], pytz.all_timezones, f"Unknown timezone {params['tz']}")

        validate_format(params["const"], DEFAULT_DATETIME_FORMAT)
        validate_format(params["from_datetime"], DEFAULT_DATETIME_FORMAT)
        validate_format(params["to_datetime"], DEFAULT_DATETIME_FORMAT)
        if params["from_datetime"] and params["to_datetime"]:
            assert_gt(
                params["to_datetime"],
                params["from_datetime"],
                'Param "to_datetime" must be someday after "from_datetime"',
            )

    def generate(self) -> datetime:
        if self._params["const"]:
            datetime.strptime(self._params["const"], self._params["format"])

        from_datetime = datetime.strptime(self._params["from_datetime"], self._params["format"])
        to_datetime = datetime.strptime(self._params["to_datetime"], self._params["format"])
        tz_info = pytz.timezone(self._params["tz"])
        return self._faker.date_time_between_dates(from_datetime, to_datetime, tz_info)

    def generate_by_dialect(self, dialect: str) -> datetime:
        if dialect == "in_century":
            return self._faker.datetime_this_century()
        elif dialect == "in_decade":
            return self._faker.datetime_this_decade()
        elif dialect == "in_year":
            return self._faker.datetime_this_year()
        elif dialect == "in_month":
            return self._faker.datetime_this_month()
        else:
            raise ValueError(f"Dialect {dialect} has not been supported in datetime generator")
