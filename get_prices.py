import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import random

def get_price(url):
    # print(url)
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
        cena_all = soup.find(string=re.compile(r'Cena katalogowa:'))
        if cena_all is not None:
            cena = cena_all.text.strip()
            cena = re.findall(r'\d+,\d+', cena)  #berie iba cisla a ,
            cena_pln = cena[0].replace(',', '.')
            return round(float(cena_pln) * 0.23332, 2)
        
        else:
            cena_all = soup.find(string=re.compile(r'Aktualnie najniższa cena:'))
            if cena_all is not None:
                cena = cena_all.text.strip()
                cena_element = cena_all.find_next_sibling('a')
                cena = cena_element.text.strip()
                cena = re.findall(r'\d+,\d+', cena)
                cena_pln = cena[0].replace(',', '.')
                return round(float(cena_pln) * 0.23332, 2)
            
            else:
                cena_all = soup.find(string=re.compile(r'Ostatnia cena:'))
                if cena_all is not None:
                    cena = cena_all.text.strip()
                    cena = re.findall(r'\d+,\d+', cena)
                    cena_pln = cena[0].replace(',', '.')
                    print('ostatnia', url)
                    print(cena_pln)
                    print(float(cena_pln) * 0.23332)
                    return round(float(cena_pln) * 0.23332, 2)

    except Exception as e:
        print(f"Chyba pri získavaní ceny zo stránky pre setID {set_id}: {e}")
        return None
    
if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # cursor.execute("UPDATE lego_prices SET actualprice = NULL")
    cursor.execute("SELECT setID, urlPriceHistory FROM lego_prices")
    rows = cursor.fetchall()

    dont = 0
    for row in rows:
            set_id, url = row
            
            cursor.execute("SELECT actualprice, DE_retailPrice, UK_retailPrice, US_retailPrice, CA_retailPrice FROM lego_prices WHERE setID = ?", (set_id,))
            current_price, de_retail_price, uk_retail_price, us_retail_price, ca_retail_price = cursor.fetchone()
            
            #aktualizuj iba ak ju este nemam naplnenu
            if current_price is None or current_price == 0:
                price = get_price(url)
                if price is not None:
                        cursor.execute("UPDATE lego_prices SET actualprice = ? WHERE setID = ?", (price, set_id))
                else:
                        print("Nepodarilo sa získať žiadnu cenu pre setID:", set_id)
                        dont+=1
    print(dont)
    connection.commit()
    connection.close()

