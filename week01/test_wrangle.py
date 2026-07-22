from wrangle import word_freq, invert, flatten, top_n, dedupe


def test_word_freq_strips_punctuation():
    assert word_freq("The cat and the hat.") == {'the': 2, 'cat': 1, 'and': 1, 'hat': 1}


def test_word_freq_empty_string():
    assert word_freq("") == {}


def test_invert_groups_by_value():
    assert invert({'a': 1, 'b': 2, 'c': 1}) == {1: ['a', 'c'], 2: ['b']}


def test_flatten_handles_empty_sublists():
    assert flatten([[1, 2], [3], []]) == [1, 2, 3]


def test_flatten_all_empty():
    assert flatten([[], [], []]) == []


def test_top_n_ties_alphabetical():
    assert top_n({'b': 2, 'a': 2, 'c': 1}, 2) == [('a', 2), ('b', 2)]


def test_top_n_all_ties():
    assert top_n({'z': 1, 'y': 1, 'x': 1}, 2) == [('x', 1), ('y', 1)]


def test_dedupe_preserves_order():
    assert dedupe(['x', 'y', 'x']) == ['x', 'y']


def test_dedupe_empty_list():
    assert dedupe([]) == []