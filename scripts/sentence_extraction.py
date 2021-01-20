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

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

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
from functions_utility import *
from functions_decorators import *


###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output, 'get_sentences')
#data = load_file('filings.csv', dir_data)

###############################################################################
# Function Parameters 
###############################################################################
sent_tok_mode = 'run'
tokenizer = 'custom'
write2file = True
max_num_tokens = 3
max_num_chars = 10
sample_pct = 1.0 

###############################################################################
# Execute Functions 
###############################################################################

# Segment Sentences

@my_timeit
def sentence_segmenter(data, mode, tokenizer, sample_pct, max_num_tokens,
        max_num_chars, dir_output, project_folder, write2file,
        iteration=None):                                
    """                                                                         
    Function to segment sentences from a body of text.                          
                                                                                
    Parameters                                                                  
    ----------                                                                  
        data : DataFrame, contains a col of text.                               
        sample_pct : Float, Pct by which to sample datset (for testing)         
        max_num_tokens : Testing mode.                                          
        max_num_chars : Testing mode                                            
        dir_output : String, Directory to write output.                         
        write2file : Boolean, Whether to write output to file.                  
                                                                                
    Return                                                                      
    ---------                                                                   
    DataFrame with rows as sentences                                            
    """                                                                         
    logging.info(f'---- Running in mode => {mode} v/ tokenizer => {tokenizer}')
    ###########################################################################
    # Prepare Data & Train Tokenizer
    ###########################################################################
    # Drop Na Values in the Principal Risk Column (contains text)               
    data.dropna(subset=['principal_risks'], inplace=True)                       
                                                                                
    # Create Sample of Data                                                     
    if sample_pct < 1.0:                                                        
        logging.info(f'---- Generating Data sample size => {sample_pct}')       
        data = data.sample(frac=sample_pct, random_state=1)                     
                                                                                
    # Get List of Sentences                                                     
    list_paragraphs = data['principal_risks'].values.tolist()                   
    list_pkeys = data['accession#'].values.tolist()                             
                                                                                
    # Remove Any Non-ASCII Characters (Essentially utf-8 chars)                 
    list_paragraphs = [                                                         
            sentence.encode("ascii", "ignore").decode() for sentence            
            in list_paragraphs]

    # Train NLTK Tokenizer
    if tokenizer != 'out-of-box':
        trained_sent_tokenizer = m_extract.train_nltk_sentence_tokenizer(
            list_paragraphs, print_abbrevs=False)

    ###########################################################################
    # Tokenize Sentences
    ###########################################################################
    result_sentences = []                                                       
    result_num_chars_sentence = []                                              
    result_pkey = []                                                            
    logging.info(f'---- Tokenizing {len(list_paragraphs)} Paragraphs')          
                                                                                
    # Iterate Paragraphs & Tokenize Sentences                                   
    for i in tqdm(range(len(list_paragraphs))):                                 
        # Iterate Sentences In Paragraph
        if tokenizer == 'out-of-box':
            tokenized_sentences = sent_tokenize(list_paragraphs[i])
        else:
            tokenized_sentences=\
                    trained_sent_tokenizer.tokenize(list_paragraphs[i])                      
        for sentence in tokenized_sentences:
            # Append Results to List Objects                                    
            result_sentences.append(sentence)                                   
            result_num_chars_sentence.append(len(sentence))                     
            result_pkey.append(list_pkeys[i])          
     
    # Construct Results DataFrame                                               
    df_sentences = pd.DataFrame({                                               
        'accession#': result_pkey,                                              
        'sentences': result_sentences,                                          
        'num_chars': result_num_chars_sentence})                                
    ###########################################################################
    # Run Test Diagnostics
    ###########################################################################
    
    if mode == 'Debug' or mode == 'debug':                                        
        # Get Incorrectly Tokenized Sentences & Those With Min Length           
        df_sent_min_toks, df_sent_min_chars, df_incorrect_sentences=\
                m_extract.tokenizer_quality_control(                                      
                        df_sentences, max_num_tokens, max_num_chars,            
                        dir_output, project_folder, write2file)                 
        # Get Paragraphs For Incorrectly Tokenized Sentences                    
        df_paragraphs_incurrect=\
                m_extract.get_paragraphs_for_incorrectly_tokenized_sentences(
                        data, df_incorrect_sentences, dir_output,               
                        project_folder, write2file)                             
                                                                                
    if write2file:
        if iteration is not None:
            filename=f'sentences_tokenized_iteration_{iteration}.csv'
        else:
            filename=f'sentences_tokenized_sample_pct_{sample_pct}.csv'

        write2csv(df_sentences, dir_output, project_folder, filename)           
                                                                                
    # Return Results                                                            
    return df_sentences    



# Iterate Chunks & Tokenize Sentences
for i in range(10):
    chunk = load_file(f'data_chunk_{i}.csv', dir_data) 
    sentence_segmenter(
            chunk, sent_tok_mode, tokenizer, sample_pct, max_num_tokens,
            max_num_chars, dir_output, project_folder, write2file,
            iteration=i)                                





