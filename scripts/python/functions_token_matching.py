#########################################################################
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
from nltk.stem import WordNetLemmatizer


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

###############################################################################
# FUNCTIONS 
###############################################################################

@my_timeit
def get_public_health_tokens():
    return ['illness', 'preparedness', 'communicable diseases', 'sars cov 2',
            'epidemic', 'communicable disease', 'sars', 'public health',
            'coronavirus', 'health screening', 'health screenings', 'covid',
            'quarantine', 'virus', 'hiv', 'respiratory', 'health crises',
            'prevention', 'mers', 'global health crisis', 'h1n1',
            'global health', 'sanitation', 'covid19', 'covid 19', 'pandemic',
            'disease', 'influenza', 'global health crises', 'pathogen',
            'health crisis']
 
@my_timeit
def get_natural_disaster_tokens():
    return ['windstorm', 'tornado', 'storm', 'disaster',
            'natural disasters', 'hurricane', 'tornadoe', 'fire',
            'underground', 'volcano', 'natural disaster',
            'environmental', 'tsunami', 'flood', 'death', 'earthquake',
            'cyclone', 'drought', 'seismic', 'cloud', 'lightning']



def clean_tok_sentence(sent):                           
    """
    Function that strips punctuation from string object and returns tokens.
    Args:
        sent:

    Returns:
    
    String object no punctuation.
    """
    # Deal With New Line Characters
    sent = sent.replace('\\n', ' ')
    # Clean Up Punctuation
    punctuation = list(string.punctuation)              
    sent_nopunct = ''.join(list(map(
        lambda x: x if x not in punctuation else ' ', sent)))
    # Tokenize & Lemmatize 
    sent_tok = word_tokenize(sent_nopunct)                     
    lemmer = WordNetLemmatizer()
    lemm_tok = [lemmer.lemmatize(x) for x in sent_tok]
    return lemm_tok


@my_timeit                                              
def get_sentences_matching_tokens(
        data_original, tokens, iteration, dir_output, project_folder,
        write2file, quality_control=False):
    """                                                                         
    Identify sentences that contain the list of input tokens.                     

    Steps:
    Unverified Match : find if any tokens are in sentence.
    Verified Match : Involves actually cleaning and tokenizing sentences
                    and matching one to one with tokens

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
    ##########################################################################  
    # Data Transformations                                                             
    ##########################################################################  
    # Create Deep Copy of dataset
    data_cp = copy.deepcopy(data_original)
    # Add Sentence Primary Key (accession# key is not unique at the sent lvl
    data_cp['sent_pkey'] = [randint(1000000000, 9999999999)
            for x in range(data_cp.shape[0])]

    ##########################################################################  
    # Result Object                                                             
    ##########################################################################  
    unverified_match = []
    sent_counter = 0

    # Logging
    logging.info(f'---- dimensions original dataset => {data_original.shape}')
    logging.info(f'---- number of tokens => {len(tokens)}')

    ###########################################################################
    # Get Unverified Match of Tokens
    ###########################################################################

    # Iterate Pkey & Sentences
    for sent in data_cp['sentences'].values:
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
    data_cp['unverified_match'] = unverified_match

    # Lim Data To Only Sentences Unverified Match 
    data_lim = data_cp[data_cp['unverified_match'] == 1]

    # Log number of matches
    logging.info(f'---- number unverified matches => {data_lim.shape[0]}')

    ###########################################################################
    # Get Verified Match of Tokens
    ###########################################################################
    # Create Empty Result Object
    tk_match_dict = {x:[] for x in tokens}

    # Iterate Sentences
    for sent in data_lim['sentences'].values:
        # Clean & Tokenize Sentence                                             
        sent_clean_tok = clean_tok_sentence(sent)
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
                # Tokenize token (Assumes tokens do not have punctuation)
                tk_tokenized = tk.split(' ')
                # Create ngram of sentence = len(ph token)                    
                sentence_ngrams = ngrams(sent_clean_tok, len(tk_tokenized))
                # If the ngram of token in ngram of sentence                    
                if tuple(tk_tokenized) in sentence_ngrams:
                    tk_match_dict[tk].append(1)
                else:
                    tk_match_dict[tk].append(0)

    ###########################################################################
    # Create Results DataFrame & Join to Original Dataset
    ###########################################################################
    tk_matches = pd.DataFrame(tk_match_dict)
    tk_matches['sent_pkey'] = data_lim['sent_pkey'].values
    # Get Sum of Matches Across Tokens
    tk_col = tk_matches[tokens]
    tk_matches['sum_matches'] = tk_col.sum(axis=1)
    # Limit Tk Matches To Sum > 0
    tk_matches_lim = tk_matches[tk_matches['sum_matches'].values > 0]
    # Merge df_tk_matchs w/ data_lim
    df_final = pd.merge(data_lim, tk_matches_lim, left_on='sent_pkey',
            right_on='sent_pkey')

    if quality_control:
        logging.info(f'---- dim unverified matches before => {data_lim.shape}')
        logging.info(f'---- dim unverified matches after => {tk_matches.shape}')
        logging.info(f'---- dim verified matches => {tk_matches_lim.shape}')
        logging.info(f'---- dim merged data => {df_final.shape}')

    ###########################################################################
    # Write & Return Results 
    ###########################################################################
    if write2file:
        write2csv(data_lim, dir_output, project_folder,
                'unverified_matches.csv')
        write2csv(tk_matches_lim, dir_output, project_folder,
                'verified_matches.csv')
        write2csv(df_final, dir_output, project_folder,
                'original_dataset_verified_matches.csv')
    # Return final dataframe
    return df_final














def get_metrics_tokenized_files():                                              
    # Load Data                                                                    
    dir_results = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/public_health_sentences'
                                                                                
    n_sentences = []                                                            
    n_matches = []                                                              
    tokens = []                                                                 
                                                                                
    # Get Metrics                                                               
    for i in range(10):                                                         
        chunk_results = load_file(f'sentences_public_health_iter_{i}.csv',      
                dir_results)                                                    
        n_sentences.append(chunk_results.shape[0])                                 
        matching_recs = chunk_results[chunk_results['Unverified_Match'] == 1]   
        [tokens.append(x) for x in matching_recs['Matching_token'].values.tolist()]
                                                                                
    # DataFrame Results                                                         
    #df = pd.DataFrame({'n_sentences':n_sentences, 'n_matches':n_matches})      
                                                                                
    cnt = Counter(tokens)                                                       
                                                                                
                                                                                
    from tabulate import tabulate                                               
                                                                                
                                                                                
    df = pd.DataFrame(cnt, index=['cnt'])                                       
    df_final = df.transpose().sort_values(by='cnt', ascending=False)            
                                                                                
    print(tabulate(df_final, headers='keys', tablefmt='psql'))   

























