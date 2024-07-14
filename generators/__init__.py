from generators.base import Generator
from generators.boolean import BoolGenerator
from generators.date_and_time import DateGenerator, DatetimeGenerator
from generators.number import IntGenerator, RealGenerator
from generators.text import TextGenerator
from models.config import DataType
from functools import partial


def generator_with_seed(dtype: DataType, seed: int) -> partial:
    if dtype == DataType.INTEGER:
        return partial(IntGenerator, seed)
    if dtype == DataType.REAL:
        return partial(RealGenerator, seed)
    if dtype == DataType.BOOLEAN:
        return partial(BoolGenerator, seed)
    if dtype == DataType.TEXT:
        return partial(TextGenerator, seed)
    if dtype == DataType.DATE:
        return partial(DateGenerator, seed)
    if dtype == DataType.DATE_TIME:
        return partial(DatetimeGenerator, seed)
    else:
        raise ValueError(f"Unrecognized data type {dtype}")


def generator(dtype: DataType) -> partial:
    import os

    seed = os.environ.get("ACCIO_SEED")
    return generator_with_seed(dtype, int(seed) if seed else None)
