import re

import pandas as pd
import numpy as np

from collections import Counter

from nltk.util import ngrams


def clean_text(text):
    '''Regex-based text cleaner.'''

    text = str(text).lower()
    text = re.sub('\.+', ' ', text)  # other non-alphabetic
    text = re.sub('[0-9]', ' ', text)  # numbers
    text = re.sub('[-!$%^&*()_+|~=`{}\[\]:";<>?,.\/]', ' ', text)  # other non-alphabetic
    text = re.sub('[^а-яa-z\d\s]', ' ', text)  # other non-alphabetic
    return text


def tokenize(text, stop_words=None, min_len=1):
    '''Simple tokenizer with stop words filtering.'''

    if not (not text or len(text) == 1):
        text = text.strip().split()
        if stop_words is not None:
            text = (w for w in text if not w in stop_words)
        return [g[0] for g in list(ngrams(text, 1)) if len(g[0]) > min_len]

    else:
        return []


def get_tokens_wvs(tokens, wvs):
    '''Simple wrapper for converting a list of tokens to list of word vectors.'''

    cur_vec_list = []

    for token in tokens:
        try:
            cur_vec_list.append(wvs[token])
        except KeyError:
            continue

    return cur_vec_list


def get_aggregated_wvs(tokens, wvs, aggregate=sum, no_vectors='zeros', dim=300):
    '''Aggregator for converting a list of word vectors into one word vector.'''

    vectors = get_tokens_wvs(tokens, wvs)

    if vectors:
        return aggregate(vectors)
    else:
        if no_vectors == 'zeros':
            return np.zeros(dim)
        elif no_vectors == 'empty':
            return np.array([])


def standardize_ean(input_):
    if not input_.isdigit():
        return ''
    else:
        if len(input_) == 8 or len(input_) == 13:
            res = input_
        elif 8 < len(input_) < 13:
            return input_[:8]
        elif 13 < len(input_):
            return input_[:13]
        else:
            return input_


def standardize_inn(input_):
    if not input_.isdigit():
        return ''
    else:
        if len(input_) == 10 or len(input_) == 12:
            return input_
        elif 10 < len(input_) < 12:
            return input_[:10]
        elif 12 < len(input_):
            return input_[:12]
        else:
            return input_


def fix_digit_value(input_):
    if not input_.isdigit():
        return 0


def count_top_words(word_list, n):
    return Counter(word_list).most_common(n)


def get_all_fields(items, depth=1):
    '''Recursive function for getting all keys in dictionary.'''

    fields = set()

    if isinstance(items, pd.DataFrame):
        items = items.to_dict(orient='records')

    if isinstance(items, list):
        for item in items:
            for key in item.keys():
                if isinstance(item[key], dict) and depth > 0:
                    fields.update(get_all_fields(item[key], depth=depth - 1))
                else:
                    fields.add(key)

    elif isinstance(items, dict):
        for key in items.keys():
            if isinstance(items[key], dict) and depth > 0:
                fields.update(get_all_fields(items[key], depth=depth - 1))
            else:
                fields.add(key)

    else:
        raise

    return fields


def get_ambiguous_field(obj, possible_names):
    '''Function for getting dict value that doesn\'t have one certain key.'''

    for n in possible_names:
        res = obj.get(n)
        if res is not None:
            return res


def get_multi(obj, fields):
    query = 'obj'
    for pf in fields:
        query += f'.get("{pf}")'

    return eval(query)


class Pipeline:
    '''
    A class that can be used for wrapping lots of preprocessing
    functions in one pipeline.
    '''

    def __init__(self, steps):
        self.steps = steps

    def __repr__(self):
        return f'Pipeline(steps={self.steps})'

    def __bool__(self):
        return bool(self.steps)

    def __len__(self):
        return len(self.steps)

    def __add__(self, other):
        if isinstance(other, tuple):
            return Pipeline(steps=self.steps + [other])

        elif isinstance(other, list):
            return Pipeline(steps=self.steps + other)

        elif isinstance(other, Pipeline):
            return Pipeline(steps=self.steps + other.steps)

        else:
            raise

    def __eq__(self, other):
        return self.steps == other.steps

    def __ne__(self, other):
        return self.steps != other.steps

    def apply(self, input_):
        res = input_
        for func, kwargs, input_arg_name in self.steps:
            cur_kwargs = dict(**{input_arg_name: res}, **kwargs)
            res = func(**cur_kwargs)
        return res
