
###############################################################################
# Import Libraries
###############################################################################
import mysql.connector
import os
import pandas as pd
import numpy as np

###############################################################################
# Directories
###############################################################################
dir_base = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab'
dir_data = os.path.join(dir_base, 'data')
dir_results = os.path.join(dir_base + 'results')
dir_matching_sent = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab/results/matching_sentences'


###############################################################################
# Instantiate Connection to MySQL Database
###############################################################################
conn = mysql.connector.connect(
        host='localhost',
        user='cc2',
        password='Gsu2020!',
        database='mutual_fund_lab')
mycursor = conn.cursor()


###############################################################################
# Import DataFiles 
###############################################################################
"""
df_ph_sentences = pd.read_csv(
        os.path.join(dir_matching_sent, 'public_health_sentence_matches.csv'))
"""
df_paragraphs = pd.read_csv(os.path.join(dir_data, 'filings_clean2.csv'))

###############################################################################
# Insert Statements
###############################################################################

def insert_paragraphs(data):
    count = 0
    for i in range(data.shape[0]):
        vals = data.iloc[i].values.tolist()[1:5]
        sql="""
        INSERT INTO paragraphs (pkey_para, filing_year, fund_name,
        paragraph)
        VALUES(%s, %s, %s, %s);
        """
        try:
            mycursor.execute(sql, vals)
            conn.commit()
            count += 1
        except mysql.connector.errors.ProgrammingError as err:
            print(err)
            count +=1
        except _mysql_connector.MySQLInterfaceError as err:
            print(err)
            count +=1
        if count%1000==0:
            print(f'count => {count}')


insert_paragraphs(df_paragraphs)





def insert_tokenized_senteces(data):
    for i in range(10):
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

def insert_public_health_matching_sentences(conn, mycursor, data):
    sql = """
    INSERT INTO public_health_sentence_matches
        (pkey_para,
        sentences,
        num_chars,
        sent_pkey,
        unverified_match,
        illness,
        preparedness,
        communicable_diseases,
        sars_cov_2,
        epidemic,
        communicable_disease,
        sars,
        public_health,
        coronavirus,
        health_screening,
        health_screenings,
        covid,
        quarantine,
        virus,
        hiv,
        respiratory,
        health_crises,
        prevention,
        mers,
        global_health_crisis,
        h1n1,
        global_health,
        sanitation,
        covid19,
        covid_19,
        pandemic,
        disease,
        influenza,
        global_health_crises,
        pathogen,
        health_crisis,
        sum_matches)

        VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s);
    """
    count = 0
    for i in range(df_ph_sentences.shape[0]):
        vals = df_ph_sentences.iloc[i].values.tolist()[2:]
        vals_ = [] 
        # Sanitize Insertion Values
        for val in vals:
            if isinstance(val, np.int64):
                vals_.append(int(val))
            else:
                vals_.append(val)
        mycursor.execute(sql, vals_)
        conn.commit()
        
        if count%1000 == 0:
            print(f'---- count => {count}')
            count += 1
        else:
            count += 1




