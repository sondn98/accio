import sys
from typing import Any, Dict
from generators.base import BaseGenerator
from utils.assertions import (
    assert_types, assert_gt, assert_ge
)


class IntGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kargs):
        super().__init__(seed, **kargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(
            high=sys.maxsize,
            low=-sys.maxsize - 1,
            const=None
        )

    def validate_params(self, params):
        assert_types(int, params['high'], params['low'], params['const'])

        if params['high'] and params['low']:
            assert_gt(params['high'], params['low'],
                      'Param "low" must be less then param "high"')

    def generate(self) -> int:
        if self._params['const']:
            return self._params['const']

        high = self._params['high']
        low = self._params['low']
        return self._rd.randint(low, high)

    def generate_by_dialect(self, dialect: str) -> int:
        raise Exception('Generating int by dialect has not yet supported')


class RealGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kargs):
        super().__init__(seed, **kargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(
            high=sys.float_info.max,
            low=-sys.float_info.max,
            const=None,
            scale=2
        )

    def validate_params(self, params):
        assert_types(float, params['high'], params['low'], params['const'])
        assert_types(int, params['scale'])

        assert_ge(18, params['scale'],
                  'Param "scale" in real generator must not be greater than 18')
        if params['high'] and params['low']:
            assert_gt(params['high'], params['low'],
                      'Param "low" must be less then param "high"')

    def generate(self) -> float:
        if self._params['const']:
            return self._params['const']

        high = self._params['high']
        low = self._params['low']
        scale = self._params['scale']

        n = low + (high - low) * self._rd.random()
        return round(n, scale)

    def generate_by_dialect(self, dialect: str):
        raise Exception('Generating real by dialect has not yet supported')
