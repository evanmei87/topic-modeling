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

