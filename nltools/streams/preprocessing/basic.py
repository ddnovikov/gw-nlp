import re

from collections import Counter

from nltk.util import ngrams


def clean_text(text):
    '''Regex-based text cleaner.'''

    text = str(text).lower()
    text = re.sub('^@\w+|\s@\w+|\n@\w+', '', text)  # replies to other users
    text = re.sub('#[\w]+', '', text)  # hashtags
    text = re.sub('https?:\/\/[\S]+|[\w\.-]+\.[a-z]+', '', text)  # links
    text = re.sub('^\/.+', '', text)  # requests to bots
    text = re.sub('\.+', '', text)  # other non-alphabetic
    text = re.sub('[-!$%^&*()_+|~=`{}\[\]:";<>?,.\/]', '', text)  # other non-alphabetic
    text = re.sub('.+[^а-яa-z\d\s]', '', text)  # other non-alphabetic
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


def count_top_words(word_list, n):
    return Counter(word_list).most_common(n)


def preprocess(text, ignore=1):
    text = clean_text(text)

    if text == '' or len(text) == 1:
        return []

    else:
        return [g[0] for g in list(ngrams(text.strip().split(), 1)) if len(g[0]) > ignore]
