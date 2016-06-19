import tagger
import pickle
from tagger import Tagger
import pandas as pd
import itertools
import re
import pymorphy2
from nltk.tokenize import wordpunct_tokenize

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()

weights = pickle.load(open('data/dict.pkl', 'rb')) # or your own dictionary
myreader = tagger.Reader() # or your own reader class
mystemmer = tagger.Stemmer() # or your own stemmer class
myrater = tagger.Rater(weights) # or your own... (you got the idea)
mytagger = Tagger(myreader, mystemmer, myrater)
tags = []
f = pd.read_csv('articlesabsctracts.csv', delimiter= ';')
abstracts = f['abstract']
for i in range(len(f['abstract'])-1):
    f['abstract'][i] = re.sub('Abstract', '', f['abstract'][i])

for i in range(len(f['abstract'])-1):
    f['abstract'][i] = re.sub('Summary', '', f['abstract'][i])
abstracts = [clean_str(a) for a in abstracts]
abstracts = [wordpunct_tokenize(a) for a in abstracts]
morph = pymorphy2.MorphAnalyzer()
for i in range(len(abstracts)):
    print (i)
    m = []
    for w in abstracts[i]:
        try:
            lemma = morph.parse(w)[0].normal_form
        except:
            pass
        m.append(lemma)
    abstracts[i] = m

for a in abstracts:
    m = []
    for w in a:
        if len(w)>2:
            m.append(w)
    tags.append(m)

tags_combined = list(itertools.chain.from_iterable(tags))
tags_combined = list(set(tags_combined))
df = pd.DataFrame(False, index = tags_combined, columns =(xrange(len(f)-1)) )

for i in range(len(tags)-1):
    for t in tags[i]:
        df.values[[tags_combined.index(t)], [i]] = True
df.to_csv('index5.csv')