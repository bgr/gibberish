import pytest
from gibberish import word_occurences


@pytest.mark.parametrize('inp, exp', [
    ('', {}),
    (' ', {}),
    ('    ', {}),
    ('test', {'test': 1}),
    ('test test  Test', {'test': 3}),
    ('a   b c B a A b', {'a': 3, 'b': 3, 'c': 1}),
    ('. Aa. Bb.  aa.', {'.': 4, 'aa': 2, 'bb': 1}),
    (', Aa, Bb,  aa,', {',': 4, 'aa': 2, 'bb': 1}),
    ('A - hyphen -- a', {'-': 2, 'a': 2, 'hyphen': 1}),
    ('Aa - bb. Bb, aa.', {'aa': 2, 'bb': 2, '-': 1, '.': 2, ',': 1}),
])
def test_word_occurences(inp, exp):
    assert word_occurences(inp) == exp
