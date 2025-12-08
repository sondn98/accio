from datagen.generators.base import Generator


class IntGenerator(Generator):

    def generate(self) -> int:
        return self._cfg.const if self._cfg.const else self._rd.randint(self._cfg.min, self._cfg.max)


class RealGenerator(Generator):

    def generate(self) -> float:
        cfg = self._cfg
        return cfg.const if cfg.const else round(cfg.min + (cfg.max - cfg.min) * self._rd.random(), cfg.round)
