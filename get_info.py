import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import random

def get_info(url, info_type):
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
        # Upravenie URL 
        pattern = r'-h(\d+)$'
        url = re.sub(pattern, r'-p\1', url)

        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Nájsť správne pole na základe typu informácií
        if info_type == 'minifigs':
            class_string = 'Liczba minifigurek'
        elif info_type == 'pieces':
            class_string = 'Liczba elementów'
        elif info_type == 'minAge':
            class_string = 'Grupa wiekowa'
        else:
            raise ValueError("Neplatný typ informácií")
        
        class1 = soup.find(string=re.compile(class_string))
        if class1 is not None:
            class2 = class1.find_next('dd')
            if class2 is not None:
                if info_type == 'minAge':
                    age = class2.text.strip().rstrip('+')
                    return int(round(float(age)))
                else:
                    return int(class2.text)
            else:
                print(f"Nepodarilo sa nájsť informáciu pre {info_type}.")
        else:
            print(f"Nepodarilo sa nájsť informáciu pre {info_type}.")

    except Exception as e:
        print(f"Chyba pri získavaní informácie zo stránky: {e}")
        return None
    
if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT setID, urlPriceHistory FROM lego_prices")
    rows = cursor.fetchall()

    for row in rows:
        set_id, url = row
        
        cursor.execute("SELECT minifig, minAge, pieces FROM lego_main WHERE setID = ?", (set_id,))
        minifigs, min_age, pieces = cursor.fetchone()

        # # Aktualizácia minifigúrok
        if minifigs is None:
            new = get_info(url, 'minifigs')
            if new is not None:
                cursor.execute("UPDATE lego_main SET minifigs = ? WHERE setID = ?", (new, set_id))
            else:
                cursor.execute("UPDATE lego_main SET minifigs = ? WHERE setID = ?", (0, set_id))
        
        
        # # Aktualizácia počtu dielikov
        if pieces is None:
            new = get_info(url, 'pieces')
            if new is not None:
                cursor.execute("UPDATE lego_main SET pieces = ? WHERE setID = ?", (new, set_id))
            else:
                print("Nepodarilo sa aktualizovať počet dielikov pre setID:", set_id)
        
        
        # Aktualizácia veku
        if min_age is None:
            new = get_info(url, 'minAge')
            if new is not None:
                if new <50:
                    cursor.execute("UPDATE lego_main SET minAge = ? WHERE setID = ?", (new, set_id))
                else:
                    print("Nepodarilo sa aktualizovať minAge pre setID:", set_id)
            else:
                print("Nepodarilo sa aktualizovať minAge pre setID:", set_id)

    connection.commit()
    connection.close()
