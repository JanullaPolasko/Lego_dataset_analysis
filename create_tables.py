import sqlite3

def create_tables():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    cursor.execute("""DROP TABLE IF EXISTS lego_main""")
    cursor.execute("""DROP TABLE IF EXISTS lego_availibity""")
    cursor.execute("""DROP TABLE IF EXISTS lego_prices""")
    cursor.execute("""DROP TABLE IF EXISTS lego_pictures""")
    connection.commit()

    cursor.execute("""CREATE TABLE lego_main (
                        setID INT, 
                        name VARCHAR(255),
                        year INT,
                        theme VARCHAR(255),
                        themeGroup VARCHAR(255),
                        subtheme VARCHAR(255),
                        category VARCHAR(255),
                        pieces INT ,
                        minifigs FLOAT , 
                        packagingType INT ,
                        instructionsCount INT ,
                        minAge INT ,
                        tags VARCHAR(2255),
                        status VARCHAR(255)

                    )""")
    
    cursor.execute("""CREATE TABLE lego_availibity (
                        setID INT, 
                        dateFirstAvailable_US DATE,
                        dateFirstAvailable_UK DATE,
                        dateFirstAvailable_CA DATE,
                        dateFirstAvailable_DE DATE
                    )""")
    
    cursor.execute("""CREATE TABLE lego_prices (
                        setID INT, 
                        US_retailPrice INT,
                        UK_retailPrice INT,
                        CA_retailPrice INT,
                        DE_retailPrice INT,
                        urlPriceHistory VARCHAR(255),
                        actualprice VARCHAR(255)

                    )""")


    cursor.execute("""CREATE TABLE lego_pictures (
                        setID INT,
                        urlPicture VARCHAR(255)
                    )""")
    
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()