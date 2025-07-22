from datagen.generators.datetime import DateGenerator, DatetimeGenerator, DateConfig, DateTimeConfig
from datetime import datetime, date

SEED = 192837465


def test_date_and_time():
    d_dt1 = DatetimeGenerator(
        DateTimeConfig(
            type="datetime",
            timezone="Asia/Ho_Chi_Minh",
            min="2024-01-02 12:23:31.000000",
            max="2024-04-02 12:59:31.000000",
        ),
        seed=SEED,
    )

    assert datetime.strftime(d_dt1.generate(), "%Y-%m-%d %H:%M:%S.%f") == "2024-01-16 08:51:36.492215"


def test_date():
    d_dt1 = DateGenerator(DateConfig(type="date", min="2024-01-02", max="2024-04-02"), seed=SEED)

    assert date.strftime(d_dt1.generate(), "%Y-%m-%d") == "2024-01-15"
