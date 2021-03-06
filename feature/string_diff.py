#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn import model_selection
from sklearn import linear_model

from sklearn.metrics import accuracy_score
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


import pandas as pd
import numpy as np
import math
import nltk
import datetime
from collections import Counter
from nltk.corpus import stopwords
from sklearn.metrics import log_loss
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.optimize import minimize
stops = set(stopwords.words("english"))
import xgboost as xgb
from sklearn.cross_validation import train_test_split
import multiprocessing
import difflib
import re
from string import punctuation
import sys

from gensim.models.tfidfmodel import TfidfModel
from gensim.models import Word2Vec
from nltk.corpus import brown
from gensim.models.keyedvectors import KeyedVectors
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from nltk.stem.snowball import SnowballStemmer
from gensim.similarities import MatrixSimilarity
from scipy import spatial
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from scipy.stats import skew, kurtosis


def readData():
    train = pd.read_csv('./input/train.csv')[:]
    test = pd.read_csv('./input/test.csv')[:]
    return train, test


def total_unique_words(row):
    return len(set(row['question1']).union(row['question2']))

def total_unq_words_stop(row, stops =stops):
    return len([x for x in set(row['question1']).union(row['question2']) if x not in stops])

def wc_diff(row):
    return abs(len(row['question1']) - len(row['question2']))

def wc_ratio(row):
    l1 = len(row['question1'])*1.0 
    l2 = len(row['question2'])
    if l2 == 0:
        return np.nan
    if l1 / l2:
        return l2 / l1
    else:
        return l1 / l2

def wc_diff_unique(row):
    return abs(len(set(row['question1'])) - len(set(row['question2'])))

def wc_ratio_unique(row):
    l1 = len(set(row['question1'])) * 1.0
    l2 = len(set(row['question2']))
    if l2 == 0:
        return np.nan
    if l1 / l2:
        return l2 / l1
    else:
        return l1 / l2

def wc_diff_unique_stop(row, stops=stops):
    return abs(len([x for x in set(row['question1']) if x not in stops]) - len([x for x in set(row['question2']) if x not in stops]))

def wc_ratio_unique_stop(row, stops=stops):
    l1 = len([x for x in set(row['question1']) if x not in stops])*1.0 
    l2 = len([x for x in set(row['question2']) if x not in stops])
    if l2 == 0:
        return np.nan
    if l1 / l2:
        return l2 / l1
    else:
        return l1 / l2

def same_start_word(row):
    if not row['question1'] or not row['question2']:
        return np.nan
    return int(row['question1'][0] == row['question2'][0])

def char_diff(row):
    return abs(len(''.join(row['question1'])) - len(''.join(row['question2'])))

def char_ratio(row):
    l1 = len(''.join(row['question1'])) 
    l2 = len(''.join(row['question2']))
    if l2 == 0:
        return np.nan
    if l1 / l2:
        return l2 / l1
    else:
        return l1 / l2

def char_diff_unique_stop(row, stops=stops):
    return abs(len(''.join([x for x in set(row['question1']) if x not in stops])) - len(''.join([x for x in set(row['question2']) if x not in stops])))

def makeFeature(df_features):
    now = datetime.datetime.now()
    print now.strftime('%Y-%m-%d %H:%M:%S') 
    df_features['f_total_unique_words'] = df_features.apply(total_unique_words, axis=1, raw=True)
    df_features['f_total_unq_words_stop'] = df_features.apply(total_unq_words_stop, axis=1, raw=True)
    df_features['f_wc_diff'] = df_features.apply(wc_diff, axis=1, raw=True) 
    df_features['f_wc_ratio'] = df_features.apply(wc_ratio,axis=1, raw=True)
    df_features['f_wc_diff_unique']= df_features.apply(wc_diff_unique, axis=1, raw=True)
    df_features['f_wc_ratio_unique']= df_features.apply(wc_ratio_unique, axis=1, raw=True)
    df_features['f_wc_diff_unique_stop']= df_features.apply(wc_diff_unique_stop, axis=1, raw=True)
    df_features['f_wc_ratio_unique_stop']= df_features.apply(wc_ratio_unique_stop, axis=1, raw=True)
    df_features['f_same_start_word']= df_features.apply(same_start_word, axis=1, raw=True)
    df_features['f_char_diff']= df_features.apply(char_diff, axis=1, raw=True)
    df_features['f_char_ratio']= df_features.apply(char_ratio, axis=1, raw=True)
    df_features['f_char_diff_unique_stop']= df_features.apply(char_diff_unique_stop, axis=1, raw=True)
    now = datetime.datetime.now()
    print now.strftime('%Y-%m-%d %H:%M:%S') 
    return df_features




if __name__ == "__main__":
    train, test = readData()
    train = train.fillna(' ')
    test = test.fillna(' ')

    col = [c for c in train.columns if c[:1] == 'z' or c[:1] == 'f']
    train = makeFeature(train)
    train.to_csv('train_simple.csv', index=False, columns = col)

    test = makeFeature(test)
    test.to_csv('test_simple.csv', index=False, columns = col)
