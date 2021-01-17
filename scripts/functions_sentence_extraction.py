# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 18:34:49 2021

@author: chris.cirelli
"""
###############################################################################
# Import Python Libraries
###############################################################################
import logging; logging.basicConfig(level=logging.INFO)
from datetime import datetime
from tqdm import tqdm
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktParameters
import pandas as pd
from tqdm import tqdm
import re
import inspect
from collections import Counter
import os

###############################################################################
# Import Project Modules 
###############################################################################
from functions_utility import *
from functions_decorators import *

###############################################################################
# Function
###############################################################################


@my_timeit                                                                      
def train_nltk_sentence_tokenizer(paragraphs, print_abbrevs=False):       
    """                                                                         
    Function to train NLTK PunctSentTokenizer Class on unique body of text.     
                                                                                
    Supposed to work better than out of box sent tokenizer                      
                                                                                
    Args:
    paragraphs : paragraphs on which to train tokenizer
    print_abbrevs : if you want to print the abbreviations that were
                    identified by the the trained tokenizer
    Returns :                                                                   
    -------------                                                               
    trained sentence tokenizer                                                  
    """                                                                         
    # Ensure that paragraphs are strings                                                           
    paragraphs = [str(x) for x in paragraphs]
    # Join all paragraphs into a single body of text
    raw_text = ''.join(paragraphs)                                              
                                                                                
    # Instantiate & Train Tokenizer Training Class                              
    trainer = PunktTrainer()                                                    
    trainer.train(raw_text)                                                     
    trainer.finalize_training()                                                 
    params = trainer.get_params()                                               
                                                                                
    if print_abbrevs:                                                           
        abbrevs = params.abbrev_types                                           
        print(abbrevs)                                                          
                                                                                
    # Add Trained Parameters To Sentence Tokenizer                              
    sent_tokenizer = PunktSentenceTokenizer(params)                             
                                                                                
    # Return Tokenizer                                                          
    return sent_tokenizer                                                       
                                   


def get_list_words_end_dot_provided():
    return ['dr.', 'mr.', 'bro.', 'bro', 'mrs.', 'ms.',                                
            'jr.', 'sr.', 'e.g.', 'vs.', 'u.s.',                                    
            'etc.', 'j.p.', 'inc.', 'llc.', 'co.', 'l.p.',                          
            'ltd.', 'jan.', 'feb.', 'mar.', 'apr.', 'i.e.',                         
            'jun.', 'jul.', 'aug.', 'oct.', 'dec.', 's.e.c.',                       
            'inv. co. act']  

@my_timeit
def get_tokens_end_dot(data, num, dir_output, project_folder,
                       write2file):
    """
    Function to obtain tokens ending or containing a period.

    Parameters
    ----------
    data : Dataframe
        Contains sentences of interest.
    sample_pct : Float 
        Sample percentage of rows to choose.

    Returns
    -------
    Dictionary with word:count pair.

    """
    
    sentences = data['sentences'].values.tolist()

    # Declare Results Object
    word_end_dot = []

    # Iterate Sample Setences
    for i in tqdm(range(len(sentences))):
        if num == 1:
            regex = re.compile('[a-z]+\.')
        elif num == 2:
            regex = re.compile('[a-z]\.[a-z]\.')
        elif num == 3:
            regex = re.compile('[a-z]\.[a-z]\.[a-z]\.')
        elif num == 4:
            regex = re.compile('[a-z]\.[a-z]\.[a-z]\.[a-z]\.')
        else:
            logging.error('Error: num must be <= 4')
            
        matches = re.findall(regex, sentences[i])
        [word_end_dot.append(x) for x in matches]

    # Get Count of Words ending with a dot (returns dictionary)
    cnt_wrds_end_dot = Counter(word_end_dot)
    
    # Get DataFrame Of Results
    df = pd.DataFrame(cnt_wrds_end_dot, index=['cnt']).transpose()

    # Write 2 file
    if write2file:
        write2csv(df, dir_output, project_folder,
                  f'sample_set_words_ending_{num}_dot.csv')

    # Return Results
    duration = round((datetime.now() - start).total_seconds(), 3)               
    return cnt_wrds_end_dot


@my_timeit
def get_sentences_max_num_tokens_chars(df_sentences, max_num_tokens,
        max_num_chars, dir_output, project_folder, write2file):
    """
    Function to obtain sentences with <= maximum number of characters or tokens.
    """
    logging.info('---- Identifying sentences w/ max tokens {} chars {}'.format(
        max_num_tokens, max_num_chars))

    # <= Max Num Tokens                                                     
    sentences_min_tokens = [                                                
            x for x in df_sentences['sentences'].values                     
            if len(word_tokenize(x)) <= max_num_tokens]                     
    
    df_sent_min_toks = pd.DataFrame.from_dict(Counter(sentences_min_tokens),
            orient='index').rename(columns={0:'Count'}).sort_values(by=     
                    'Count', ascending=False)                               
                                                                            
    # <= Max Num Chars                                                      
    sentences_min_chars = [                                                 
            x for x in df_sentences['sentences'].values                     
            if len(x) <= max_num_chars]                                     
    
    df_sent_min_chars = pd.DataFrame.from_dict(Counter(sentences_min_chars),
            orient='index').rename(columns={0:'Count'}).sort_values(by=     
                    'Count', ascending=False)                               
    
    # Logging                                                               
    logging.info('---- Top sentences <= {} tokens \n{}'.format(           
        max_num_tokens, df_sent_min_toks.head()))                                           
    logging.info('---- Top sentences <= {} chars \n{}'.format(            
        max_num_chars, df_sent_min_chars.head()))

    if write2file:
        filename = 'sentences_max_number_tokens.csv'
        write2csv(df_sent_min_toks, dir_output, project_folder, filename)
        filename = 'sentences_max_number_chars.csv'
        write2csv(df_sent_min_chars, dir_output, project_folder, filename)
    
    # Results
    duration = round((datetime.now() - start).total_seconds(), 3)               
    return df_sent_min_toks, df_sent_min_chars


@my_timeit
def get_incorrectly_tokenized_sentences(df_sentences, dir_output,
        project_folder, write2file):                                                            
    """
    Function that identifies possibly incorrectly tokenized sentences.

    Certain tokens contain periods that may be incorrectly identified by the
    tokenizer and ends of sentences.  This function identifies those tokens
    and checks to see if the tokenized sentences end with them.

    df_sentences : DataFrame; tokenized sentences
    
    Return
    --------
    DataFrame with sentences and tokens

    """
    logging.info(f'---- Testing {df_sentences.shape[0]} tokenized sentences')   
    ###########################################################################
    # Get Tokens Contain One or Two Dots                                       
    ###########################################################################
    tokens_2_dots = get_tokens_end_dot(df_sentences, 2,          
            dir_output, project_folder, write2file)                             
    tokens_3_dots = get_tokens_end_dot(df_sentences, 3,          
            dir_output, project_folder, write2file)                             
    tokens_n_dots = get_list_words_end_dot_provided()                    
    tokens_all_dots = list(tokens_2_dots.keys()) + list(tokens_3_dots.keys()) +\
            tokens_n_dots                                                      
    logging.info('---- Tokens to search for at end of sentence => {}'.format(   
        tokens_all_dots))                                                       
    logging.info('---- Searching for possibly incorrectly tokenized sentences')

    ##########################################################################
    # Identify Sentences Ending In Dot Tokens                                                 
    ##########################################################################
    pkey_list = []
    result_sentences = []                                                       
    result_token = []                                                           
                                                                                
    # Iterate Sentences                                                         
    for i in tqdm(range(df_sentences.shape[0])):
        pkey = df_sentences['accession#'].values.tolist()[i]
        sent = df_sentences['sentences'].values.tolist()[i]                               
        
        # Tokenize Sentence                                                     
        tokens = word_tokenize(sent)                                            
        try:                                                                    
            if ''.join(tokens[-2] + tokens[-1]) in tokens_all_dots:             
                pkey_list.append(pkey)
                result_sentences.append(sent)                                   
                result_token.append(tokens[-2] + tokens[-1])                    
        except IndexError:                                                      
            pass                                                                
                                                                                
    df_results = pd.DataFrame({
        'accession#':pkey_list,
        'sentences': result_sentences,
        'tokens':result_token})
    
    df_tok_frequencey = pd.DataFrame.from_dict(Counter(result_token),
            orient='index')

    if write2file:
        filename = 'sentences_incorrectly_tokenized.csv'
        write2csv(df_results, dir_output, project_folder, filename) 
        filename = 'sentences_incorrectly_tokenized_token_frequency.csv'
        write2csv(df_tok_frequencey, dir_output, project_folder, filename) 
    
    ###########################################################################
    # Return Results
    ###########################################################################
    logging.info('---- Number of possible eroneous sentences => {}'.
        format(df_results.shape[0]))                           
    logging.info('---- Pct of sentences => {}%'.format(                         
        round((df_results.shape[0] / df_sentences.shape[0])*100,2))) 
    
    # Return Results
    return df_results

@my_timeit
def tokenizer_quality_control(df_sentences, max_num_tokens, max_num_chars,      
        dir_output, project_folder, write2file):                                
    """                                                                         
    Function to check the quality of the sentence tokenizer.                    
                                                                                
    Args:                                                                       
        df_sentences: DataFrame; Contains rows w/ sentences                     
        max_num_tokens: Int; Identify sentences <= max num tokens               
        max_num_chars: Int; Identify sentences <= max num chars                 
        dir_output: String; output directory                                    
        project_folder: String;                                                 
        write2file: Boolean                                                     
                                                                                
    Return :                                                                    
        Returns a dataframe with the sentences of interest & a report with      
        metrics on the quality of the tokenization                              
                                                                                
    """                                                                         
    logging.info(f'---- Testing {df_sentences.shape[0]} tokenized sentences')   
                                                                                
    # Get Sentences <= Min Number Tokens or Chars                               
    df_sent_min_toks, df_sent_min_chars =\
            get_sentences_max_num_tokens_chars(df_sentences,          
                    3, 10, dir_output, project_folder, write2file)              
                                                                                
    # Sentences ending in dot & end of sentence                                 
    df_sent_end_dot_toks = get_incorrectly_tokenized_sentences(       
            df_sentences, dir_output, project_folder, write2file)               
                                                                                
    # Return Results                                                            
    return df_sent_min_toks, df_sent_min_chars, df_sent_end_dot_toks 


@my_timeit
def get_paragraphs_for_incorrectly_tokenized_sentences(
        data, df_sentences, dir_output, project_folder, write2file):
    """

    Args:
        data:
        df_sentences:

    """
    
    # Get Primary Keys for Incorrectly Tokenized Sentences
    pkeys = df_sentences['accession#'].values

    # Get Paragraphs
    df_paragraphs = data.merge(df_sentences, left_on='accession#',
            right_on='accession#').rename(columns={'principal_risk':
                'paragraphs'})

    if write2file:
        filename = 'incurrectly_tokenized_paragraphs.csv'
        write2csv(df_paragraphs, dir_output, project_folder, filename)
    
    # Return Results                                                            
    return df_paragraphs

@my_timeit
def sentence_segmenter(data, sample_pct, mode, max_num_tokens, max_num_chars,
        dir_output, project_folder, write2file):
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

    # Results Objects
    result_sentences = []
    result_num_chars_sentence = []
    result_pkey = []                                                            
    logging.info(f'---- Tokenizing {len(list_paragraphs)} Paragraphs')          
                                                                                
    # Iterate Paragraphs & Tokenize Sentences                                   
    for i in tqdm(range(len(list_paragraphs))):                                 
        # Iterate Sentences In Paragraph                                        
        for sentence in sent_tokenize(list_paragraphs[i]):                      
            # Append Results to List Objects                                    
            result_sentences.append(sentence)                                   
            result_num_chars_sentence.append(len(sentence))                     
            result_pkey.append(list_pkeys[i])                                   
                                                                                
    # Construct Results DataFrame                                               
    df_sentences = pd.DataFrame({                                               
        'accession#': result_pkey,                                              
        'sentences': result_sentences,                                          
        'num_chars': result_num_chars_sentence})                                
    
    if mode == 'Test' or mode == 'test':
        # Get Incorrectly Tokenized Sentences & Those With Min Length
        df_sent_min_toks, df_sent_min_chars, df_incorrect_sentences =\
                tokenizer_quality_control(
                        df_sentences, max_num_tokens, max_num_chars,
                        dir_output, project_folder, write2file)
        # Get Paragraphs For Incorrectly Tokenized Sentences
        df_paragraphs_incurrect =\
                get_paragraphs_for_incorrectly_tokenized_sentences(
                        data, df_incorrect_sentences, dir_output,
                        project_folder, write2file)

    if write2file:                                                              
        filename=f'sentences_all_results_sample_pct_{sample_pct}.csv'          
        write2csv(df_sentences, dir_output, project_folder, filename)
                                                                                
    # Return Results                                                            
    return df_sentences                                                         
    













