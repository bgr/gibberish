import re
from collections import defaultdict


matcher = re.compile('(\w{1,})|([.])|(,)|(--?)|(;)')

word_fixes = {
    '--': '-',
}


def fix_word(word):
    word = word.lower()
    return word_fixes.get(word, word)


def word_occurences(line, prev_word=''):
    """ Returns a tuple (occurrence_mapping, last_seen_word).
        The occurrence_mapping is a dict with format:
            { word: { next_word: num_occurences } }
    """
    mapping = {
        fix_word(prev_word): {}
    }

    for m in matcher.finditer(line):
        if prev_word not in mapping:
            mapping[prev_word] = {}

        d = mapping[prev_word]

        raw_word = m.group(0)
        word = fix_word(raw_word)

        if word not in d:
            d[word] = 0
        d[word] += 1

        prev_word = word

    return mapping, prev_word


def build_dict(lines_iterable):
    """ Returns a { word: [(probability, word), ...] } mapping from given
        iterable.
        The iterable should produce strings - lines of text (hint: you can pass
        an open file descriptor).
    """
    prev_word = ''
    d = defaultdict(lambda: defaultdict(int))

    for line in lines_iterable:
        mapping, prev_word = word_occurences(line, prev_word)

        for word in mapping:
            for inner_word in mapping[word]:
                d[word][inner_word] += mapping[word][inner_word]

    return d
