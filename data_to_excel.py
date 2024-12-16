import sqlite3
import pandas as pd


def to_excel():
    conn = sqlite3.connect('database.db')
    
    df1 = pd.read_sql_query("SELECT * FROM lego_main", conn)
    df2 = pd.read_sql_query("SELECT * FROM lego_prices", conn)
    df3 = pd.read_sql_query("SELECT * FROM lego_availibity", conn)


    merged_df = pd.merge(df1, df2, on='setID', how='inner')
    merged_df = pd.merge(merged_df, df3, on='setID', how='left')

    merged_df.to_excel('lego_newdata.xlsx', index=False)


    conn.close()

if __name__ == "__main__":
    to_excel()