from jiradata import get_by_path


def test_get_by_path():
    dummy = {'a': 1,
             'b': {'c': 'ok', 'd': 3}}
    assert get_by_path(dummy, ('a')) == 1
    assert get_by_path(dummy, ('b', 'c')) == 'ok'
