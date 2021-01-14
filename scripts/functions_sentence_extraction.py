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
# Functions
###############################################################################



def load_file(filename, directory, project_folder=None):
    """
    Generic function load Excel and CSV files.

    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    directory : TYPE
        DESCRIPTION.
    project_folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    Dataframe

    """
    start = datetime.now()
    logging.info(f'Loading File => {filename}')
    # Define Path 2 File
    if project_folder:
        path = directory + '/' + project_folder + '/' + filename
    else:
        path = directory + '/' + filename

    # Load Data
    if '.csv' in filename:
        data = pd.read_csv(path)
    elif '.xlsx' in filename:
        data = pd.read_excel(path)
    else:
        logging.warning('This function can only load Excel of CSV files')

    # Return data
    duration = round((datetime.now() - start).total_seconds(), 3)
    logging.info('Data loaded.  Shape => {}, Duration => {}\n\n'.format(
        data.shape, duration))
    return data

def write2csv(dataframe, dir_output, project_folder=None, filename=''):
    """
    Generic function write dataframe to csv.

    Parameters
    ----------
    dataframe : TYPE
        DESCRIPTION.
    dir_output : TYPE
        DESCRIPTION.
    filename : TYPE
        DESCRIPTION.
    project_folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    if project_folder:
        path = dir_output + '/' + project_folder + '/' + filename
    else:
        path = dir_output + '/' + filename
    
    dataframe.to_csv(path)
    logging.info(f'---- {filename} writen to directory {dir_output}')
   

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



def create_project_folder(dir_output, name):
    """
    Generic function to create a project folder in the output directory.

    Parameters
    ----------
    dir_output : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    path : TYPE
        DESCRIPTION.

    """
    logging.info(f'Creating project folder => {name}')
    path = dir_output + '/' + name
    try:
        os.mkdir(path)
        logging.info(f'---- Project folder created => {path}\n\n')

    except FileExistsError as err:
        logging.error(f'---- {name} directory already exists\n\n')
    return name            




