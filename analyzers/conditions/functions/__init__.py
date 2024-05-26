from analyzers.conditions.functions.maths import *
from analyzers.conditions.functions.strings import *
from analyzers.conditions.functions.dtype import *
from typing import Callable, Dict


MATH_FUNCTION_REGISTRY: Dict[str, Callable] = dict(
    abs=m_abs,
    cbrt=m_cbrt,
    ceil=m_ceil,
    degrees=m_degrees,
    e=m_e,
    exp=m_exp,
    floor=m_floor,
    ln=m_ln,
    log=m_log,
    log2=m_log2,
    log10=m_log10,
    mod=m_mod,
    pi=m_pi,
    pow=m_pow,
    radians=m_radians,
    round=m_round,
    sign=m_sign,
    sqrt=m_sqrt,
    truncate=m_truncate,
    width_bucket=m_width_bucket,
)

STR_FUNCTION_REGISTRY: Dict[str, Callable] = dict(
    concat=s_concat,
    concat_ws=s_concat_ws,
    hamming_distance=s_hamming_distance,
    length=s_length,
    lower=s_lower,
    upper=s_upper
)

DTYPE_FUNCTION_REGISTRY: Dict[str, Callable] = dict(
    bool=cast_bool,
    tinyint=cast_int,
    smallint=cast_int,
    int=cast_int,
    integer=cast_int,
    bigint=cast_int,
    double=cast_double,
    float=cast_double,
    dec=cast_dec,
    char=cast_str,
    varchar=cast_str,
    string=cast_str,
    binary=cast_bin,
    date=cast_date,
    timestamp=cast_ts,
)

FUNCTIONS: Dict[str, Callable] = dict(**MATH_FUNCTION_REGISTRY, **STR_FUNCTION_REGISTRY)
