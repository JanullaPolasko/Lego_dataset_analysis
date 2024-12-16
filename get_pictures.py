import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import random

def get_picture(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]
    header = {"User-Agent": random.choice(user_agents)}
    
    try:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        div =  soup.find('div', class_='text-center pt-3')
        image = div.find('img', class_ = 'img-fluid')
        src = image.get('src')
        if src is not None:
            return 'https://promoklocki.pl/' + src
        return None
        
    except Exception as e:
        print(f"Chyba pri získavaní ceny zo stránky pre setID {set_id}: {e}")
        return None
    
if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT setID, urlPriceHistory FROM lego_prices")
    rows = cursor.fetchall()


    for row in rows:
                set_id, url = row
                
                cursor.execute("SELECT urlPicture FROM lego_pictures WHERE setID = ?", (set_id,))
                picture = cursor.fetchone()[0]
                if picture is None:
                    picture = get_picture(url)
                    # break
                    if picture is not None:
                            # print(picture)
                            cursor.execute("UPDATE lego_pictures SET urlPicture = ? WHERE setID = ?", (picture, set_id))

                    else:
                            print("Nepodarilo sa nahrat obrazok pre setID:", set_id)

    connection.commit()
    connection.close()

