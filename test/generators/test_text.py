from datagen.generators.text import TextGenerator, TextConfig


SEED = 192837465


def test_text():
    d_tt1 = TextGenerator(TextConfig(type="text", allowed_values=["abc", "xyz"]), SEED)
    assert d_tt1.generate() == "abc"

    d_tt2 = TextGenerator(TextConfig(type="text", length=100), SEED)
    gen_text = "congue sagittis 5 vehicula scelerisque luctus Duis lorem Cras mollis posuere dictum pulvinar dictum"
    assert d_tt2.generate() == gen_text

    d_tt3 = TextGenerator(TextConfig(type="text", length=100, const="Lorem Ipsum"), SEED)
    gen_text = "Lorem Ipsum"
    assert d_tt3.generate() == gen_text
