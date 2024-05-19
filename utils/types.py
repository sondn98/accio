def assert_types(p_type: type, *args):
    for arg in args:
        assert not arg or isinstance(arg, p_type)
