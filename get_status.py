import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import random

def get_status(url):
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
        
        # Extract ceny z a odstráň všetko okrem ceny
        cena_all = soup.find(string=re.compile(r'Aktualnie najniższa cena:'))
        if cena_all is not None:
            return "Available"
        
        else:
            # Produkt už nie je v ponuke
            cena_all = soup.find(string=re.compile(r'Ostatnia cena:'))
            if cena_all is not None:
                return "Discontinued"
            
            else:
                #produkt neni v ponuke a ani o tom neni zaznam 
                return "Not found"

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
            
            cursor.execute("SELECT status FROM lego_main WHERE setID = ?", (set_id,))
            status = cursor.fetchone()[0]

            #aktualizuj status
            if status != 'A gift upon purchase':
                status_new = get_status(url)
                if status_new is not None:
                    cursor.execute("UPDATE lego_main SET status = ? WHERE setID = ?", (status_new, set_id))
                else:
                    print("Nepodarilo sa aktualizovat status pre setID:", set_id, 'nechavam status', status)
    connection.commit()
    connection.close()

