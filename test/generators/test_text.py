from generators.text import *
from datetime import datetime
import pytz


SEED = 192837465


def test_text():
    d_tt1 = TextGenerator(SEED, allowed_values=["abc", "xyz"])
    assert d_tt1.generate() == "abc"

    d_tt2 = TextGenerator(SEED, length=100)
    gen_text = "congue sagittis 5 vehicula scelerisque luctus Duis lorem Cras mollis posuere dictum pulvinar dictum"
    assert d_tt2.generate() == gen_text

    d_tt3 = TextGenerator(SEED, length=100, const="Lorem Ipsum")
    gen_text = "Lorem Ipsum"
    assert d_tt3.generate() == gen_text
