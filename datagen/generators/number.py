from typing import Optional

from datagen.generators.base import Generator


class IntGenerator(Generator):

    def generate(self) -> Optional[int]:
        null = self._rd.random()
        if null < self._cfg.nullability:
            return None

        return self._cfg.const if self._cfg.const else self._rd.randint(self._cfg.min, self._cfg.max)


class RealGenerator(Generator):

    def generate(self) -> Optional[float]:
        cfg = self._cfg
        null = self._rd.random()
        if null < cfg.nullability:
            return None

        return cfg.const if cfg.const else round(cfg.min + (cfg.max - cfg.min) * self._rd.random(), cfg.round)
