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
import sys
import pandas as pd
import inspect
import string
import copy
import time
from tqdm import tqdm
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
from random import randint
from tabulate import tabulate
import mysql.connector


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
# Create Directory Paths 
###############################################################################
dir_base = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_results = os.path.join(dir_base, 'results')
dir_data = os.path.join(dir_base, 'data')
dir_scripts = os.path.join(dir_base, 'scripts')
dir_output = os.path.join(dir_base, 'results')
dir_tokenized_sentences = os.path.join(dir_output,
        'get_sentences/tokenized_sentences')
dir_sent_matches = os.path.join(dir_output, 'matching_sentences')
dir_ph_matches = os.path.join(dir_output, 'inspect_matched_toks_public_health')
# Append Directories to path
list_dirs = [dir_base, dir_data, dir_scripts, dir_tokenized_sentences,
        dir_sent_matches, dir_ph_matches]
[sys.path.append(d) for d in list_dirs]

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

conn, my_cursor = conn_mysql('Gsu2020!', 'mutual_fund_lab')


























