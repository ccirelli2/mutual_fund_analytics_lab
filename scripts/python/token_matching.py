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
dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/data'
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
import functions_token_matching as m_ph

###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'public_health_sentences')

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

###############################################################################
# Iterate Chunked Files & Match PH Tokens
###############################################################################

frames = []

for i in range(10):
    logging.info(f'---- iteration => {i}')
    chunk_filename = f'sentences_tokenized_iteration_{i}.csv'
    chunk_data = load_file(chunk_filename, dir_tokenized_sentences)
    
    # Run Function
    df_iter_result = m_ph.get_sentences_matching_tokens(
            chunk_data, ph_tokens, i, dir_output, project_folder,
            write2file, quality_control)
    # Append Result DataFrame to Frames
    frames.append(df_iter_result)

# Concatenate Results
df_concat = pd.concat(frames)

# Logging
logging.info(f'---- final concatenated results dim => {df_concat.shape}')

# Write Results to File
write2excel(df_concat, dir_output, project_folder,
        'public_health_sentence_matches.xlsx')








