from datagen.generators import base
from datagen.generators.boolean import BoolGenerator, BoolConfig
from datagen.generators.datetime import DateGenerator, DateConfig, DatetimeGenerator, DateTimeConfig
from datagen.generators.number import IntGenerator, IntConfig, RealGenerator, RealConfig
from datagen.generators.text import TextGenerator, TextConfig
from datagen.models import GeneratorConfig
from functools import lru_cache


@lru_cache
def find_generator(cfg: type[GeneratorConfig], **kwargs):
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
