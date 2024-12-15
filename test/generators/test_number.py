from datagen.generators.number import IntGenerator, RealGenerator, IntConfig, RealConfig


SEED = 192837465


def test_generate_int():
    i_g1 = IntGenerator(IntConfig(type="integer", const=1), seed=SEED)
    assert i_g1.generate() == 1

    i_g2 = IntGenerator(IntConfig(type="integer", max=4, min=-4, const=6), seed=SEED)
    assert i_g2.generate() == 6

    i_g3 = IntGenerator(IntConfig(type="integer", max=4, min=-4), seed=SEED)
    assert i_g3.generate() == -2


def test_generate_real():
    r_g1 = RealGenerator(RealConfig(type="real", const=1.2, scale=3), seed=SEED)
    assert r_g1.generate() == 1.2

    r_g2 = RealGenerator(RealConfig(type="real", max=4.0, min=-4.0, const=6.0), seed=SEED)
    assert r_g2.generate() == 6.0

    r_g3 = RealGenerator(RealConfig(type="real", max=4.0, min=-4.0, round=2), seed=SEED)
    assert r_g3.generate() == -2.81

    r_g4 = RealGenerator(RealConfig(type="real", max=4.0, min=-4.0, round=6), seed=SEED)
    assert r_g4.generate() == -2.808136
