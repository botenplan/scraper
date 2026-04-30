import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_mpet():
    # De echte website van het Loodswezen
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx"
    
    # We doen alsof we een normale browser zijn
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"--- Bot start op: {datetime.now().strftime('%d-%m %H:%M:%S')} ---")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("Verbinding met Loodswezen gelukt!")
        else:
            print(f"Fout: Website geeft code {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        mpet_boten = []
        print(f"Totaal aantal rijen gevonden op site: {len(rows)}")

        for row in rows:
            cells = row.find_all('td')
            # Een rij moet minstens 6 kolommen hebben voor tijd, naam, kade etc.
            if len(cells) >= 6:
                tijd = cells[0].get_text(strip=True)
                naam = cells[1].get_text(strip=True)
                kade = cells[5].get_text(strip=True)
                
                # We zoeken specifiek naar de kades van MPET (beginnend met 17)
                if "17" in kade:
                    print(f"Gevonden: {naam} naar kade {kade}")
                    mpet_boten.append({
                        "naam": naam,
                        "tijd": tijd,
                        "kade": kade,
                        "laatst_gezien": datetime.now().strftime('%H:%M')
                    })

        # Als er geen boten zijn, maken we een 'systeem-status' aan
        if not mpet_boten:
            print("Geen MPET boten gevonden op dit moment.")
            mpet_boten.append({
                "naam": "Bot is Online (Wachten op schepen)",
                "tijd": datetime.now().strftime('%H:%M'),
                "kade": "17XX"
            })

        # Opslaan in het JSON bestand
        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(mpet_boten, f, ensure_ascii=False, indent=4)
        
        print(f"--- Bot succesvol afgerond: {len(mpet_boten)} items in JSON ---")

    except Exception as e:
        print(f"ER IS IETS MISGEGAAN: {e}")

if __name__ == "__main__":
    scrape_mpet()
