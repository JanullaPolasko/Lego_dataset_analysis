import sqlite3

def check_correct( columns, table):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = f"DELETE FROM {table} WHERE {' OR '.join([f'{col} IS NULL' for col in columns])}"
    cursor.execute(query)
    cursor.connection.commit()
    print('Data was safely delete')
    connection.close()


def remove_duplicates(table, id_column):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM {table} WHERE rowid NOT IN (SELECT MIN(rowid) FROM {table} GROUP BY {id_column});")
    
    cursor.connection.commit()
    print('Duplicate rows removed successfully.')
    connection.close()


# def convert_dollar_to_euro(columns, table):
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()
    
#     conversion_rate = 0.93726108
    
#     for col in columns:
#         query = f"UPDATE {table} SET {col} = ROUND({col} * {conversion_rate}, 2)"
#         cursor.execute(query)
    
#     cursor.connection.commit()
#     print('Values were successfully converted from dollars to euros.')
#     connection.close()

# def convert_libra_to_euro(columns, table):
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()
    
#     conversion_rate = 1.1711158
    
#     for col in columns:
#         query = f"UPDATE {table} SET {col} = ROUND({col} * {conversion_rate}, 2)"
#         cursor.execute(query)
    
#     cursor.connection.commit()
#     print('Values were successfully converted from libra to euros.')
#     connection.close()

if __name__ == "__main__":
    #vymazanie riadkov ktore neobsahuju kompletne informacie v lego_availibity
    columns_to_check = ['dateFirstAvailable_US', 'dateFirstAvailable_UK', 'dateFirstAvailable_CA', 'dateFirstAvailable_DE']
    check_correct( columns_to_check, 'lego_availibity' )
    
    #vymazanie rovnakych riadkov zo vsetkych tabuliek
    remove_duplicates('lego_availibity', 'setID')
    remove_duplicates('lego_main', 'setID')
    remove_duplicates('lego_prices', 'setID')
    remove_duplicates('lego_pictures', 'setID')

    #prevedenie penazi na rovnaku menu
    # columns_to_convert = ['US_retailPrice', 'CA_retailPrice']
    # convert_dollar_to_euro(columns_to_convert, 'lego_prices')
    # convert_libra_to_euro(['UK_retailPrice'], 'lego_prices')
    
