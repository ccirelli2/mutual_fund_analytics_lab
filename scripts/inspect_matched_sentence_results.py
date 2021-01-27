# -*- coding: utf-8 -*-
"""
Purpose:    Identify sentences w/ public health key words


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
import string
import copy
from random import randint
import matplotlib.pyplot as plt

from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

###############################################################################
# Set up logging parameters & Package Conditions
###############################################################################
today = datetime.today().strftime("%d_%m%Y")
logging.basicConfig(level=logging.INFO)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

###############################################################################
# Declare Variables
###############################################################################
dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/matching_sentences'
dir_scripts = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/scripts'
dir_output = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results'
dir_tokenized_sentences = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/get_sentences/tokenized_sentences'
sys.path.append(dir_data)
sys.path.append(dir_scripts)
sys.path.append(dir_output)

###############################################################################
# Import Project Modules
###############################################################################
from functions_utility import *
from functions_decorators import *
import functions_word_search_public_health as m_ph

###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'inspect_matched_sentences')

###############################################################################
# Function Parameters 
###############################################################################
write2file=False
quality_control=True



###############################################################################
# Execute Functions 
###############################################################################
ph_tokens = m_ph.get_public_health_tokens()
nd_tokens = m_ph.get_natural_disaster_tokens()


data = pd.read_excel(dir_data + '/' + 'natural_disaster_sentence_matches.xlsx')
data_tks = data[nd_tokens]

tk_sum = data_tks.sum().reset_index()
tk_sum.rename(columns={'index':'tokens', 0:'Count'}, inplace=True)
tk_sum['pct_total_sentences'] = tk_sum['Count'].values / data_tks.shape[0]
tk_sum.sort_values(by='pct_total_sentences', ascending=False, inplace=True)

plt.bar(x=tk_sum['tokens'].values.tolist(), height=tk_sum['pct_total_sentences'].values)
plt.xticks(rotation='vertical')
plt.grid(b=True)
plt.title('Natural Disaster - Pct Sentence Match By Token')
plt.xlabel('Tokens')
plt.ylabel('Pct Documents')
plt.tight_layout()
plt.show()



