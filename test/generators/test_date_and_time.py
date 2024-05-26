from generators.date_and_time import *
from datetime import datetime
import pytz

SEED = 192837465


def test_date_and_time():
    d_dt1 = DatetimeGenerator(SEED, tz='Asia/Ho_Chi_Minh',
                              from_datetime='2024-01-02 12:23:31.000000',
                              to_datetime='2024-04-02 12:59:31.000000')

    assert datetime.strftime(d_dt1.generate(), d_dt1.format) == '2024-01-16 08:51:36.492215'
