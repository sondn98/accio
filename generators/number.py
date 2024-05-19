import faker
import sys
from faker import Faker
from faker.generator import random
from typing import Any, Dict
from generators.base import BaseGenerator
from utils.types import assert_type

int_fake = Faker()
DEFAULT_PARAMS = dict(
    high=None,
    low=None,
    const=None
)


class IntGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kargs):
        super().__init__(**kargs)
        self.faker = BaseGenerator._create_faker(seed)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(
            high=None,
            low=None,
            const=None
        )

    def __validate_params(self, params):
        assert_type(int,
                    params['high'], params['low'], params['const'])

        if params['high'] and params['low']:
            assert params['low'] < params['high'], 'Param "low" must be less then param "high"'

    def generate(self) -> int:
        if self._params['const']:
            return self._params['const']

        rd = faker.Generator.random
        high = self._params.get('const', sys.maxsize)
        low = self._params.get('low', -sys.maxsize - 1)
        return rd.randint(low, high)

    def generate_by_dialect(self, dialect: str) -> int:
        raise Exception('Generating int by dialect has not yet supported')
