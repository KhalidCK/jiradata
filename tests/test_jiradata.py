from jiradata import get_by_path, get_top_label


def test_get_by_path():
    dummy = {'a': 1,
             'b': {'c': 'ok', 'd': 3}}
    assert get_by_path(dummy, ('a')) == 1
    assert get_by_path(dummy, ('b', 'c')) == 'ok'


def test_get_top_label():
    dummy_labels = [{'fields': {'labels': ['pirate', 'marine']}},
                    {'fields': {'labels': ['hero', 'vilain']}},
                    {'fields': {'labels': ['pirate']}},
                    {'fields': {'labels': ['marine']}}]

    assert get_top_label(dummy_labels) == {
        ('pirate', 2/4), ('marine', 2/4), ('hero', 1/4), ('vilain', 1/4)}
