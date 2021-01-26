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
data_test = load_file(
        'sentences_tokenized_iteration_0.csv', dir_tokenized_sentences)
project_folder = create_project_folder(dir_output, 'public_health_sentences')

###############################################################################
# Function Parameters 
###############################################################################
write2file = True

###############################################################################
# Execute Functions 
###############################################################################
ph_tokens = m_ph.get_public_health_tokens()


###############################################################################
# Iterate Chunked Files & Match PH Tokens
###############################################################################
"""
for i in range(10):
    chunk_filename = f'sentences_tokenized_iteration_{i}.csv'
    chunk_data = load_file(chunk_filename, dir_tokenized_sentences)
    
    # Run Function
    get_sentences_matching_tokens(chunk_data, ph_tokens, i, dir_output,
        project_folder, write2file)
"""

###############################################################################
#   Get Metrics On Tokenized Files 
###############################################################################

@my_timeit                                                                      
def get_sentences_matching_tokens(data, tokens, iteration, dir_output,          
        project_folder, write2file):                                            
    """                                                                         
    Identify sentences that contain the list of input tokens.                     
                                                                                
    Args:                                                                       
        data: DataFrame; Rows = each row is a tokenized sentences.
                A primary key links the sentence to the original paragraphs.
        tokens: List; contains lowercase single ngram tokens                                 
        interation : Int; because the tokenized sentences are chunked, the
                iteration value is passed to the write2file function to match
                each input file to output.
        dir_output:                                                           
        project_folder:                                                         
        write2file: Boolean; Whether to write to file or not.

    Return:                                                                     
    -------------                                                               
    data with the addition of columns for each of the n tokens containing
    binary values that represent a match with the sentence or not.
    """                                                                         
    logging.info(f'---- dataset shape => {data.shape}')
    ##########################################################################  
    # Result Object                                                             
    ##########################################################################  
    unverified_match = []
    pkey_verify = []
    sent_counter = 0

    ###########################################################################
    # Get Unverified Match of Tokens
    ###########################################################################
    # Iterate Pkey & Sentences
    for pkey, sent in zip(data['accession#'].values, data['sentences'].values):
        # Record Primary Key
        pkey_verify.append(pkey)
        # Token Counter
        tokens_cp = copy.deepcopy(tokens)
        # Iterate Tokens
        for tk in tokens:
            # Remove Token From List
            tokens_cp.pop(tokens_cp.index(tk))
            # If list not empty
            if tokens_cp:
                if tk in sent:
                    logging.debug('---- match found')
                    unverified_match.append(1)
                    break
            else:
                logging.debug(f'---- no match found')
                unverified_match.append(0)
    
    # Add Unverified Match to Data
    data['unverified_match'] = unverified_match

    # Lim Data To Only Sentences W/ Prelim Match
    data_lim = data[data['unverified_match'] == 1]
    
    # Log number of matches
    logging.info(f'---- number of sent containing token => {data_lim.shape[0]}')
    
    ###########################################################################
    # Get Verified Match of Tokens
    ###########################################################################
    
    # Result Object
    tk_match_dict = {x:[] for x in tokens}

    # Iterate Sentences
    for sent in data_lim['sentences'].values:
        # Clean & Tokenize Sentence                                             
        sent_clean_tok = m_ph.clean_tok_sentence(sent)
    
        # Iterate Tokens                                                        
        for tk in tokens:

            # If Our Token is a 1 Gram                                          
            if len(tk.split(' ')) == 1:
                # Check if token in tokenized sentence
                if tk in sent_clean_tok:
                    # Append Initial Result                                     
                    tk_match_dict[tk].append(1)
                else:
                    tk_match_dict[tk].append(0)

            # Otherwise We need to Create Ngrams of Sentence                    
            else:
                # Tokenize token                                                
                tk_tokenized = tk.split(' ')
                # Create ngram of sentence = len(ph token)                    
                sentence_ngrams = ngrams(sent_clean_tok, len(tk_tokenized))
                # If the ngram of token in ngram of sentence                    
                if tuple(tk_tokenized) in sentence_ngrams:
                    tk_match_dict[tk].append(1)
                else:
                    tk_match_dict[tk].append(0)

    # Create DataFrame With Matching Vectors
    df_tk_matches = pd.DataFrame(tk_match_dict)
    df_tk_matches['accession#'] = data_lim['accession#'].values
   
    logging.info('---- shape dataframe w/ matches => {df_tk_matches.shape}')

    # Join Left Matches w/ Original Dataset 
    df_final = data.merge(df_tk_matches, how='outer', left_on='accession#',
            right_on='accession#')
    # Fill Nan Values w/ Zero
    df_final.fillna(value=0, inplace=True)

    logging.info(f'---- final df shape => {df_final.shape}')

    # Need to figure out how to merge the small subset of
    # matches with original dataset such that the non-missing
    # rows are all set to nan but that the num rows dataset
    # never changes.


data_sample = data_test.sample(frac=0.1, random_state=123)

get_sentences_matching_tokens(data_sample, ph_tokens, 1,
        dir_output, project_folder, write2file)






