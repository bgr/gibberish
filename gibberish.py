import re


matcher = re.compile('(\w{1,})|([.])|(,)|(--?)|(;)')

word_fixes = {
    '--': '-',
}


def fix_word(word):
    word = word.lower()
    return word_fixes.get(word, word)


def word_occurences(line):
    """ Returns list of (word, number_of_occurrences) tuples."""
    d = {}
    for m in matcher.finditer(line):
        raw_word = m.group(0)
        word = fix_word(raw_word)
        if word not in d:
            d[word] = 0
        d[word] += 1

    return d


def build_dict(lines_iterable):
    """ Returns a { word: [(probability, word), ...] } mapping from given
        iterable.
        The iterable should produce strings - lines of text (hint: you can pass
        an open file descriptor).
    """
    d = {}

    for line in lines_iterable:


        w

    return d
