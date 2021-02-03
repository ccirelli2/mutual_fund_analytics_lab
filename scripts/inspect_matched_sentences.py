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
from tabulate import tabulate

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
dir_base = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_data = os.path.join(dir_base, 'data')
dir_scripts = os.path.join(dir_base, 'scripts')
dir_output = os.path.join(dir_base, 'results')
dir_tokenized_sentences = os.path.join(dir_output, 'get_sentences/tokenized_sentences')
dir_sent_matches = os.path.join(dir_output, 'matching_sentences')
dir_ph_matches = os.path.join(dir_output, 'inspect_matched_toks_public_health')

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
"""
f_token_freq_by_filing_year = load_file(
        'public_health_matches_cnt_by_paragraph_by_year.csv',
        dir_ph_matches)
df_paras = load_file('filings_clean2.csv', dir_data)
df_sent_matches = load_file('natural_disaster_sentence_matches.csv',
        dir_sent_matches)
df_filing_yr_results = pd.read_csv(os.path.join(dir_output, project_folder,
    'natural_disaster_matches_cnt_by_paragraph_by_year.csv'))
"""
df_sent_matches = load_file('natural_disaster_sentence_matches.csv',
        dir_sent_matches)
df_paras = load_file('filings_clean2.csv', dir_data)
df_sent_all = pd.read_csv(os.path.join(dir_tokenized_sentences,
    'sentences_tokenized_all_chunks.csv'))


project_folder = create_project_folder(
        dir_output, 'inspect_matched_toks_natural_disaster')
ph_tokens = m_ph.get_public_health_tokens()
nd_tokens = m_ph.get_natural_disaster_tokens()


###############################################################################
# Functions 
###############################################################################
"""
# Load concatenated sentences
m_insp.get_paragraph_token_counts_by_filing_year(df_paras, df_sent_matches,
        'natural_disaster', nd_tokens, dir_output, project_folder,
        write2file)

# Generate Frequency Plots For Each Token Over Filing years
for token in nd_tokens:
    m_insp.plot_token_as_pct_paragraph_cnt_by_filing_yr(
            df_filing_yr_results, token, dir_output, project_folder,
            savefig)
"""



def get_match_sent_pct_all_sent_by_filing_year(df_paras, df_sent_matches,
        df_sent_all):

    # Get Count All Tokenized Sentences By Filing Year
    df_sent_all_cnt_by_yr = df_sent_all.groupby('filing_year')[
            'filing_year'].count()

    # Append Filing Year To Matched Sentences
    df_paras = df_paras[['accession#', 'filing_year']]
    df_merged = pd.merge(df_sent_matches, df_paras, left_on='accession#',
            right_on='accession#')

    # Clean Up Matched Sent Columns
    df_merged['match_any'] = list(map(lambda x: 1 if x > 0 else x,
        df_merged['sum_matches'].values))
    df_merged['filing_year'] = [int(x) for x in df_merged['filing_year'].values]

    # Calculations
    cnt_matches = df_merged.groupby('filing_year')['match_any'].sum()
    cnt_sentences = df_sent_all_cnt_by_yr.values
    pct_matches = (cnt_matches.values / cnt_sentences)*100

    # Build Results DataFrame
    df_results = pd.DataFrame({
        'filing_year': cnt_matches.index,
        'cnt_sentences': cnt_sentences,
        'cnt_matches': cnt_matches.values,
        'pct_matches':pct_matches})

    # Plot Results
    plt.bar(x=df_results['filing_year'].values,
            height=df_results['pct_matches'].values, alpha=0.5)
    plt.title('Natural Disaster - Pct Matches Sentences By Filing Year')
    plt.xlabel('Filing Year')
    plt.ylabel('Pct')
    plt.grid(b=True)
    plt.show()
    
    print(df_results)

    # Return Results DataFrame
    return df_results

get_match_sent_pct_all_sent_by_filing_year(df_paras, df_sent_matches,
        df_sent_all)













