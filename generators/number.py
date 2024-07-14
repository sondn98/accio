import sys
from typing import Any, Dict
from generators.base import Generator
from utils.assertions import assert_types, assert_gt, assert_ge


class IntGenerator(Generator):

    def __init__(self, seed: int = None, **kwargs):
        super().__init__(seed, **kwargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(max=sys.maxsize, min=-sys.maxsize - 1, const=None)

    def validate_params(self, params):
        assert_types(int, params["max"], params["min"], params["const"])

        if params["max"] and params["min"]:
            assert_gt(params["max"], params["min"], 'Param "min" must be less then param "max"')

    def generate(self) -> int:
        if self._params["const"]:
            return self._params["const"]

        high = self._params["max"]
        low = self._params["min"]
        return self._rd.randint(low, high)

    def generate_by_dialect(self, dialect: str) -> int:
        raise Exception("Generating int by dialect has not yet supported")


class RealGenerator(Generator):

    def __init__(self, seed: int = None, **kwargs):
        super().__init__(seed, **kwargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(max=sys.float_info.max, min=-sys.float_info.max, const=None, scale=2)

    def validate_params(self, params):
        assert_types(float, params["max"], params["min"], params["const"])
        assert_types(int, params["scale"])

        assert_ge(18, params["scale"], 'Param "scale" in real generator must not be greater than 18')
        if params["max"] and params["min"]:
            assert_gt(params["max"], params["min"], 'Param "min" must be less then param "max"')

    def generate(self) -> float:
        if self._params["const"]:
            return self._params["const"]

        high = self._params["max"]
        low = self._params["min"]
        scale = self._params["scale"]

        n = low + (high - low) * self._rd.random()
        return round(n, scale)

    def generate_by_dialect(self, dialect: str):
        raise Exception("Generating real by dialect has not yet supported")
