import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_mpet():
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    try:
        print("Bot zoekt naar echte boten...")
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        mpet_boten = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 6:
                tijd = cells[0].get_text(strip=True)
                naam = cells[1].get_text(strip=True)
                kade = cells[5].get_text(strip=True)
                
                if "17" in kade:
                    mpet_boten.append({"naam": naam, "tijd": tijd, "kade": kade})

        # Altijd één bericht erin zetten zodat we weten dat hij werkt
        if not mpet_boten:
            mpet_boten.append({
                "naam": "Systeem: Verbonden (Geen MPET boten)", 
                "tijd": datetime.now().strftime('%H:%M'), 
                "kade": "17XX"
            })

        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(mpet_boten, f, ensure_ascii=False, indent=4)
        print("Bestand lokaal aangemaakt.")

    except Exception as e:
        print(f"Fout: {e}")

if __name__ == "__main__":
    scrape_mpet()
