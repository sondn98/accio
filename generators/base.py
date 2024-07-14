from abc import ABC, abstractmethod
from faker.generator import random as rd
from faker import Faker
from typing import Any, Dict


class Generator(ABC):

    def __init__(self, seed: int = None, **kwargs):
        self._params = self.__get_and_validate_params(self.default_params, **kwargs)

        self._faker = Faker()
        self._rd = rd
        if seed:
            Faker.seed(seed)
            self._rd.seed(seed)

    @property
    def default_params(self):
        return dict()

    def __get_and_validate_params(self, default_params: Dict[str, Any], **kargs) -> Dict[str, Any]:
        from copy import deepcopy

        params = deepcopy(default_params)
        for key in params.keys():
            if key in kargs and kargs[key]:
                params[key] = kargs[key]
        self.validate_params(params)
        return params

    @abstractmethod
    def validate_params(self, params):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def generate_by_dialect(self, dialect: str):
        pass
