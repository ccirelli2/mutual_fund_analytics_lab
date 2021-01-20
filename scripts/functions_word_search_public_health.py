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

###############################################################################
# FUNCTIONS 
###############################################################################

def get_public_health_tokens():
    return ['communicable diseases', 'communicable disease', 'health crises','pandemic',
            'pandemics', 'respiratory', 'illness', 'illnesses', 'prevention',
            'epidemic', 'epidemics', 'coronavirus', 'viruses', 'health crisis',
            'pandemics','sanitation','global health crises', 'covid',
            'health screenings', 'health screening', 'pathogens', 'pathogen', 'sars',
            'global health crisis', 'covid 19', 'covid19', 'hiv','preparedness',
            'sars cov 2', 'epidemics','disease', 'diseases', 'influenza',
            'public health','virus','global health', 'mers',
            'quarantines','h1n1','viruses']


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
    sent_nopunct = ''.join(list(map(lambda x: x if x not in punctuation else ' ', sent)))         
    return word_tokenize(sent_nopunct)                     




































