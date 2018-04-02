import os

from ..io_ import basic as basic_io
from ..preprocessing import basic as basic_prep
from ...exceptions import WrongSourceTypeError


def basic_gen(filename_prp, filename_raw, msg_brd=20000, src='prp'):
    if os.path.isfile(filename_prp) and src == 'prp':
        yield from basic_io.read_top_words(filename_prp)

    elif os.path.isfile(filename_raw) and (src == 'prp' or src == 'raw'):
        common = []
        for _, mes in basic_io.read_csv(filename_raw, msg_brd=msg_brd):
            common += basic_prep.preprocess(mes)
        if common:
            common = basic_prep.count_top_words(common)
            basic_io.list_to_csv(common, filename_prp)
            yield from common

    else:
        return


def common_gen(src='prp',
               filename_prp='common/prp/top_common.csv',
               filename_raw='common/raw/common.csv.gz'):
    yield from basic_gen(filename_prp, filename_raw, src=src)


def categories_gens(src_upd,
                    paths=None,
                    default_src='prp'):

    if paths is None:
        paths = ['categories/prp/', 'categories/raw/']

    src_dict = {c: default_src for c in ['it', 'marketing',
                                         'business', 'crypto', 'politics', 'flood',
                                         'gaming', 'cinema']}

    categories = {}

    if src_upd is not None:
        for key in src_upd.keys():
            src_dict[key] = src_upd[key]

    for cat in src_dict.keys():
        if src_dict[cat] == 'raw':
            categories[cat] = basic_gen(f'{paths[0]}top_{cat}.csv',
                                        f'{paths[1]}{cat}.csv.gz',
                                        msg_brd=150000,
                                        src='raw')

        elif src_dict[cat] == 'prp':
            categories[cat] = basic_gen(f'{paths[0]}top_{cat}.csv',
                                        f'{paths[1]}{cat}.csv.gz',
                                        src='prp')

        else:
            raise WrongSourceTypeError(f'Unknown source type {src_dict[cat]}')

    return categories


def input_gens(fs_list,
               count=200,
               src='prp',
               paths=None):

    if paths is None:
        paths = ['prp/', 'raw/']

    inputs = []

    for cnt, dump in enumerate(fs_list):
        if cnt <= count:
            if src == 'raw' or src == 'prp':
                ta = basic_gen(f'{paths[0]}top_{dump[:-3]}', f'{paths[1]}{dump}', src=src)
                if ta:
                    inputs.append(ta)

            else:
                raise WrongSourceTypeError(f'Unknown source type: {src}')

        else:
            break

    return inputs
