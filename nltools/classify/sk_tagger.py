import re
import os
import gzip
import csv
from collections import Counter
from nltk.util import ngrams


def read_raw(filename, msg_brd=20000):
    
    if filename[-4:] == '.csv':
        with open(filename) as csvfile:
            for i, row in enumerate(csv.reader(csvfile, delimiter=',')):
                if i+1 <= msg_brd:
                    yield row[1], row[2]
                else:
                    return 

    elif filename[-7:] == '.csv.gz':
        with gzip.open(filename, 'rt') as csvgzfile:
            for i, row in enumerate(csv.reader(csvgzfile, delimiter=',')):
                if i+1 <= msg_brd:
                    yield row[0], row[1], row[2]
                else:
                    return

    else:
        raise Exception('File extension is not *.csv or *.csv.gz.')


def read_prp(filename):
    with open(filename) as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            yield row[0], row[1]
           
 
def write_csv(data, filename, arg='w'):
    if filename[-3:] == '.gz':
        filename = filename[:-3]
    csvwriter = csv.writer(open(filename, arg))
    for d in data:
        csvwriter.writerow(d)
 
 
def clean_text(text):
    text = text.lower()
    text = re.sub('^@\w+|\s@\w+|\n@\w+', '', text) # replies to other users
    text = re.sub('#[\w]+', '', text) # hashtags
    text = re.sub('https?:\/\/[\S]+|[\w\.-]+\.[a-z]+', '', text) # links
    text = re.sub('^\/.+', '', text) # requests to bots
    text = re.sub('\.+', '', text) # other non-alphabetic
    text = re.sub('[-!$%^&*()_+|~=`{}\[\]:";<>?,.\/]', '', text) # other non-alphabetic
    text = re.sub('.+[^а-яa-z\d\s]', '', text) # other non-alphabetic
    return text


def preprocess(text):
    text = clean_text(text)
    
    if text == '' or len(text) == 1:
        return []

    else:
        return [g[0] for g in list(ngrams(text.strip().split(), 1)) if len(g[0]) > 1]


def get_top_words(wordlist, n=None):
    return Counter(wordlist).most_common(n)


def basic_gen(filename_prp, filename_raw, msg_brd=20000, src='prp'):
    if os.path.isfile(filename_prp) and src == 'prp':
        yield from read_prp(filename_prp)

    elif os.path.isfile(filename_raw) and (src == 'prp' or src == 'raw'):
        common = []
        for _, mes in read_raw(filename_raw, msg_brd=msg_brd):
            common += preprocess(mes)
        if common:
            common = get_top_words(common)
            write_csv(common, filename_prp)
            yield from common

    else:
        return []

def common_gen(src='prp', filename_prp='common/prp/top_common.csv', 
                filename_raw='common/raw/common.csv.gz'):
    yield from basic_gen(filename_prp, filename_raw, src=src)


def categories_gens(src_upd={}, paths=['categories/prp/',
                   'categories/raw/'], default_src='prp'):

    src_dict = {c: default_src for c in ['it', 'marketing',
                'business', 'crypto', 'politics', 'flood',
                'gaming', 'cinema']}

    categories = {}
    for key in src_upd.keys():
        src_dict[key] = src_upd[key]

    for cat in src_dict.keys():
        if src_dict[cat] == 'raw':
            categories[cat] = basic_gen((paths[0]+'top_'+cat+'.csv'), (paths[1]+cat+'.csv.gz'), msg_brd=150000, src='raw')
       
        elif src_dict[cat] == 'prp':
            categories[cat] = basic_gen((paths[0]+'top_'+cat+'.csv'), (paths[1]+cat+'.csv.gz'), src='prp')
       
        else:
            raise Exception('Unknown source type'+src_dict[cat])

    return categories


def input_gens(count=200, fs_list=[], src='prp',
               paths=['/home/danya/Yandex.Disk/work/data_science/research/prod/sk_tagger/chnls_test/prp/', '/home/danya/Yandex.Disk/work/data_science/research/prod/sk_tagger/chnls_test/raw/']):

    inputs = []

    cnt = 0
    for dump in fs_list:
        cnt += 1
        if cnt <= count:
            if src == 'raw' or src == 'prp':
                ta = basic_gen((paths[0]+'top_'+dump[:-3]), (paths[1]+dump), src=src)
                if ta:
                    inputs.append(ta)
       
            else:
                raise Exception('Unknown source type: '+src)

        else:
            break

    return inputs


class SemanticKernelTagger():
    def __init__(self,
                 com_gen=None,
                 cat_gens=None,
                 top_m=50,
                 top_n=1000):
        self.top_m = top_m
        self.top_n = top_n
        self.categories = {}
        self.common = []
        if com_gen:
            self.load_common(com_gen)
        if cat_gens:
            self.load_categories(cat_gens)

    def load_common(self, gen):
        self.common = [i for i, _ in gen]

    def get_sk(self, gen):
        unigrams = [i for i, _ in gen]
        sk_n_ord = set(unigrams) - set(self.common)
        return [el for el in unigrams if el in sk_n_ord]

    def load_categories(self, gens_dict):
        for key in gens_dict.keys():
            self.categories[key] = self.get_sk(gens_dict[key])

    def _metric(self, top_input, top_supportive):
        if len(top_input):
            return (1 - (len(set(top_input) - set(top_supportive)) / float(len(top_input))))
        else:
            return -1

    def tag(self, gen):
        res = {}
        sk = self.get_sk(gen)
        for cat in self.categories.keys():
            res[cat] = self._metric(sk[:self.top_m], self.categories[cat][:self.top_n])
        return res

