import pandas as pd
import sqlite3

def insert_data():
    file_name = 'C:/Users/jjpol/OneDrive/Documents/MAD/lego_final_data.xlsx'
    df = pd.read_excel(file_name)

    connection = sqlite3.connect('database.db')

    for index, row in df.iterrows():
        query = """INSERT OR IGNORE INTO lego_main (
                        setID, 
                        name, 
                        year, 
                        theme, 
                        themeGroup, 
                        subtheme, 
                        category, 
                        pieces, 
                        minifigs,  
                        packagingType, 
                        instructionsCount, 
                        minAge, 
                        tags, 
                        status ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            row['setID'], 
            row['name'], 
            row['year'], 
            row['theme'], 
            row['themeGroup'], 
            row['subtheme'], 
            row['category'], 
            row['pieces'], 
            row['minifigs'], 
            row['packagingType'], 
            row['instructionsCount'], 
            row['minAge'], 
            row['tags'], 
            row['status']
        )
        connection.execute(query, values)
        
    # for index, row in df.iterrows():
        query = """INSERT OR IGNORE INTO lego_availibity (
                        setID,
                        dateFirstAvailable_US,
                        dateFirstAvailable_UK,
                        dateFirstAvailable_CA,
                        dateFirstAvailable_DE )
                    VALUES (?, ?, ?, ?, ?)"""
        values = (
            row['setID'], 
            row['US_dateFirstAvailable'], 
            row['UK_dateFirstAvailable'], 
            row['CA_dateFirstAvailable'], 
            row['DE_dateFirstAvailable']
        )
        connection.execute(query, values)

    for index, row in df.iterrows():
        query = """INSERT OR IGNORE INTO lego_prices (
                        setID,
                        US_retailPrice ,
                        UK_retailPrice ,
                        CA_retailPrice ,
                        DE_retailPrice ,
                        URLpriceHistory )
                    VALUES (?, ?, ?, ?, ?, ?)"""
        values = (
            row['setID'], 
            row['US_retailPrice'],
            row['UK_retailPrice'],
            row['CA_retailPrice'],
            row['DE_retailPrice'],
            row['urlRetailPriceHistoryPLN']
        )
        connection.execute(query, values)

    for index, row in df.iterrows():
        query = """INSERT OR IGNORE INTO lego_pictures (
                        setID)
                    VALUES (?)"""
        values = ( row['setID'], )
        connection.execute(query, values)

    connection.commit() 
    connection.close() 

if __name__ == "__main__":
    insert_data()
