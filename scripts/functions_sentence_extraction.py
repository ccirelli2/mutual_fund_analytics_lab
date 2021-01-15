# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 18:34:49 2021

@author: chris.cirelli
"""

###############################################################################
# Set up logging parameters
###############################################################################
import logging
from datetime import datetime
today = datetime.today().strftime("%d_%m%Y")
dir_output = r'C:\Users\chris.cirelli\Desktop\repositories\mutual_fund_analytics_lab\reports\logs'
path2file = dir_output + '/' + f'sentence_extraction_{today}.log'
logging.basicConfig(filename=path2file, level=logging.INFO)


###############################################################################
# Import Libraries
###############################################################################
import pandas as pd
from tqdm import tqdm
import re
import inspect
from collections import Counter
import os

###############################################################################
# Function
###############################################################################


def get_list_words_end_dot_provided():
    return ['dr.', 'mr.', 'bro.', 'bro', 'mrs.', 'ms.',                                
        'jr.', 'sr.', 'e.g.', 'vs.', 'u.s.',                                    
        'etc.', 'j.p.', 'inc.', 'llc.', 'co.', 'l.p.',                          
        'ltd.', 'jan.', 'feb.', 'mar.', 'apr.', 'i.e.',                         
        'jun.', 'jul.', 'aug.', 'oct.', 'dec.', 's.e.c.',                       
        'inv. co. act']  


def get_count_word_end_dot(data, sample_pct, num, dir_output, project_folder,
                           write2file):
    """
    Function to obtain count of words ending in a period or dot.

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    sample_pct : TYPE
        DESCRIPTION.

    Returns
    -------
    Dictionary with word:count pair.

    """
    f_name = inspect.currentframe().f_code.co_name
    start = datetime.now()
    logging.info('###########################################################')
    logging.info(f"""Function '{f_name}' Starting""")
    logging.info('###########################################################')

    ###########################################################################
    # Get Sample of data
    ###########################################################################
    data_sample = data.sample(frac=sample_pct, random_state=1)
    sample_sentences = data_sample['principal_risks'].values.tolist()

    # Declare Results Object
    word_end_dot = []

    # Iterate Sample Setences
    for i in tqdm(range(len(sample_sentences))):
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
            
        matches = re.findall(regex, sample_sentences[i])
        [word_end_dot.append(x) for x in matches]

    # Get Count of Words ending with a dot
    cnt_wrds_end_dot = Counter(word_end_dot)

    # Write 2 file
    if write2file:
        df = pd.DataFrame(
            cnt_wrds_end_dot,
            index=['cnt']).transpose()
        write2csv(df, dir_output, project_folder,
                  f'sample_set_words_ending_{num}_dot.csv')

    ###########################################################################
    # Return Results
    ###########################################################################
    duration = round((datetime.now() - start).total_seconds(), 3)
    logging.info('Function completed.  Duration => {}\n\n'.format(duration))
    return cnt_wrds_end_dot


