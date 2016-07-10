#!/usr/bin/python

import numpy as np

def generateRandomStringList(n_strings=1, string_length=6,
        string_length_prob=None, character_choices=None,
        character_probabilities=None,):

    ''' Generates a list of strings with random alphanumeric strings.

    Parameters
    ----------
    n_strings : int
        Number of strings in list.
    string_length : int, array-like
        Number of characters in each string. If the string_length
    string_length_prob : None, array-like
        If array-like, and string_length is array-like, corresponds to the
        relative proportions of string lengths to be generated in list.

    '''

    import random

    # Constants
    ALPHANUM = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # initialize variables
    string_list = []

    # specify character_choices as all numbers and letters if not provided
    if character_choices is None:
        character_choices = ALPHANUM

    # separate the string of characters into a list
    character_choices = list(character_choices)

    # get the probability of choosing a character
    if character_probabilities is not None:
        character_probabilities /= np.sum(character_probabilities)
    else:
        character_probabilities = len(character_choices) * (1,)

    # create list of strings lengths
    if string_length_prob is not None and isArrayLike(string_length_prob):
        # normalize the probabilities
        string_length_prob /= np.sum(string_length_prob)

        string_lengths = np.random.choice(string_length,
                                          size=n_strings,
                                          p=string_length_prob,
                                          )
    else:
        string_lengths = np.array(n_strings * (string_length,))


    # for each string length generate a string of random characters
    for string_length in string_lengths:

        string = np.random.choice(character_choices,
                                  size=string_length,
                                  p=character_probabilities,
                                  )

        # join the list as a string
        string_list.append(''.join(string))

    return string_list

def isArrayLike(var):

    ''' Checks if variable is array-like

    '''

    if hasattr(var, '__len__') and (not isinstance(var, str)):
        return True
    else:
        return False

def getRegexMatches(data, pattern):

    import re

    matches = np.empty(np.size(data))

    pattern = re.compile(pattern)

    for i in xrange(len(matches)):

        result = re.match(pattern, data[i])

        if result is None:
            matches[i] = 0
        else:
            matches[i] = 1

    return matches

