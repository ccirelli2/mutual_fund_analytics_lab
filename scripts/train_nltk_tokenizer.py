# -*- coding: utf-8 -*-
"""

Debugging:
    1.) The NLTK model did not pick up u.s.
        Need to research how to fit the model.



Created on Wed Jan 13 18:23:56 2021
@author: chris.cirelli
"""

###############################################################################
# Import Python Libraries
###############################################################################
import logging
from datetime import datetime
import sys
import pandas as pd
import inspect
from tqdm import tqdm
import time
from collections import Counter
from functools import wraps

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer, PunktParameters

###############################################################################
# Set up logging parameters & Package Conditions
###############################################################################
today = datetime.today().strftime("%d_%m%Y")
dir_log = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/reports/logs'
path2file = dir_log + '/' + f'sentence_extraction_{today}.log'
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
'logging.basicConfig(filename=path2file, level=logging.INFO)'
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

###############################################################################
# Declare Variables
###############################################################################
dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/data'
dir_scripts = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/scripts'
dir_output = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results'
sys.path.append(dir_data)
sys.path.append(dir_scripts)
sys.path.append(dir_output)

###############################################################################
# Import Project Modules
###############################################################################
import functions_sentence_extraction as m_extract
import functions_utility as m_utility
from functions_decorators import *

###############################################################################
# Import Data
###############################################################################
project_folder = m_utility.create_project_folder(dir_output, 'get_sentences')
data = m_utility.load_file('filings.csv', dir_data)

###############################################################################
# Function Parameters 
###############################################################################
function_mode = 'test'
write2file = True
max_num_tokens = 3
max_num_chars = 10
sample_pct = 0.01

###############################################################################
# Execute Functions 
###############################################################################

# Load Incorrect Paragraphs
filename = r'incurrectly_tokenized_paragraphs.csv'
df_paragraphs = m_utility.load_file(filename, dir_output, project_folder)

# Iterate Paragraphs
paragraphs = df_paragraphs['principal_risks'].values
sentences = df_paragraphs['sentences'].values
tokens = df_paragraphs['tokens'].values


print(sentences[0])

"""
trained_tokenizer = m_extract.train_nltk_sentence_tokenizer(
        data, sample_pct, print_abbrevs=False)

para_test = paragraphs[0]
token_test = tokens[0]


sentences = trained_tokenizer.tokenize(para_test)

for sent in sentences:
    if token_test in sent:
        print(f'Problematic Token => {token_test} |', sent, '\n') 
"""












