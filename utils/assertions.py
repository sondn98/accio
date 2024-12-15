from typing import Any, List


def assert_types(p_type: type, *args):
    for arg in args:
        assert not arg or isinstance(arg, p_type)


def assert_gt(p1, p2, msg: str):
    assert p1 > p2, msg


def assert_ge(p1, p2, msg: str):
    assert p1 >= p2, msg


def assert_in(p, lst: List[Any], msg: str):
    assert p in lst, msg


def assert_between(p, high, low, msg, high_exclusive=False, low_exclusive=False):
    upper_bound_valid = p < high if high_exclusive else p <= high
    lower_bound_valid = p > low if low_exclusive else p >= high

    assert upper_bound_valid and lower_bound_valid, msg


def assert_not_null(*p):
    for _ in p:
        assert _ is not None


def validate_str_datetime(text, fmt="%Y-%m-%d %H:%M:%S") -> bool:
    if not text:
        return False

    from datetime import datetime

    try:
        datetime.strptime(text, fmt)
        return True
    except ValueError as e:
        return False
