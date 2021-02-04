import os
import pandas as pd

dir_base = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_data = os.path.join(dir_base, 'data') 

frames = []
for i in range(10):
    frames.append(pd.read_csv(os.path.join(dir_data, f'data_chunk_{i}.csv')))


df_concat = pd.concat(frames)

set_pkey = list(set(df_concat['accession#'].values))

print(len(set_pkey))
