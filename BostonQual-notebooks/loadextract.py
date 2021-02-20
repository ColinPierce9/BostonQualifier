import psycopg2
from sqlalchemy import create_engine
import time
import pandas as pd
import numpy as np

# transfer data to database
def load_data(df, table, index_bool):
    conn_string = 'Put database string here'
    db = create_engine(conn_string)
    conn = db.connect()

    df.to_sql(table, con=conn, if_exists='replace', index=index_bool)

    conn.close()
    db.dispose()

# query all data from database. save result as a dataframe
def extract_data(table):
    conn_string = 'Put database string here'
    db = create_engine(conn_string)
    conn = db.connect()

    df = pd.read_sql_query(f'select * from "{table}"', con=conn)

    conn.close()
    db.dispose()

    return df
