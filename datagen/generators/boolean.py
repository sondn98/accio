from datagen.generators.base import Generator


class BoolGenerator(Generator):

    def generate(self):
        n = self._rd.random()
        return n < self._cfg.ratio
