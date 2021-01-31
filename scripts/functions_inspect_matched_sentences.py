##############################################################################
# Import Python Modules
##############################################################################
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os


##############################################################################
# Declare Variables
##############################################################################
dir_scripts = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/scripts'
sys.path.append(dir_scripts)


##############################################################################
# Import Project Modules
##############################################################################
from functions_utility import *
from functions_decorators import *


##############################################################################
# Functions
##############################################################################


@my_timeit
def concat_sentence_dataframes(data_paragraphs, dir_data, dir_sent_toks,
        dir_results):           
    """
    Function to concatenate all sentence dataframes into a single doc.

    Args:
        data_paragraphs : dataframe with all paragraph data
        dir_data:
        dir_sent_toks:
        dir_results:
    Return:
    ----------------------
    df_merged dataframe.
    """
    ###########################################################################
    # Concatenate Sentence Files                                                
    ###########################################################################
    frames = []                                                                 
    for i in range(10):                                                         
        filename = f'sentences_tokenized_iteration_{i}.csv'                     
        frames.append(load_file(filename, dir_sent_toks))                       
    # Concat Frames                                                             
    logging.info('---- concatanating frames')                                   
    df_concat = pd.concat(frames)                                               
    logging.info('---- finished.')                                              
    
    ###########################################################################
    # Merge Data & Filing Year w/ Sentences                                     
    ###########################################################################
    # Limit Paragraph Data to Primary Key & Filing YEar
    data = data[['pkey_para', 'filing_year']]                                   
    
    df_merged = df_concat.merge(data, left_on='accession#',                     
            right_on='pkey_para')                                               
    ###########################################################################
    # Write df_merged to results                                                
    ###########################################################################
    df_merged.to_csv(os.path.join(                                              
        dir_results, 'sentences_tokenized_all_chunks.csv'))    
    # Return df_merged
    return df_merged



@my_timeit
def get_paragraph_token_counts_by_filing_year(df_paras, df_matches, topic,      
        tokens, dir_output, project_folder, write2file):                 
    """                                                                         
    Function to obtain the count of paragraphs and sentences matches per yr.    
                                                                                
    Args:                                                                       
        df_paras:   DataFrame; paragraph data                                   
        df_matches: DataFrame; sentences matches w/ tokens.                     
        topic :     String;    Ex; public health, natural disaster              
        tokens :    List;      List of tokens as cols in df_matches             
    Returns:                                                                    
    --------------------                                                        
    df_final : DataFrame that contains paragraph & token counts summed          
                by filing year.                                                 
    """                                                                            
    ########################################################################### 
    # Get Count Paragraphs Per Year                                                
    ########################################################################### 
    cnt_paras_peryr = df_paras.groupby('filing_year')['filing_year'].count()    
    # Create Base DataFrame                                                     
    df_base = pd.DataFrame({                                                    
        'filing_year':cnt_paras_peryr.index,                                    
        'cnt_paras':cnt_paras_peryr.values})                                       
    ########################################################################### 
    # Group Sentence Matches By Paragraph Key & Sum Over Token Matches             
    ########################################################################### 
    # Group By Paragraph Key                                                    
    df_matches_bykey = df_matches.groupby(                                      
            'accession#')[tokens].sum().reset_index()                             
    # Append Year to Accession Key                                              
    df_matches_bykey = df_matches_bykey.merge(df_paras[['accession#',           
        'filing_year']], left_on='accession#', right_on='accession#')           
    # Group Matches By Year & Sum Counts                                           
    df_matches_peryr = df_matches_bykey.groupby('filing_year')[tokens].sum()    
                                                                                   
    ########################################################################### 
    # Group Paragraph & Token Sums By Year                                         
    ########################################################################### 
    df_final = pd.merge(df_base, df_matches_peryr, left_on='filing_year',       
            right_on='filing_year')                                             
                                                                                   
    ########################################################################### 
    # Write & Return Results                                                       
    ########################################################################### 
    if write2file:                                                              
        write2csv(df_final, dir_output, project_folder,
                f'{topic}_matches_cnt_by_paragraph_by_year.csv')  
    # Return Df Final                                                           
    return df_final      



@my_timeit
def plot_token_as_pct_paragraph_cnt_by_filing_yr(df_filing_yr,                  
        token, dir_output, project_folder, savefig):                            
    """                                                                         
    Function to plot relationship between token counts and paragraph            
    cnts by filing year.                                                        
                                                                                
    Args:                                                                       
        df_filing_yr: DataFrame; dataframe containing paragraph and token          
                      counts grouped by filing year.                            
        token:        String; name of token and column in dataframe.            
        dir_output:                                                             
        project_folder:                                                         
        savefig:                                                                
                                                                                
    Returns:                                                                    
    ---------------                                                             
    None                                                                        
                                                                                
    """                                                                         
    cnt_disease = df_filing_yr[token].values                            
    cnt_paras = df_filing_yr['cnt_paras'].values                        
    disease_pct_paras = cnt_disease / cnt_paras                                 
                                                                                
    plt.bar(df_filing_yr['filing_year'].values,                         
            disease_pct_paras)                                                  
    plt.title("""Token => {}                                                       
                 Match Cnt By Yr As                                              
                 Pct Paragraph Cnt By Yr""".format(token))                      
    plt.xlabel('Filing Year')                                                   
    plt.ylabel('Pct')                                                           
    plt.grid(b=True)                                                            
    plt.tight_layout()                                                          
    if savefig:                                                                 
        filename = f'{token}_pct_paragraphs_by_filing_yr.jpeg'                  
        plt.savefig(os.path.join(dir_output, project_folder, filename))         
    plt.show()                                                                  
    plt.close()                                                                 
                                                                                
    return None                                                                 
                                                                                








































