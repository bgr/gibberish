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


def word_pairs(lines_iterable):
    prev_word = ''

    for line in lines_iterable:

        yielded = False
        for m in matcher.finditer(line):
            cur_word = m.group(0)

            if (prev_word, cur_word) != ('', ''):
                yield prev_word, cur_word
                yielded = True

            prev_word = cur_word

        if not yielded and prev_word != '':
            # line had no words, assume it's a start of a new paragraph
            cur_word = ''
            yield prev_word, cur_word
            prev_word = cur_word


def build_dict(lines_iterable):
    """ Returns a mapping with format { word: { next_word: num_occurences } }.

        The given iterable should produce strings - lines of text (hint: you
        can pass an open file descriptor).
    """
    occs = defaultdict(lambda: defaultdict(int))
    # caps = defaultdict(str)

    for raw_prev_word, raw_cur_word in word_pairs(lines_iterable):
        prev_word = fix_word(raw_prev_word)
        cur_word = fix_word(raw_cur_word)

        occs[prev_word][cur_word] += 1

        # remember that current word should be capitalized in generated output
        # if it's capitalized in original text and it's not the first word in
        # the sentence
        # if prev_word not in ['', '.'] and raw_cur_word[:1] != cur_word[:1]:
            # caps[cur_word] = raw_prev_word

    return occs


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
