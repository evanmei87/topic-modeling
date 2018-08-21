import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

# Plotting
import pyLDAvis
import pyLDAvis.gensim  
import matplotlib.pyplot as plt

# Enable logging for gensim
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# Natural language processing stop words
import nltk
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

dataset = pd.read_csv('dataset.csv')
data = dataset.combined_text.tolist()

# Remove new line characters
data = [re.sub('\s+', ' ', sent) for sent in data]

# Remove single quotes
data = [re.sub("\'", "", sent) for sent in data]

# Delete website links
data = [re.sub(r'http\S+', '', str2) for str2 in data]

# Delete [removed] comments which are commmon in reddit threads
data = [str3.replace(' [removed] ', ' ') for str3 in data]

def tokenize(text):
    """ Tokenize document into a list of words that can be processed by our topic models
    
    Arguments:
        text {list<String>} -- A document  
    
    Returns:
        list <String> -- A list of all the words in the sentence without the new line characters and punctuation marks
    """

    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif not token.orth_.isalnum():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def remove_stopwords(texts):
    """ Process the text to remove stop words which will increase our model's accuracy
    
    Arguments:
        text {list<String>} -- A list of word tokens from a single thread/document
    
    Returns:
        list<String> -- The input list without the unnessecary stop words
    """

    return [word for word in simple_preprocess(str(texts)) if word not in stop_words]

def get_lemma(doc):
    """ Reduce inflectional forms and derive root base form of a word for each token in the docs
    
    Arguments:
        doc {list<String>} -- A list of word tokens from a single thread/document
    
    Returns:
        list<String> -- The input list where all the tokens are morphed into the root of the word
    """

    phrases = []
    for word in doc:
        lemma = wn.morphy(word)
        if lemma is None:
            phrases.append(word)
        else:
            phrases.append(lemma)
    return phrases

def prepare_for_model(data):
    """ Pre-process the text data into digestable tokens for the lda model
    
    Arguments:
        data {list<String>} -- List of document texts
    
    Returns:
        {list<list<String>>} -- List of a List of all the words for every document in the data
    """

    tokens = [tokenize(document) for document in data]
    no_stop_words = [remove_stopwords(doc)  for doc in tokens]
    data_lemmatized = [get_lemma(doc) for doc in no_stop_words ]
    return data_lemmatized

print(data)
print(prepare_for_model(data))