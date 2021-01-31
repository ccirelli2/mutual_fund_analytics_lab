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
import os
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
# Define directory variables
dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/data'
dir_scripts = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/scripts'
dir_output = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results'
dir_tokenized_sentences = dir_output + r'/get_sentences/tokenized_sentences'
dir_sent_matches = dir_output + r'/matching_sentences'

# Append Directories to path
sys.path.append(dir_data)
sys.path.append(dir_scripts)
sys.path.append(dir_output)

###############################################################################
# Import Project Modules
###############################################################################
import functions_inspect_matched_sentences as m_insp
from functions_utility import *
from functions_decorators import *
import functions_word_search_public_health as m_ph

###############################################################################
# Function Parameters 
###############################################################################
write2file=True
quality_control=True
pplot=True
savefig=True

###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'inspect_matched_toks_natural_disaster')
ph_tokens = m_ph.get_public_health_tokens()
nd_tokens = m_ph.get_natural_disaster_tokens()


###############################################################################
# Functions 
###############################################################################
"""
df_paras = load_file('filings_clean2.csv', dir_data)
df_sent_matches = load_file('natural_disaster_sentence_matches.csv',
        dir_sent_matches)
m_insp.get_paragraph_token_counts_by_filing_year(df_paras, df_sent_matches,
        'natural_disaster', nd_tokens, dir_output, project_folder,
        write2file)
"""

df_filing_yr_results = pd.read_csv(os.path.join(dir_output, project_folder,
    'natural_disaster_matches_cnt_by_paragraph_by_year.csv'))


for token in nd_tokens:
    m_insp.plot_token_as_pct_paragraph_cnt_by_filing_yr(
            df_filing_yr_results, token, dir_output, project_folder,
            savefig)
















































