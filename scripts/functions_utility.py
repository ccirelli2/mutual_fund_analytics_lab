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
    logging.debug(f'---- {filename} writen to directory {dir_output}')


def write2excel(dataframe, dir_output, project_folder=None, filename=''):
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
 
    dataframe.to_excel(path)
    logging.info(f'---- {filename} writen to directory {dir_output}')


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
        logging.warning(f'---- {name} directory already exists\n\n')
    return name            



