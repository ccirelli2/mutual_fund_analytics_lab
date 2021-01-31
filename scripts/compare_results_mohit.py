# -*- coding: utf-8 -*-
"""
Purpose : Compare the sentence tokenized results provided by mohit

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
dir_repo = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_data = os.path.join(dir_repo, 'data')
dir_scripts = os.path.join(dir_repo, 'scripts')
dir_output = os.path.join(dir_repo, 'results')
dir_tokenized_sentences = os.path.join(dir_output,
        'get_sentences/tokenized_sentences')
dir_sent_matches = os.path.join(dir_output, 'matching_sentences')

# Append Directories to path
sys.path.append([dir_data, dir_repo, dir_scripts, dir_output,
    dir_tokenized_sentences, dir_sent_matches])


###############################################################################
# Import Project Modules
###############################################################################
import functions_inspect_matched_sentences as m_insp
from functions_utility import *
from functions_decorators import *
import functions_word_search_public_health as m_ph

###############################################################################
# Connect to DataBase 
###############################################################################





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

mycursor = conn_mysql('Gsu2020!', 'mutual_fund_lab')







































