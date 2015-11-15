import pytest
from gibberish import word_occurences


class Test_word_occurences:

    @pytest.mark.parametrize('inp, exp', [
        ('', {
            '': {}
        }),
        (' ', {
            '': {}
        }),
        ('    ', {
            '': {}
        }),
        ('test', {
            '': {'test': 1},
        }),
        ('  Aa bb  cc  Bb  aa bb cc', {
            '':   { 'aa': 1 },
            'aa': { 'bb': 2 },
            'bb': { 'cc': 2, 'aa': 1 },
            'cc': { 'bb': 1 },
        }),
        ('test test  Test', {
            '':     { 'test': 1 },
            'test': { 'test': 2},
        }),
    ])
    def test_words(self, inp, exp):
        assert word_occurences(inp) == exp

    @pytest.mark.parametrize('sign', ['.', ',', ';'])
    def test_interpunction(self, sign):
        inp = 'Aa{sign} Bb{sign}  aa{sign}'.format(sign=sign)
        exp = {
            '':   { 'aa': 1 },
            'aa': { sign: 2 },
            sign:  { 'bb': 1, 'aa': 1 },
            'bb': { sign: 1 },
        }
        assert word_occurences(inp) == exp

    @pytest.mark.parametrize('inp, exp', [
        ('A - hyphen -- a - Hyphen', {
            '':  { 'a': 1 },
            'a': { '-': 2 },
            '-': { 'hyphen': 2, 'a': 1 },
            'hyphen': { '-': 1 }
        }),
    ])
    def test_hyphen(self, inp, exp):
        assert word_occurences(inp) == exp
