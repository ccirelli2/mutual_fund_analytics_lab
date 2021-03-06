# -*- coding: utf-8 -*-
"""
Purpose : Compare the sentence tokenized results provided by mohit

Created on Wed Jan 13 18:23:56 2021
@author: chris.cirelli
"""

###############################################################################
# Import Python Libraries
###############################################################################
import logging
import csv
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
from nltk.corpus import stopwords
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
# Define directory variables
dir_repo = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_data = os.path.join(dir_repo, 'data')
dir_scripts = os.path.join(dir_repo, 'scripts')
dir_output = os.path.join(dir_repo, 'results')
dir_tokenized_sentences = os.path.join(dir_output,
        'get_sentences/tokenized_sentences')
dir_sent_matches = os.path.join(dir_output, 'matching_sentences')
dir_mohit = os.path.join(dir_output, 'mohit')

# Append Directories to path
sys.path.append([dir_data, dir_repo, dir_scripts, dir_output,
    dir_tokenized_sentences, dir_sent_matches, dir_mohit])


###############################################################################
# Import Project Modules
###############################################################################
import functions_inspect_matched_sentences as m_insp
from functions_utility import *
from functions_decorators import *
import functions_word_search_public_health as m_ph

###############################################################################
# Connect to DataBase 
###############################################################################
conn, mycursor = conn_mysql('Gsu2020!', 'mutual_fund_lab')


###############################################################################
# Import Data
###############################################################################
project_folder = create_project_folder(dir_output,
        'inspect_public_health_paragraph_lexicon')
ph_tokens = m_ph.get_public_health_tokens()
nd_tokens = m_ph.get_natural_disaster_tokens()


logging.info('---- loading sql data')
query_ph = """
            SELECT t1.pkey_para
                  ,t1.filing_year
                  ,t1.paragraph
            FROM paragraphs AS t1
            JOIN public_health_sentence_matches AS t2 ON
            SUBSTRING(t1.pkey_para, 2, 20) = t2.pkey_para   
        """
df_paras = pd.read_sql(query_ph, conn)

###############################################################################
# Function Parameters 
###############################################################################
write2file=True
quality_control=True
pplot=True
savefig=True

###############################################################################
# Functions 
###############################################################################

def tokenize_clean_public_health_text(df_paras):
    # Raw Text
    logging.info('---- concatenating text')
    text = ''.join(df_paras['paragraph'].values.tolist())
    # Strip Punctuation
    logging.info('---- stripping punctuation')
    punctuation = string.punctuation
    text = ''.join(list(map(lambda x: x if x not in punctuation else ' ', text)))
    # Tokenize Text
    logging.info('---- tokenizing text')
    tokens = word_tokenize(text)
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Lemmatize Tokens
    logging.info('---- lematizing text')
    lemmer = WordNetLemmatizer()
    tokens = [lemmer.lemmatize(tok) for tok in tokens]
    # Strip out 3 letter tokens
    logging.info('--- stripping 3 letter tokens')
    tokens = [x for x in tokens if len(x) >3]
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Strip Stopwords
    logging.info('---- striping stop words')
    stop_words_english = stopwords.words('english')
    tokens = [x for x in tokens if x not in stop_words_english]
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Create DataFrame & Write to file
    logging.info('---- writing tokens to project folder')
    df_tokens = pd.DataFrame({'tokens':tokens})
    filename = 'public_health_paragraph_tokens.csv'
    df_tokens.to_csv(os.path.join(dir_output, project_folder,
        filename))
    return filename




def tokenize_clean_ngrams_public_health_text(df_paras, num_grams):
    # Raw Text
    logging.info('---- concatenating text')
    text = ''.join(df_paras['paragraph'].values.tolist())
    # Strip Punctuation
    logging.info('---- stripping punctuation')
    punctuation = string.punctuation
    text = ''.join(list(map(lambda x: x if x not in punctuation else ' ', text)))
    # Tokenize Text
    logging.info('---- tokenizing text')
    tokens = word_tokenize(text)
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Lemmatize Tokens
    logging.info('---- lematizing text')
    lemmer = WordNetLemmatizer()
    tokens = [lemmer.lemmatize(tok) for tok in tokens]
    # Strip out 3 letter tokens
    logging.info('--- stripping 3 letter tokens')
    tokens = [x for x in tokens if len(x) >3]
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Strip Stopwords
    logging.info('---- striping stop words')
    stop_words_english = stopwords.words('english')
    tokens = [x for x in tokens if x not in stop_words_english]
    logging.info('---- num tokens => {}'.format(len(tokens)))
    # Ngrams
    tokens_grams = ngrams(tokens, num_grams)
    # Create DataFrame & Write to file
    logging.info('---- writing tokens to project folder')
    df_tokens = pd.DataFrame({'tokens':tokens_grams})
    filename = 'public_health_paragraph_{}gram_tokens.csv'.format(
            num_grams)
    df_tokens.to_csv(os.path.join(dir_output, project_folder,filename))
    return filename

filename = tokenize_clean_ngrams_public_health_text(df_paras, num_grams=2)


def create_frequency_table(filename):
    logging.info('---- load csv file')
    df_para_tokens = pd.read_csv(os.path.join(dir_output, project_folder,
        filename))

    logging.info('---- creating frequency table')
    cnt_tokens = Counter(df_para_tokens['tokens'].values.tolist())

    logging.info('---- creating dataframe from frequency table')
    df_token_freq = pd.DataFrame(cnt_tokens, index=['cnt']).transpose()
    df_token_freq.sort_values(by='cnt', ascending=False, inplace=True)


    logging.info('---- writing results to output directory')
    df_token_freq.to_excel(os.path.join(dir_output, project_folder,
        'public_health_2gram_token_freq.xlsx'))


create_frequency_table(filename)
































