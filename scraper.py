import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_mpet():
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"Start scan om {datetime.now().strftime('%H:%M:%S')}")
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We zoeken alle rijen in de tabel
        rows = soup.find_all('tr')
        mpet_boten = []

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 6:
                tijd = cells[0].get_text(strip=True)
                naam = cells[1].get_text(strip=True)
                kade = cells[5].get_text(strip=True)
                
                # We checken of '17' voorkomt in de kade kolom
                # Of we zoeken in de hele rij voor het geval de kolommen verspringen
                row_text = row.get_text()
                
                if any(num in kade for num in ["1700", "1710", "1718", "1720", "1730", "1740", "1742"]) or "17" in kade:
                    mpet_boten.append({
                        "naam": naam,
                        "tijd": tijd,
                        "kade": kade,
                        "update": datetime.now().strftime('%H:%M')
                    })

        # Als we écht niets vinden, sturen we een 'System Log' mee zodat de app niet leeg blijft
        if not mpet_boten:
            mpet_boten.append({
                "naam": "Systeem Check: Online",
                "tijd": datetime.now().strftime('%H:%M'),
                "kade": "Geen MPET boten op site"
            })

        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(mpet_boten, f, ensure_ascii=False, indent=4)
        
        print(f"Klaar! {len(mpet_boten)} items opgeslagen.")

    except Exception as e:
        print(f"Fout: {e}")
        # Bij fout ook een melding naar de app sturen
        with open('mpet_planning.json', 'w') as f:
            json.dump([{"naam": "Bot Fout", "tijd": "Nu", "kade": str(e)[:20]}], f)

if __name__ == "__main__":
    scrape_mpet()
