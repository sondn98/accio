from datagen.generators import base
from models.config import BoolConfig, DateConfig, DateTimeConfig, IntConfig, RealConfig, TextConfig
from datagen.generators.boolean import BoolGenerator
from datagen.generators.datetime import DateGenerator, DatetimeGenerator
from datagen.generators.number import IntGenerator, RealGenerator
from datagen.generators.text import TextGenerator
from functools import lru_cache


@lru_cache
def find_generator(cfg, **kwargs):
    if isinstance(cfg, IntConfig):
        return IntGenerator(cfg, **kwargs)
    if isinstance(cfg, RealConfig):
        return RealGenerator(cfg, **kwargs)
    if isinstance(cfg, BoolConfig):
        return BoolGenerator(cfg, **kwargs)
    if isinstance(cfg, TextConfig):
        return TextGenerator(cfg, **kwargs)
    if isinstance(cfg, DateConfig):
        return DateGenerator(cfg, **kwargs)
    if isinstance(cfg, DateTimeConfig):
        return DatetimeGenerator(cfg, **kwargs)
    else:
        raise ValueError(f"Unrecognized data type {cfg.type}")
