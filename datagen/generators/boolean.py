from typing import Optional

from datagen.generators.base import Generator


class BoolGenerator(Generator):

    def generate(self) -> Optional[bool]:
        null = self._rd.random()
        if null < self._cfg.nullability:
            return None

        n = self._rd.random()
        return n < self._cfg.ratio
