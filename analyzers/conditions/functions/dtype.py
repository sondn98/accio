from datetime import datetime, date


cast_bool = lambda x: bool(x)
cast_int = lambda x: int(x)
cast_double = lambda x: float(x)
cast_dec = lambda x, p, s: x
cast_str = lambda x: str(x)
cast_bin = lambda x: bin(x)
cast_date = lambda x: date.fromisoformat(x)
cast_ts = lambda x: datetime.fromisoformat(x)
