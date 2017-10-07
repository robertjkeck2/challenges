import re
from data import DICTIONARY, LETTER_SCORES


def load_words():
    """Load dictionary into a list and return list"""
    dictionary_file = open(DICTIONARY, "r")
    dictionary_list = dictionary_file.read().split('\n')
    return dictionary_list[:-1]

def calc_word_value(word):
    """Calculate the value of the word entered into function
    using imported constant mapping LETTER_SCORES"""
    word_regex = "^[a-zA-Z]+$"
    if re.match(word_regex, word):
        word_score = 0
        letters = list(word)
        for letter in letters:
            word_score += LETTER_SCORES[letter.upper()]
        return word_score

def max_word_value(word_list=None):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    if not word_list:
        word_list = load_words()

    max_word, max_value = word_list[0], 0
    for word in word_list:
        word_value = calc_word_value(word)
        if word_value > max_value:
            max_word, max_value = word, word_value

    return max_word

if __name__ == "__main__":
    from test_wordvalue import *
    import unittest
    
    unittest.main() # run unittests to validate
