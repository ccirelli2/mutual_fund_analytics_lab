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

    The documents are in 10 separate files.  This function simply concats
    those separate documents.

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
    Function to obtain the token matches as an absolute count and percentage
    of the count of paragraphs by filing year.     
                                                                                
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
                                                                                

def get_sum_token_match_freq_as_pct_num_sent_matched(df_sent_matches,           
        df_token_matches, dir_output, project_folder, write2file,               
        pplot, savefig):                                                        
    """                                                                         
    Function to get the ratio of the number of token matches to                 
    number of sentences matched.  So what of matches sentences were             
    comprised by each token.                                                    
                                                                                
    Args:                                                                       
        df_sent_matches: DataFrame; All matched sentences                       
        df_token_matches: DataFrame; Frequency of matched tokens                
        dir_output: String; Output directory                                    
        project_folder:                                                         
        write2file:                                                             
        pplot:                                                                  
        savefig:                                                                
                                                                                
    Returns:                                                                    
                                                                                
    Pandas series w/ sum matches for each token / count matched sentences.         
    """                                                                         
    sum_tok_matches = df_token_freq_by_filing_year[ph_tokens].sum().sort_values(
            ascending=False)                                                    
                                                                                
    tok_match_pct_sent_match = sum_tok_matches / df_sent_matches.shape[0]          
                                                                                
    if pplot:                                                                   
        plt.bar(x=tok_match_pct_sent_match.index,                               
                height=tok_match_pct_sent_match.values)                         
        plt.grid(b=True)                                                        
        plt.title('Sum Token Matches As Pct Total Matched Sentences')           
        plt.xlabel('Tokens')                                                    
        plt.xticks(rotation=90)                                                 
        plt.ylabel('Pct Total Sentences')                                       
        plt.tight_layout()                                                      
        plt.show()                                                              
    # Return results                                                            
    return tok_match_pct_sent_match                                             
                                       




@my_timeit
def get_match_sent_pct_all_sent_by_filing_year(paras, sent_matches,             
        sent_all):                                                              
    """                                                                         
    Function to get the ratio of matches sentences to total sentences by        
    filing year.                                                                
                                                                                
    Args:                                                                       
        paras: DataFrame; all paragraphs and accession key.                     
        sent_all: DataFrame; all sentences                                      
        sent_matches: DataFrame; matches sentences and accession key.           
                                                                                
    Returns:                                                                    
       df_results: DataFrame; includes cnt of sentences, cnt of matched         
        sentences and pct matched sentences by filing year.                     
                                                                                
    """                                                                         
                                                                                
    ########################################################################### 
    # Get Sentence Count By Filing Year                                         
    ########################################################################### 
    sent_cnt_by_yr = sent_all.groupby('filing_year')[                              
            'filing_year'].count()                                                 
                                                                                   
    ########################################################################### 
    # Sentence Matches - Add Filing | Create Binary Match Column                   
    ########################################################################### 
    para_filing_yr = paras = paras[['accession#', 'filing_year']]                  
    sent_matches = pd.merge(                                                       
            sent_matches, paras, left_on='accession#', right_on='accession#')   
    sent_matches['filing_year'] = [                                                
            int(x) for x in df_merged['filing_year'].values]                       
    sent_matches['match_any'] = list(map(lambda x: 1 if x > 0 else x,              
        df_merged['sum_matches'].values))                                          
                                                                                   
    ########################################################################### 
    # Get Ratios : Sum Matches, Sum Se                                             
    ########################################################################### 
    cnt_sentences = sent_all_cnt_by_yr.values                                      
    cnt_sent_matches = sent_matches.groupby('filing_year')['match_any'].sum()   
    pct_sent_matches = (cnt_matches.values / cnt_sentences)*100            

    ########################################################################### 
    # Build Results DataFrame                                                      
    ########################################################################### 
    df_results = pd.DataFrame({                                                    
        'filing_year': cnt_matches.index,                                       
        'cnt_sentences': cnt_sentences,                                         
        'cnt_matches': cnt_matches.values,                                      
        'pct_matches':pct_matches})                                             
                                                                                
    ########################################################################### 
    # Plot Results                                                              
    ########################################################################### 
    plt.bar(x=df_results['filing_year'].values,                                 
            height=df_results['pct_matches'].values, alpha=0.5)                 
    plt.title('Natural Disaster - Pct Matches Sentences By Filing Year')        
    plt.xlabel('Filing Year')                                                   
    plt.ylabel('Pct')                                                           
    plt.grid(b=True)                                                            
    plt.show()                                                                  
                                                                                
    # Return Results DataFrame                                                  
    return df_results  






























