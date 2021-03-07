#!/usr/bin/python

import query_table

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

# FIXME make these function parameters eventually
sql_table = "chat_logs"
sql_query = f"SELECT * FROM {sql_table}"

corpus = query_table.get_data(sql_query, sql_table)

tokenizer = RegexpTokenizer(r"\w+")
stemmer = SnowballStemmer("english")

text = [' '.join([stemmer.stem(word)
                  for word in tokenizer.tokenize(sentence)]) for sentence in corpus]

if True:  # FIXME
    vectorizer = CountVectorizer()
elif False:  # FIXME
    vectorizer = TfidfVectorizer()
elif False:  # FIXME
    # FIXME fix the n_features argument
    vectorizer = HashingVectorizer(n_features=2**4)

X = vectorizer.fit_transform(text)

# from sklearn.model_selection import train_test_split

# X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'])
