import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=a"
    gefilterde_boten = []
    zoektermen = ["1700", "1742", "MPET", "ATG", "MSC"]

    # We maken een 'Session' aan om cookies te bewaren, net als een echte browser
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://lisscheldemonden.eu/',
        'Connection': 'keep-alive'
    }

    try:
        # Stap 1: Bezoek de hoofdpagina om cookies te krijgen
        session.get("https://lisscheldemonden.eu/", headers=headers, timeout=15)
        
        # Stap 2: Vraag de echte data op
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # We zoeken naar de tabel met ID gvReizen
            table = soup.find('table', id='gvReizen')
            
            if not table:
                # Als de ID niet werkt, zoeken we elke tabel met data
                table = soup.find('table', class_='gridview') or soup.find('table')

            if table:
                rows = table.find_all('tr')
                for row in rows[1:]: # Sla de koptekst over
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        naam = cols[1].get_text(strip=True)
                        kade = cols[5].get_text(strip=True).upper()
                        tijd = cols[0].get_text(strip=True)
                        
                        # Check of het voor ons interessant is
                        if any(term in kade for term in zoektermen) or any(term in naam.upper() for term in zoektermen):
                            gefilterde_boten.append({
                                "naam": naam,
                                "tijd": tijd,
                                "kade": kade
                            })
        
        # Voeg een 'laatst geüpdatet' tijdstip toe zodat je ziet dat de bot gewerkt heeft
        if not gefilterde_boten:
            print("Geen boten gevonden op de site op dit moment.")

    except Exception as e:
        print(f"Fout tijdens het scrapen: {e}")

    # Opslaan
    with open('mpet_planning.json', 'w', encoding='utf-8') as f:
        json.dump(gefilterde_boten, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_mpet()
