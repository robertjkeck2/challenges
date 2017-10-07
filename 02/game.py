#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

import itertools
import json
import random
from pymemcache.client.base import Client

from data import DICTIONARY, LETTER_SCORES, POUCH

NUM_LETTERS = 7

def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")


def user_login(username):
    client = Client(('localhost', 11211), serializer=json_serializer,
                deserializer=json_deserializer)
    client.set(username, {'high_score': 0})
    return client


def get_high_score(client, username, score):
    current_high = client.get(username)['high_score']
    if score > current_high:
        current_high = score
    client.set(username, {'high_score': current_high})
    return current_high


def draw_letters():
    """Pick NUM_LETTERS letters randomly. Hint: use stdlib random"""
    return random.sample(set(POUCH), NUM_LETTERS)


def input_word(draw):
    """Ask player for a word and validate against draw.
    Use _validation(word, draw) helper."""
    word = ''
    while _validation(word, draw) is False:
        word = raw_input('Form a valid word: ')
    return word


def _validation(word, draw):
    """Validations: 1) only use letters of draw, 2) valid dictionary word"""
    validated = False
    if word in DICTIONARY and set(char.upper() for char in word).issubset(set(draw)):
        validated = True
    return validated


# From challenge 01:
def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


# Below 2 functions pass through the same 'draw' argument (smell?).
# Maybe you want to abstract this into a class?
# get_possible_dict_words and _get_permutations_draw would be instance methods.
# 'draw' would be set in the class constructor (__init__).
def get_possible_dict_words(draw):
    """Get all possible words from draw which are valid dictionary words.
    Use the _get_permutations_draw helper and DICTIONARY constant"""
    return [word for word in _get_permutations_draw(draw) if word.lower() in DICTIONARY]


def _get_permutations_draw(draw):
    """Helper for get_possible_dict_words to get all permutations of draw letters.
    Hint: use itertools.permutations"""
    permutations = []
    for i in range(1, NUM_LETTERS + 1):
        permutations.extend(map(''.join, itertools.permutations(draw, i)))
    return permutations

# From challenge 01:
def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)


def main():
    """Main game interface calling the previously defined methods"""
    username = raw_input('Username: ')
    client = user_login(username)

    while True:
        draw = draw_letters()
        print('Letters drawn: {}'.format(', '.join(draw)))

        word = input_word(draw)
        word_score = calc_word_value(word)
        print('Word chosen: {} (value: {})'.format(word, word_score))

        possible_words = get_possible_dict_words(draw)

        max_word = max_word_value(possible_words)
        max_word_score = calc_word_value(max_word)
        print('Optimal word possible: {} (value: {})'.format(
            max_word, max_word_score))

        game_score = word_score * 100.0 / max_word_score
        high_score = get_high_score(client, username, game_score)
        print('You scored: {:.1f}'.format(game_score))
        print('High score for {}: {:.1f}'.format(username, high_score))



if __name__ == "__main__":
    main()
