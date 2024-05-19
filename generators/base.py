from abc import ABC, abstractmethod
from faker import Faker
from typing import Any, Dict


class BaseGenerator(ABC):

    def __init__(self, **kargs):
        self._params = self.__get_and_validate_params(self.default_params, **kargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict()

    @staticmethod
    def _create_faker(self, seed: int = None) -> Faker:
        faker = Faker()
        if seed:
            Faker.seed(seed)
        return faker

    def __get_and_validate_params(self, default_params: Dict[str, Any], **kargs) -> Dict[str, Any]:
        from copy import deepcopy
        params = deepcopy(default_params)
        for key in params.keys():
            if key not in kargs:
                continue
            params[key] = kargs[key]
        params = self.__validate_params(params)
        return params

    @abstractmethod
    def __validate_params(self, params) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def generate_by_dialect(self, dialect: str):
        pass
