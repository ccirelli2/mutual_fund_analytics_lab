############################################################################## 
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
# Import Project Modules                                                        
############################################################################### 
import functions_inspect_matched_sentences as m_insp                            
from functions_utility import *                                                 
from functions_decorators import *                                              
import functions_word_search_public_health as m_ph        


############################################################################### 
# Functions                                                        
############################################################################### 

@my_timeit
def get_indv_rows_for_each_tok_sentence(df, sample, dir_output, write2file):       
    """                                                                         
    Function to convert mohits single row of multiple sentences to              
    individual rows for each tokenized sentence.                                
                                                                                
    Args:                                                                       
        df: DataFrame; Contains mohit's results                                 
        sample: Int; Number of samples to take from dataset                     
        dir_output:                                                             
        write2file:                                                             
                                                                                
    Returns:                                                                    
        Dataframe w/ each row representing a single sentence.                   
                                                                                
    """                                                                         
    ##########################################################################  
    # Define Variables                                                          
    ##########################################################################  
    # Sample                                                                    
    df_sample = df.sample(sample, random_state=123)                             
    # Result Objects                                                            
    pkey_list = []                                                              
    sentence_list = []                                                          
                                                                                
    ##########################################################################  
    # Iterate DataFrame, Separate Sentences & Append to list                    
    ##########################################################################  
    for row in df_sample.itertuples():                                          
        pkey = row[1]                                                           
        sent_list = row[2]                                                      
        # Append pkey to list where ntimes = len(sent_list)                     
        [pkey_list.append(pkey) for pkey in range(len(sent_list))]              
        # Append Sentences                                                      
        [sentence_list.append(x) for x in sent_list]                            
    # Create DataFrame                                                          
    df_sep_sent = pd.DataFrame({                                                
        'pkey_para':pkey_list,                                                  
        'sentence':sentence_list})                                              
    # Write to output directory                                                 
    if write2file:                                                              
        write2csv(df_sep_sent, dir_output, 'mohit_seperated_sent.csv')          
    # Return Results                                                            
    return df_sep_sent    
