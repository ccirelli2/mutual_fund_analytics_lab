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
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'public_health_sentences')

###############################################################################
# Function Parameters 
###############################################################################
write2file = True

###############################################################################
# Execute Functions 
###############################################################################
ph_tokens = m_ph.get_public_health_tokens()



def get_sentences_matching_tokens(data, tokens, iteration, dir_output,
        project_folder, write2file):
    """
    Identify sentences that contain one of the input tokens

    Args:
        data:
        tokens: List; contains lowercase tokens
        dir_output:
        project_folder:
        write2file:
    Return:
    -------------
    Same data w/ additional binary column indicating a match
    """
    ##########################################################################
    # Result Object
    ##########################################################################
    initial_match_flag = []
    match_token = []
    match_pkey = []
    start = datetime.now()
    sent_counter = 0

    ##########################################################################
    # Iterate Sentencess
    ##########################################################################
    
    for pkey, sent in zip(data['accession#'].values,
            data['sentences'].values):
        # Clean & Tokenize Sentence 
        sent_clean_tok = m_ph.clean_tok_sentence(sent)
        match_pkey.append(pkey)
        tok_counter = 0
        #######################################################################
        # Iterate Tokens
        #######################################################################
        for tok in tokens:
            # If Our Token is a 1 Gram
            if len(tok.split(' ')) == 1:      
                if tok in sent_clean_tok:
                    # Append Initial Result
                    initial_match_flag.append(1)
                    match_token.append(tok)
                    break
                else:
                    tok_counter += 1

            # Otherwise We need to Create Ngrams of Sentence
            else:
                # Tokenize token
                tok_tokenized = tok.split(' ') 
                # Create ngram of sentence = len(ph token)
                sentence_ngrams = ngrams(sent_clean_tok, len(tok_tokenized))
                # If the ngram of token in ngram of sentence
                if tuple(tok_tokenized) in sentence_ngrams:
                    initial_match_flag.append(1)
                    match_token.append(tok)
                    break
                else:
                    tok_counter += 1
                
            # Once the counter reachines len(tokens) append no match
            if tok_counter == len(ph_tokens):
                initial_match_flag.append(0)
                match_token.append(None)
                break
            
        # Get Estimated Time to Completion
        if sent_counter == 0:
            duration = (datetime.now() - start).total_seconds()
            est_time = round((duration * data.shape[0])/3600, 0)
            logging.info(f'--- estimation duration in min => {est_time}')
        else:
            if sent_counter%int(0.01 * data.shape[0]) == 0:
                pct_completed = round((sent_counter / data.shape[0])*100, 0)
                logging.info(f'---- pct sentences completed => {pct_completed}%')
        
        # Increas Counter
        sent_counter += 1

    # Quality Check
    logging.info('---- length of match column == num sentences:     {}'.format(
        len(initial_match_flag) == data.shape[0]))
    # Add Match Column to DataFrame
    data['Matching_pkey'] = match_pkey
    data['Verified_pkey'] = data['accession#'].values == data['Matching_pkey'].values
    data['Unverified_Match'] = initial_match_flag
    data['Matching_token'] = match_token
    
    # Write To File
    if write2file:
        filename = f'sentences_public_health_iter_{iteration}.csv'
        write2csv(data, dir_output, project_folder, filename)
    # Return Data
    return data

###############################################################################
# Iterate Chunk Files
###############################################################################


for i in range(10):
    chunk_filename = f'sentences_tokenized_iteration_{i}.csv'
    chunk_data = load_file(chunk_filename, dir_tokenized_sentences)
    
    # Run Function
    get_sentences_matching_tokens(chunk_data, ph_tokens, i, dir_output,
        project_folder, write2file)


















