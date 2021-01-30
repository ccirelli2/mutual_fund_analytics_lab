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
import functions_word_search_public_health as m_ph

###############################################################################
# Function Parameters 
###############################################################################
write2file=False
quality_control=True

###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'inspect_matched_sentences')
ph_tokens = m_ph.get_public_health_tokens()
nd_tokens = m_ph.get_natural_disaster_tokens()


###############################################################################
# Execute Functions 
###############################################################################

dir_matches = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/matching_sentences'
df_matches = pd.read_csv(os.path.join(dir_matches, 'public_health_sentence_matches.csv'))
df_paras = pd.read_csv(os.path.join(dir_data, 'filings_clean2.csv'))

# Merge Filing Year On to Sentence Matches
#df_paras = df_paras[['accession#', 'filing_year']]
#df_matches = df_matches.merge(df_paras, left_on='accession#',
#        right_on='accession#')


#**** Need dictionary to map like tokens to single column

def get_matches_as_pct_paragraphs_per_yr(df_paras, df_matches):
    # Step 1: Get Count Paragraphs Per Year
    cnt_paras_peryr = df_paras.groupby('filing_year')['filing_year'].count()
    # Create Base DataFrame
    df_base = pd.DataFrame({
        'filing_year':cnt_paras_peryr.index,
        'cnt_paras':cnt_paras_peryr.values})
    
    # Step 2: Group Matches By Accession Key & Sum
    toks = ['illness', 'preparedness',
       'communicable diseases', 'sars cov 2', 'epidemic',
       'communicable disease', 'sars', 'public health', 'coronavirus',
       'health screening', 'health screenings', 'covid', 'quarantine', 'virus',
       'hiv', 'respiratory', 'health crises', 'prevention', 'mers',
       'global health crisis', 'h1n1', 'global health', 'sanitation',
       'covid19', 'covid 19', 'pandemic', 'disease', 'influenza',
       'global health crises', 'pathogen', 'health crisis']
    
    df_matches_bykey = df_matches.groupby(
            'accession#')[toks].sum().reset_index()

    # Step 3: Append Year to Accession Key
    df_matches_bykey = df_matches_bykey.merge(df_paras[['accession#',
        'filing_year']], left_on='accession#', right_on='accession#')

    # Step 4: Get Sum Token Matches Per Year At Paragraph Lvl
    df_matches_peryr = df_matches_bykey.groupby('filing_year')[toks].sum()

    # Step 5: Merge Paragraph Count By Year & Matches By Year
    df_final = pd.merge(df_base, df_matches_peryr, left_on='filing_year',
            right_on='filing_year')

    df_final.to_csv(os.path.join(
        dir_output, 'public_health_matches_cnt_by_paragraph_by_year.csv'))


get_matches_as_pct_paragraphs_per_yr(df_paras, df_matches)


























