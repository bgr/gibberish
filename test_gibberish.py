import pytest
from gibberish import build_dict, gutenberg_sanitized


class Test_build_dict:

    @pytest.mark.parametrize('inp, exp', [
        ('', {}),
        (' ', {}),
        ('    ', {}),

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
    def test_words_single_line(self, inp, exp):
        assert build_dict([inp])[0] == exp

    @pytest.mark.parametrize('sign', ['.', ',', ';'])
    def test_interpunction_single_line(self, sign):
        inp = 'Aa{sign} Bb{sign}  aa{sign}'.format(sign=sign)
        exp = {
            '':   { 'aa': 1 },
            'aa': { sign: 2 },
            sign:  { 'bb': 1, 'aa': 1 },
            'bb': { sign: 1 },
        }
        assert build_dict([inp])[0] == exp

    @pytest.mark.parametrize('inp, exp', [
        ('A - hyphen -- a - Hyphen', {
            '':  { 'a': 1 },
            'a': { '-': 2 },
            '-': { 'hyphen': 2, 'a': 1 },
            'hyphen': { '-': 1 }
        }),
    ])
    def test_hyphen_single_line(self, inp, exp):
        assert build_dict([inp])[0] == exp

    def test_multiple_empty_lines(self):
        d = build_dict(['', '   ', ''])[0]
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
        (['Hello', 'world'], {
            '':  { 'hello': 1 },
            'hello': { 'world': 1 },
        }),
        (['Hello', 'world', 'hello world', 'hello', 'world'], {
            '':  { 'hello': 1 },
            'hello': { 'world': 3 },
            'world': { 'hello': 2 },
        }),
    ])
    def test_lines_no_new_paragraphs(self, inp, exp):
        assert build_dict(inp)[0] == exp

    @pytest.mark.parametrize('inp, exp', [
        (['Hello', '', '   ', 'world', ' '], {
            '':  { 'hello': 1, 'world': 1 },
            'hello': { '': 1 },
            'world': { '': 1 },
        }),
        (['Hello', 'world', 'hello world', '', 'hello', '', '', 'world'], {
            '':  { 'hello': 2, 'world': 1 },
            'hello': { 'world': 2, '': 1 },
            'world': { 'hello': 1, '': 1 },
        }),
    ])
    def test_lines_with_new_paragraphs(self, inp, exp):
        assert build_dict(inp)[0] == exp

    def test_caps(self):
        inp = ['Hello John McClane.']
        caps = build_dict(inp)[1]
        assert 'hello' not in caps
        assert caps['john'] == 'John'
        assert caps['mcclane'] == 'McClane'


def test_gutenberg_sanitized():
    lines = [
        'Something irrelevant',
        '',
        'more stuff',
        '',
        '',
        '*** START OF THIS PROJECT GUTENBERG EBOOK TEST ***',
        '',
        'important',
        'also important',
        '',
        '*** END OF THIS PROJECT GUTENBERG EBOOK FRANKENSTEIN ***',
        '',
        'this should not be included',
        '',
        'neither should this',
        '',
        '*** START OF THIS PROJECT GUTENBERG EBOOK TEST ***',
        '',
        'again, important',
        '',
        '*** END OF THIS PROJECT GUTENBERG EBOOK FRANKENSTEIN ***',
        'this should not be included either',
    ]
    assert list(gutenberg_sanitized(lines)) == [
        '',
        'important',
        'also important',
        '',
        '',
        'again, important',
        '',
    ]
