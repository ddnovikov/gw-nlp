import re

import pymorphy2

from collections import Counter

from nltk.util import ngrams


OBSC_PATTERNS = ["([сs]{1}[сsц]{0,1}[uoоуy]{0,5}(?:[ч4]{0,1}[иаakqк][^ц]))",
                 "([а-яa-z]*(?!пло|стра|[тл]и)(\w(?!(у|пло)))*[хx][уy](й|йа|[еeё]|и|я|ли|ю)(?!га)*[а-яa-z]*)",
                 "([а-яa-z]*(п[oо]|[нз][аa])*[хx][eе][рp][а-яa-z]*)",
                 "([а-яa-z]*[мm][уy][дd]([аa][кk]|[oо]|и)[а-яa-z]*)",
                 "([а-яa-z]*д[рp](?:[oо][ч4]|[аa][ч4])(?!л)[а-яa-z]*)",
                 "([а-яa-z]*(?!(?:кило)?[тм]ет)(?!смо)[а-яa-z]*(?<!с)т[рp][аa][хx][а-яa-z]*)",
                 "([а-яa-z]*[к|k][аaoо][з3z]+[eе]?ё?л[а-яa-z]*)",
                 "([а-яa-z]*(?!со)\w*п[еeё]р[нд](и|иc|ы|у|н|е|ы|о)[а-яa-z]*)",
                 "([а-яa-z]*[бп][ссз]д[а-яa-z]+)",
                 "([а-яa-z]*[нnп][аa]?[оo]?[xх][а-яa-z]+)",
                 "([а-яa-z]*([аa]?[оo]?[нnпбз][аa]?[оo]?)?([cс][pр][аa][^зжбсвм])[а-яa-z]*)",
                 "([a-zа-я]*([оo]т|вы|[рp]и|[оo]|и|[уy]){0,1}([пnрp][iиеeё]{0,1}[3zзсcs][дd])[а-яa-z]*)",
                 "([а-яa-z]*(вы)?у?[еeё]?би?ля[дт]?[юоo]?[а-яa-z]*)",
                 "((?!вело|ски|эн)[а-яa-z]*[пpp][eеиi][дd][oaоаеeирp](?![цянгюсмйчв])[рp]?(?![лт])[а-яa-z]*)",
                 "([а-яa-z]*(?!в?[ст]{1,2}еб)(?:(?:в?[сcз3о][тяaа]?[ьъ]?|вы|п[рp][иоo]|[уy]|р[aа][з3z][ьъ]?|к[оo]н[оo])?[её]б[а-яa-z]*)|(?:[а-яa-z]*[хлрдв][еeё]б)[а-яa-z]*)",
                 "([а-яa-z]*[з3z][аaоo]л[уy]п[аaeеин][а-яa-z]*)",
                 "([а-яa-z]*сс?р?[аыуеи][клчунт][а-яa-z]*)"]


def clean_obs(text):
    """ """

    text = re.sub('\n', ' ', text, re.IGNORECASE |
                                   re.VERBOSE | re.UNICODE |
                                   re.DOTALL)

    for ptrn in PATTERNS:
        text = re.sub(ptrn, ' ', text, re.IGNORECASE |
                                       re.VERBOSE | re.UNICODE |
                                       re.DOTALL)

    return text


def clean_text(text):
    '''Regex-based text cleaner.'''

    emoji_pattern = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    text = str(text).lower()
    text = re.sub('^@\w+|\s@\w+|\n@\w+', '', text)  # replies to other users
    text = re.sub('#[\w]+', '', text)  # hashtags
    text = re.sub('https?:\/\/[\S]+|[\w\.-]+\.[a-z]+', '', text)  # links
    text = re.sub('^\/.+', '', text)  # requests to bots
    text = re.sub('\.+', '', text)  # other non-alphabetic
    text = re.sub('[-$%^&*_+|~=`{}\[\]<>\/]', '', text)  # other non-alphabetic
    text = re.sub('.+[^а-яa-z\d\s]', '', text)  # other non-alphabetic

    text = emoji_pattern.sub('', text)
    text = clean_obs(text)

    return text


def tokenize(text, 
             stop_words=None, 
             min_len=1,
             punctuation=False):
    '''Simple tokenizer with stop words filtering.'''

    if not (not text or len(text) == 1):
        if punctuation:
            text = text.strip().split()
        else:
            text = re.split('(\W+)', text.strip())

        if stop_words is not None:
            text = (w for w in text if not w in stop_words)
        return [g[0] for g in list(ngrams(text, 1)) if len(g[0]) > min_len]

    else:
        return []


def count_top_words(word_list, n):
    return Counter(word_list).most_common(n)


def lemmatize(word, lemmatizer):
    if len(lemmatizer.parse(word)) > 1:
        for prs in lemmatizer.parse(word):
            if prs.tag.case == 'nomn':
                return prs.normal_form
            else:
                return self.lemmatizer.parse(word)[0].normal_form

    else:
        return self.lemmatizer.parse(word)[0].normal_form


def preprocess(text, stop_words=None, min_len=1):
    morph = pymorphy2.MorphAnalyzer()
    text = clean_text(text)
    return [lemmatize(i, morph) for i in tokenize(text, stop_words, min_len)]

