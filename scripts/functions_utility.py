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
logging.basicConfig(level=logging.INFO)


###############################################################################
# Import Libraries
###############################################################################
import pandas as pd
from tqdm import tqdm
import re
import inspect
from collections import Counter
import os
import sys

###############################################################################
# Add to Path
###############################################################################
dir_scripts = '/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/scripts'
sys.path.append(dir_scripts)

###############################################################################
# Import Project Modules
###############################################################################
from functions_decorators import *



###############################################################################
# Function
###############################################################################


def conn_mysql(password, database):                                             
    host = 'localhost',                                                         
    user='cc2',                                                                 
    password=password,                                                          
    database=database)                                                          
    return mycursor = conn.cursor()



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


@my_timeit
def chunk_csv_file(data, num_chunks, dir_output, write2file):
    """
    Function to create and write to file equal size chunks of csv file.

    Args:
        num_chunks:
        path2file:
        dir_output:
        project_folder:
        write2file:
    Return :
    ----------------
    n number of equal size chunks
    """
    # Calculate Size of Chunks
    chunk_size = (data.shape[0] - (data.shape[0]%num_chunks)) / num_chunks
    logging.info(f'---- creating {num_chunks} chunks of size ~ {chunk_size}')
    # Result Object
    chunks = []
    # Iterate Range & Get Chunks
    count = 0
    for i in tqdm(range(num_chunks)):
        if count < num_chunks: 
            chunk = data.sample(frac=chunk_size)
            logging.info('---- data dimension pre chunk => {data.shape}')
            data = data.drop(axis=0, index=chunk.index)
            logging.info('---- data dimension post chunk => {data.shape}')
            # Append Chunk to list
            chunks.append(chunk)
            # Write Chunk to output directory
            filename = 'data_chunk_{i}.csv'
            path2file = dir_output + '/' + filename
            chunk.to_csv(path2file)
            # Increase Count
            count += 1
        else:
            chunks.append(data)
    














