from generators.base import BaseGenerator
from generators.boolean import BoolGenerator
from generators.date_and_time import DateGenerator, DatetimeGenerator
from generators.number import IntGenerator, RealGenerator
from generators.text import TextGenerator
from models.config import DataType


def generator(dtype: DataType, seed: int = None, **params) -> BaseGenerator:
    if dtype == DataType.INTEGER:
        return IntGenerator(seed, **params)
    if dtype == DataType.REAL:
        return RealGenerator(seed, **params)
    if dtype == DataType.BOOLEAN:
        return BoolGenerator(seed, **params)
    if dtype == DataType.TEXT:
        return TextGenerator(seed, **params)
    if dtype == DataType.DATE:
        return DateGenerator(seed, **params)
    if dtype == DataType.DATE_TIME:
        return DatetimeGenerator(seed, **params)
    else:
        raise ValueError(f"Unrecognized data type {dtype}")
