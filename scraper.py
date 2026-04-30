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
        print(f"--- Bot start scan: {datetime.now().strftime('%H:%M:%S')} ---")
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zoek de tabel en alle rijen
        rows = soup.find_all('tr')
        mpet_boten = []

        for row in rows:
            cells = row.find_all('td')
            # De website heeft meestal 10 kolommen. 
            # Kolom 0 = Tijd, Kolom 1 = Schip, Kolom 5 = Kade/Bestemming
            if len(cells) >= 6:
                tijd_ruw = cells[0].get_text(strip=True)
                schip_naam = cells[1].get_text(strip=True)
                bestemming_kade = cells[5].get_text(strip=True)
                
                # We filteren op kades die met 17 beginnen (MPET)
                if "17" in bestemming_kade:
                    print(f"Gevonden: {schip_naam} naar {bestemming_kade}")
                    mpet_boten.append({
                        "naam": schip_naam,
                        "tijd": tijd_ruw,
                        "kade": bestemming_kade,
                        "status": "Live"
                    })

        # Als er echt niets voor MPET is, laat dan een status zien
        if not mpet_boten:
            print("Geen schepen voor kade 1700-1742 gevonden.")
            mpet_boten.append({
                "naam": "Systeem Online: Geen MPET schepen",
                "tijd": datetime.now().strftime('%H:%M'),
                "kade": "Check Loodswezen"
            })

        # Opslaan in JSON
        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(mpet_boten, f, ensure_ascii=False, indent=4)
        
        print(f"Succes: {len(mpet_boten)} regels opgeslagen.")

    except Exception as e:
        print(f"Fout tijdens scrapen: {e}")

if __name__ == "__main__":
    scrape_mpet()
