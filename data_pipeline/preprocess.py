#!/usr/bin/python

import query_table

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

sql_table = "chatlogs"
sql_query = f"SELECT * FROM {table}"

query_table.get_data(sql_query)

tokenizer = RegexpTokenizer(r"\w+")
stemmer = SnowballStemmer("english")

text = [' '.join([stemmer.stem(word)
                  for word in tokenizer.tokenize(sentence)]) for sentence in corpus]

if True:  # FIXME
    vectorizer = CountVectorizer()
elif False:  # FIXME
    vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(text)

# from sklearn.model_selection import train_test_split

# X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'])
