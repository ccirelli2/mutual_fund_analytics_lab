# -*- coding: utf-8 -*-
"""


Created on Wed Jan 13 18:23:56 2021
@author: chris.cirelli
"""

###############################################################################
# Import Python Libraries
###############################################################################
import logging
from datetime import datetime
import pandas as pd
import re
import os
import sys
from collections import Counter
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import csv

###############################################################################
# Set up logging parameters & Package Conditions
###############################################################################
today = datetime.today().strftime("%d_%m%Y")
dir_log = r'C:\Users\chris.cirelli\Desktop\repositories\mutual_fund_analytics_lab\reports\logs'
path2file = dir_log + '/' + f'sentence_extraction_{today}.log'
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#logging.basicConfig(filename=path2file, level=logging.INFO)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

###############################################################################
# Declare Variables
###############################################################################
dir_data = r'C:\Users\chris.cirelli\Desktop\repositories\mutual_fund_analytics_lab\data'
dir_scripts = r'C:\Users\chris.cirelli\Desktop\repositories\mutual_fund_analytics_lab\scripts'
dir_output = r'C:\Users\chris.cirelli\Desktop\repositories\mutual_fund_analytics_lab\results'
sys.path.append(dir_scripts)

###############################################################################
# Import Project Modules
###############################################################################c
import functions_sentence_extraction as m_main


###############################################################################
# Import Data
###############################################################################
#data = m_main.load_file('filings.csv', dir_data)

# Preprocessing
data.dropna(subset=['principal_risks'], inplace=True)


project_folder = m_main.create_project_folder(dir_output, 'get_sentences')    


# Data Cleaning Pipeline
data_sample = data.sample(frac=0.1, random_state=1)
sentences = data_sample['principal_risks'].values.tolist()
test_sentence = sentences[0]

for i in sentences:
    print(sentences, '\n')


"""
# Get words with 2 and three dots.
word_two_dot = list(m_main.get_count_word_end_dot(
    data, 0.1, 2, dir_output, project_folder, write2file=False).keys())
word_one_dot = list(m_main.get_count_word_end_dot(
    data, 0.1, 3, dir_output, project_folder, write2file=False).keys())
word_dot_provided = ['dr.', 'mr.', 'bro.', 'bro', 'mrs.', 'ms.',
                    'jr.', 'sr.', 'e.g.', 'vs.', 'u.s.',
                    'etc.', 'j.p.', 'inc.', 'llc.', 'co.', 'l.p.',
                    'ltd.', 'jan.', 'feb.', 'mar.', 'apr.', 'i.e.',
                    'jun.', 'jul.', 'aug.', 'oct.', 'dec.', 's.e.c.',
                    'inv. co. act']
complete_list_word_dots = word_two_dot + word_one_dot + word_dot_provided

punkt_params = PunktParameters()
punkt_params.abbrev_types = set(complete_list_word_dots)
tokenizer = PunktSentenceTokenizer(punkt_params)
tokens = tokenizer.tokenize(test_sentence)

df_sentence = pd.DataFrame({'sentences':tokens})    
m_main.write2csv(df_sentence, dir_output, project_folder, filename='after.csv')
"""











