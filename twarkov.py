#!usr/bin/env python
# -*- coding: utf-8 -*-

from nltk import word_tokenize
from collections import defaultdict, Counter
from sys import argv
import random
import operator
import bisect
import string
import re

# token cleanup functions


def default_tokenize(text):
    '''gets rid of unnecessary quotes'''
    return [w for w in word_tokenize(text)
            if w not in string.punctuation
            and w != "''" and w != "``"]


def twitter_tokenize(text):
    '''fixes hashtags and @replies
    that are separated by nltk's tokenizer'''
    prefixes = set(['@', '#'])
    garbage = set(["''", "``", "http", "https", "n't"])
    tokens = word_tokenize(text)
    result = []
    for tok in tokens:
        if result and result[-1] in prefixes:
            result[-1] = '{}{}'.format(result[-1], tok)
        elif (tok in string.punctuation or tok in garbage) and tok not in prefixes:
            pass
        else:
            result.append(tok)
    return result

# text cleanup functions


def fix_apostrophes(text):
    '''no space between end of word and apostrophe, 
    friend 's becomes friend's', i 'm becomes i'm'''
    return re.sub(r"(\w)\s'(\w)", r"\1'\2", text)


def fix_nt(text):
    '''fixes issue with words ending in n't,
    is n't becomes isn't, do n't becomes don't'''
    return re.sub(r"(\w)\sn't", r"\1n't", text)


def fix_tco(text):
    '''gets rid of poorly formatted t.co links'''
    no_tco = re.sub(r"(//t\.co/\w+)", r"", text)
    return re.sub(r"(\s)\s", r"\1", no_tco)


def fix_hashtags(text):
    clean = re.sub(r'(#|#\s)\1*', r'', text)
    return clean.strip()


def fix_therest(text):
    '''hacky tool to replace other stuff that has
    been consistently wrong'''
    nna_hack = re.sub(r'n na', r'nna', text)
    quote_hack = re.sub(r"“”“", r'', nna_hack)
    if quote_hack[0:2] == "'s":
        clean = quote_hack[3:]
    else:
        clean = quote_hack
    return clean


def final_cleanup(text):
    '''run on generated text to do all cleanup'''
    clean = fix_apostrophes(fix_nt(fix_tco(fix_hashtags(fix_therest(text)))))
    if len(clean) >= 2 and clean[-2] == (' ' or '.'):
        clean = clean[:-2] + '.'
    return clean


# end marker

class EndToken(object):
    ''' Special dummy class denoting the end of a sentence. '''

    def __init__(self):
        # no-op
        return

class MarkovGenerator(object):

    '''markov text generator for making bots from people's twitter timelines'''

    def __init__(self, text, ngram=2, tokenize_fun=default_tokenize, use_end_tokens=False):
        self.text = text
        self.ngram = ngram
        self.tokenize_fun = tokenize_fun
        self.use_end_tokens = type(text) is list and use_end_tokens
        self.markov_dict = self.make_markov_dict()

    def make_markov_dict(self):
        '''returns a dict of {ngram tuple: Counter} 
        counting the number of times words follow an ngram'''
        text = self.text if type(self.text) is list else [self.text]
        ngram = self.ngram
        markov_dict = defaultdict(Counter)

        for sentence in text:
            words = self.tokenize_fun(sentence)
            zippy_words = zip(*[words[i:] for i in xrange(ngram + 1)])
            for t in zippy_words:
                a, b = t[:-1], t[-1]
                markov_dict[a][b] += 1
            if self.use_end_tokens:
                markov_dict[t[1:]][EndToken()] += 1

        return markov_dict

    def choose_word(self, start_key):
        '''returns a next word based on cumulative distribution
        likelihood that it follows the previous ngram'''
        def accumulate(iterable, func=operator.add):
            it = iter(iterable)
            total = next(it)
            yield total
            for el in it:
                total = func(total, el)
                yield total
        if len(self.markov_dict[start_key].keys()):  # Check that values follow the start_key
            choices, weights = zip(*self.markov_dict[start_key].iteritems())
            cumulative_distribution = list(accumulate(weights))
            rando = random.random() * cumulative_distribution[-1]
            return choices[bisect.bisect(cumulative_distribution, rando)]
        else:
            return EndToken()

    def ngrams_to_words(self, tuple_list):
        '''(list of ngram tuples) -> string
        helper function for generate_tweet'''
        word_list = [x[0] for x in tuple_list[1:-1]] + list(tuple_list[-1])
        words = ''
        for i in word_list:
            if i not in string.punctuation:
                words += i + ' '
            else:
                words = words.strip() + i + ' '
        return words.strip()

    def generate_tweet(self):
        '''generates tweet text'''
        start_tup = random.choice(self.markov_dict.keys())
        words_length = 0
        words_tuples = [start_tup]
        while words_length < 90:
            next_word = self.choose_word(words_tuples[-1])
            if type(next_word) == EndToken:
                break
            next_tup = words_tuples[-1][1:] + (next_word,)
            words_length += len(next_word) + 1
            words_tuples.append(next_tup)
        words_tuples.append(('.',))
        generated_text = self.ngrams_to_words(words_tuples)
        return final_cleanup(generated_text)
