import random


def generate_bool(ratio=0.5, seed=None) -> bool:
    if ratio >= 1 or ratio <= 0:
        raise Exception('Boolean generator ratio must be in (0.0, 1.0) exclusive')

    if seed:
        random.seed(seed)

    bean = random.random()
    return bean < ratio
