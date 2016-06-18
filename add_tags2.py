import tagger
import pickle
from tagger import Tagger
import pandas as pd
import re


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
f = pd.read_csv('articlesabsctracts2.csv')
abstracts = f['abstract']
abstracts = [clean_str(a) for a in abstracts]
for a in abstracts:
	tags.append(mytagger(a))

for i in range(len(tags)-1):
	tags[i] = [str(w)[1:-1] for w in tags[i]]

tags_combined = []
for tag in tags:
	tags_combined += tag

df = pd.DataFrame(False, index = tags_combined, columns =(xrange(len(f)-1)) )

for i in range(len(tags)-1):
	for t in tags[i]:
		df.values[[tags_combined.index(t)], [i]] = True