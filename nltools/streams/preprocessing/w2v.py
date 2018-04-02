import numpy as np


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
