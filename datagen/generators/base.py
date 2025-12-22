from abc import ABC, abstractmethod

from faker import Faker
from faker.generator import random as rd


class Generator(ABC):

    def __init__(self, config, seed: int = None, **kwargs):
        self._faker = Faker()
        self._rd = rd
        self._cfg = config
        if seed:
            Faker.seed(seed)
            self._rd.seed(seed)

    @abstractmethod
    def generate(self):
        pass
