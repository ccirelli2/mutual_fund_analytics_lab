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
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import sent_tokenize

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
import functions_sentence_extraction as m_main
import functions_utility as m_utility

###############################################################################
# Import Data
###############################################################################
project_folder = m_utility.create_project_folder(dir_output, 'get_sentences')
data = m_utility.load_file('filings.csv', dir_data)


###############################################################################
# Execute Functions 
###############################################################################


def sentence_segmenter(data, sample_pct, dir_output, write2file):
    """
    Function to segment sentences from a body of text.

    Parameters
    ----------
        data :          DataFrame, contains a col of text.
        sample_pct :    Float, Pct by which to sample datset (for testing)
        dir_output :    String, Directory to write output.
        write2file :    Boolean, Whether to write output to file.
    
    Return
    ---------
    DataFrame with rows as sentences
    """
    f_name = inspect.currentframe().f_code.co_name
    start = datetime.now()
    logging.info('###########################################################')
    logging.info(f"""Function '{f_name}' Starting""")
    logging.info('#########################################################\n')

    ###########################################################################
    # Data Preprocessing
    ###########################################################################
    # Drop Na Values in the Principal Risk Column (contains text)
    data.dropna(subset=['principal_risks'], inplace=True)
    # Create Sample of Data
    if sample_pct < 1.0:
        logging.info('---- Creating sample of dataset => {}'.format(
            sample_pct))
        data = data.sample(frac=sample_pct, random_state=1)
    # Get List of Sentences
    list_paragraphs = data['principal_risks'].values.tolist()
    list_pkeys = data['accession#'].values.tolist()
    # Remove Any Non-ASCII Characters (Essentially utf-8 chars)
    list_paragraphs = [
            sentence.encode("ascii", "ignore").decode() for sentence
            in list_paragraphs]
     
    ###########################################################################
    # Get List Words | Acronyms Contain/End w/ dots | Use as Param For Model 
    ###########################################################################
    word_two_dot = list(m_main.get_count_word_end_dot(
        data, 0.1, 2, dir_output, project_folder, write2file=False).keys())
    word_one_dot = list(m_main.get_count_word_end_dot(
        data, 0.1, 3, dir_output, project_folder, write2file=False).keys())
    word_dot_provided = m_main.get_list_words_end_dot_provided()
    # Combine Lists
    complete_list_word_dots = word_two_dot + word_one_dot + word_dot_provided
    logging.info('Complete list of words with dots => {}\n\n'.format(
        complete_list_word_dots))

    ###########################################################################
    # Fit NLTK Sentence Tokenizer & Apply to Sentence 
    ###########################################################################
    logging.info('Fitting NLTK Sentence Tokenizer')
    # Instantiate PunktParameter Class
    punkt_params = PunktParameters()
    # Add List of Words W/ Dots
    punkt_params.abbrev_types = set(complete_list_word_dots)
    # Instantiate Setence Tokenizer & Add Parameters
    #sent_tokenizer = PunktSentenceTokenizer(punkt_params)
    

    ###########################################################################
    # With Fit Model Iteration List of Paragraphs 
    ###########################################################################
    ''' Note: I think we need to carry forward some key to the tokenized
        sentences
    '''
    # Results Object
    result_sentences = []
    result_num_chars_sentence = []
    result_pkey = []
    logging.info(f'---- Tokenizing {len(list_paragraphs)} Paragraphs')
    
    # Iterate Paragraphs & Tokenize Sentences
    for i in tqdm(range(len(list_paragraphs))):
        # Tokenize Test Sentence & Append To Result Object
        #list_sentences = sent_tokenizer.tokenize(list_paragraphs[i])
        list_sentences = sent_tokenize(list_paragraphs[i])
        for sentence in list_sentences:
            result_sentences.append(sentence)
            result_num_chars_sentence.append(len(sentence))
            result_pkey.append(list_pkeys[i])

    # Construct Results DataFrame
    df_sentences = pd.DataFrame({
        'accession#': result_pkey,
        'sentences': result_sentences,
        'num_chars': result_num_chars_sentence})
    
    ###########################################################################
    # Write Results to Output Directory & Return 
    ###########################################################################
    if write2file:
        if sample_pct < 1.0:
            filename=f'test_results_sample_pct_{sample_pct}.xlsx'
        else:
            filename='sentences_all_results.xlsx'
        m_utility.write2excel(df_sentences, dir_output, project_folder, filename)
    # Return Results
    duration = round((datetime.now() - start).total_seconds(), 3)               
    logging.info('Function completed.  Duration => {}\n\n'.format(duration))
    return df_sentences

sentence_segmenter(data, 0.025, dir_output, write2file=True)









