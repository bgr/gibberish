import re
from collections import defaultdict
import random


matcher = re.compile('(\w{1,})|([.])|(,)|(--?)|(;)')

interpunction = ['.', ',', ';']

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
    """ Returns a mapping with format { word: { next_word: num_occurences } }.

        The given iterable should produce strings - lines of text (hint: you
        can pass an open file descriptor).
    """
    prev_word = ''
    d = defaultdict(lambda: defaultdict(int))

    for line in lines_iterable:
        mapping, prev_word = word_occurences(line, prev_word)

        for word in mapping:
            for inner_word in mapping[word]:
                d[word][inner_word] += mapping[word][inner_word]

    return d


def generate_gibberish(lines_iterable, output_words=200):
    """ Returns list of random words, containing output_words or more elements.

        Words are chosen based on probabilities obtained from given
        lines_iterable. The number of returned words will be a bit more than
        given output_words, since it'll continue generating until the current
        sentence ends.
    """
    d = build_dict(lines_iterable)

    prev_word = ''
    words = []

    while True:
        output_words -= 1

        next_words = list(d[prev_word].keys())
        next_word = random.choice(next_words)
        words.append(next_word)

        prev_word = next_word

        if output_words < 0 and prev_word == '.':
            break

    return words


def textualize(words):
    prev_word = ''

    for cur_word in words:
        if prev_word == '':
            yield '    '
            yield cur_word.capitalize()
        elif cur_word in interpunction:
            yield cur_word
        elif prev_word == '.':
            yield ' '
            yield cur_word.capitalize()
        else:
            yield ' '
            yield cur_word

        prev_word = cur_word


def gutenberg_sanitized(lines_iterable):
    enabled = False
    for line in lines_iterable:
        if line.startswith('*** START OF THIS PROJECT GUTENBERG'):
            enabled = True
        elif line.startswith('*** END OF THIS PROJECT GUTENBERG'):
            return
        elif enabled:
            yield line


if __name__ == '__main__':
    import os

    path = os.path.abspath(os.path.join('txt_books', 'pg1661.txt'))

    with open(path) as f:
        words = generate_gibberish(gutenberg_sanitized(f))
        txt = ''.join(textualize(words))

    # prevents unicode errors in Windows terminal
    printable = txt.encode('ascii', 'replace').decode('ascii')
    print(printable)
