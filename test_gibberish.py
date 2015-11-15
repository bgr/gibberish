import pytest
from gibberish import word_occurences, build_dict


class Test_word_occurences:

    @pytest.mark.parametrize('inp, exp', [
        ('', ({
            '': {}
        }, '')),

        (' ', ({
            '': {}
        }, '')),

        ('    ', ({
            '': {}
        }, '')),

        ('test', ({
            '': {'test': 1},
        }, 'test')),

        ('  Aa bb  cc  Bb  aa bb cc', ({
            '':   { 'aa': 1 },
            'aa': { 'bb': 2 },
            'bb': { 'cc': 2, 'aa': 1 },
            'cc': { 'bb': 1 },
        }, 'cc')),

        ('test test  Test', ({
            '':     { 'test': 1 },
            'test': { 'test': 2},
        }, 'test')),
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
        assert word_occurences(inp) == (exp, sign)

    @pytest.mark.parametrize('inp, exp', [
        ('A - hyphen -- a - Hyphen', ({
            '':  { 'a': 1 },
            'a': { '-': 2 },
            '-': { 'hyphen': 2, 'a': 1 },
            'hyphen': { '-': 1 }
        }, 'hyphen')),
    ])
    def test_hyphen(self, inp, exp):
        assert word_occurences(inp) == exp


class Test_build_dict:

    @pytest.mark.parametrize('inp', [ [], [''], ['', '   ', ''] ])
    def test_empty_lines(self, inp):
        d = build_dict(inp)
        assert d[''] == {}

    @pytest.mark.parametrize('inp, exp', [
        (['Hello world'], {
            '':  { 'hello': 1 },
            'hello': { 'world': 1 },
        }),
        (['Hello', 'world'], {
            '':  { 'hello': 1 },
            'hello': { 'world': 1 },
        }),
        (['Hello', '', '   ', 'world', ' '], {
            '':  { 'hello': 1 },
            'hello': { 'world': 1 },
        }),
        (['Hello', 'world', 'hello world', '', 'hello', '', '', 'world'], {
            '':  { 'hello': 1 },
            'hello': { 'world': 3 },
            'world': { 'hello': 2 },
        }),
    ])
    def test_lines(self, inp, exp):
        assert build_dict(inp) == exp
