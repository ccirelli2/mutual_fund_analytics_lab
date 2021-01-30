import mysql.connector
import pandas as pd
import os


dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/get_sentences/tokenized_sentences'
#filename = 'filings_clean.csv'
#data = pd.read_csv(os.path.join(dir_data, filename))

conn = mysql.connector.connect(
        host='localhost',
        user='cc2',
        password='Gsu2020!',
        database='mutual_fund_lab')


mycursor = conn.cursor()

for i in range(10):
    data = pd.read_csv(os.path.join(dir_data, f'sentences_tokenized_iteration_{i}.csv'))
    count = 0
    for row in data.itertuples():
        if count == 0:
            print('starting insertions')
        sql = """INSERT INTO sentences(pkey_para, sentence)
                 VALUES ("%s", "%s")"""
        vals = [str(row[2]), str(row[3])]
        mycursor.execute(sql, vals)
        conn.commit()
        if count%1000==0:
            print(f'Count => {count}')
            count += 1
        count += 1




