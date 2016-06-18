import nltk
import pandas as pd
import re
import pymorphy2
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

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
    return string.strip().lower()

f = pd.read_csv('articlesabsctracts2.csv')
# nltk.pos_tag(abstracts[0])
vectorizer = TfidfVectorizer(min_df=1)
idf = vectorizer.idf_
abstracts = f['abstract']
abstracts = [clean_str(a) for a in abstracts]
abstracts = [a.lower() for a in abstracts]
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

abstracts_join = [' '.join(a) for a in abstracts]
vectorizer.fit_transform(abstracts_join)
idf = vectorizer.idf_
features = dict(zip(vectorizer.get_feature_names(), idf))
tags = []
