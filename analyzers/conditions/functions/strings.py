s_concat = lambda *args: "".join(args)
s_concat_ws = lambda sep, *args: sep.join(args)


def __hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError('Hamming distance can not be applied for different length strings')
    sum(c1 != c2 for c1, c2 in zip(str1, str2))
s_hamming_distance = lambda str1, str2: __hamming_distance(str1, str2)
s_length = lambda x: len(x)
s_lower = lambda x: x.lower()
s_upper = lambda x: x.upper()


