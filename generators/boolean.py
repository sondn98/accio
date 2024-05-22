from utils.assertions import (
    assert_types, assert_between
)
from generators.base import BaseGenerator


class BoolGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kargs):
        super().__init__(seed, **kargs)

    @property
    def default_params(self):
        return dict(
            const=None,
            ratio=0.5
        )

    def validate_params(self, params):
        assert_types(float, params['ratio'], params['const'])
        assert_between(params['ratio'], 1.0, 0.0,
                       'Param "ratio" in bool generator must be in (0, 1) exclusive')

    def generate(self):
        n = self._rd.random()
        return n < self._params['ratio']

    def generate_by_dialect(self, dialect: str):
        raise Exception('Generating bool by dialect has not yet supported')
