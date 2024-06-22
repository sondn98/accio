from generators.number import *


SEED = 192837465


def test_generate_int():
    i_g1 = IntGenerator(seed=SEED, const=1)
    assert i_g1.generate() == 1

    i_g2 = IntGenerator(seed=SEED, max=4, min=-4, const=6)
    assert i_g2.generate() == 6

    i_g3 = IntGenerator(seed=SEED, max=4, min=-4)
    assert i_g3.generate() == -2


def test_generate_real():
    r_g1 = RealGenerator(seed=SEED, const=1.2, scale=3)
    assert r_g1.generate() == 1.2

    r_g2 = RealGenerator(seed=SEED, max=4.0, min=-4.0, const=6.0)
    assert r_g2.generate() == 6.0

    r_g3 = RealGenerator(seed=SEED, max=4.0, min=-4.0)
    assert r_g3.generate() == -2.81

    r_g4 = RealGenerator(seed=SEED, max=4.0, min=-4.0, scale=8)
    assert r_g4.generate() == -2.80813625
