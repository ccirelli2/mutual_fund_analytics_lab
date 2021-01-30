import mysql.connector
import pandas as pd
import os


dir_data = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/data'
filename = 'filings_clean.csv'
data = pd.read_csv(os.path.join(dir_data, filename))


conn = mysql.connector.connect(
        host='localhost',
        user='cc2',
        password='Gsu2020!',
        database='mutual_fund_lab')


mycursor = conn.cursor()

count = 0
for row in data.itertuples():
    if count == 0:
        print('starting insertions')
    try:
        sql = """INSERT INTO paragraphs(pkey_para, filing_year, fund_name, paragraph)
                 VALUES ("%s", "%s", "%s", "%s")"""
        vals = [str(row[1]), str(int(row[2])), str(row[3]), str(row[4])]
        mycursor.execute(sql, vals)
        conn.commit()
    except ValueError as err:
        print(err)
    if count%1000==0:
        print(f'Count => {count}')
        count += 1
    count += 1




