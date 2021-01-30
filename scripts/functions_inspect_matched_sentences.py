




"""
data = pd.read_excel(dir_data + '/' + 'natural_disaster_sentence_matches.xlsx')
data_tks = data[nd_tokens]

tk_sum = data_tks.sum().reset_index()
tk_sum.rename(columns={'index':'tokens', 0:'Count'}, inplace=True)
tk_sum['pct_total_sentences'] = tk_sum['Count'].values / data_tks.shape[0]
tk_sum.sort_values(by='pct_total_sentences', ascending=False, inplace=True)

plt.bar(x=tk_sum['tokens'].values.tolist(), height=tk_sum['pct_total_sentences'].values)
plt.xticks(rotation='vertical')
plt.grid(b=True)
plt.title('Natural Disaster - Pct Sentence Match By Token')
plt.xlabel('Tokens')
plt.ylabel('Pct Documents')
plt.tight_layout()
plt.show()
"""
def concat_sentence_dataframes(dir_data, dir_sent_toks, dir_results):           
    # Load DataFile                                                             
    data = pd.read_csv(os.path.join(dir_data, 'filings_clean.csv'))             
    data = data[['pkey_para', 'filing_year']]                                   
                                                                                
    # Concatenate Sentence Files                                                
    frames = []                                                                 
    for i in range(10):                                                         
        filename = f'sentences_tokenized_iteration_{i}.csv'                     
        frames.append(load_file(filename, dir_sent_toks))                       
    # Concat Frames                                                             
    logging.info('---- concatanating frames')                                   
    df_concat = pd.concat(frames)                                               
    logging.info('---- finished.')                                              
                                                                                
    # Merge Data & Filing Year w/ Sentences                                     
    df_merged = df_concat.merge(data, left_on='accession#',                     
            right_on='pkey_para')                                               
    # Write df_merged to results                                                
    df_merged.to_csv(os.path.join(                                              
        dir_results, 'sentences_tokenized_all_chunks.csv'))     
