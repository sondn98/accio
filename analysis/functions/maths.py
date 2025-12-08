import math
import random as rd


# Mathematical functions
m_abs = lambda x: math.fabs(x)
m_cbrt = lambda x: math.cbrt(x)
m_ceil = lambda x: math.ceil(x)
m_degrees = lambda x: math.degrees(x)
m_e = lambda: math.e
m_exp = lambda x: math.exp(x)
m_floor = lambda x: math.floor(x)
m_ln = lambda x: math.log(x)
m_log = lambda b, x: math.log(x, b)
m_log2 = lambda x: math.log(x, 2)
m_log10 = lambda x: math.log(x, 10)
m_mod = lambda x, y: math.fmod(x, y)
m_pi = lambda x: math.pi
m_pow = lambda x, y: math.pow(x, y)
m_radians = lambda x: math.radians(x)
m_round = lambda x, d=0: round(x, d)
m_sign = lambda x: 0 if x == 0 else 1 if x > 0 else -1
m_sqrt = lambda x: math.sqrt(x)
m_truncate = lambda x: math.trunc(x)
m_width_bucket = lambda x, b1, b2, n: (x - b1) // ((b2 - b1) / n) + 1

# Random functions
m_rand = lambda: rd.random()
