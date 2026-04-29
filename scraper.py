import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    # We gebruiken jouw link voor aankomende reizen (soort=a)
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=a"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'gvReizen'})
        
        boten = []
        if table:
            rows = table.find_all('tr')[1:] # Sla de header over
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 5:
                    naam = cols[1].text.strip()
                    bestemming = cols[5].text.strip().upper()
                    tijd = cols[0].text.strip()
                    
                    # We zoeken nu op meerdere termen die met MPET te maken hebben
                    zoektermen = ["MPET", "1700", "1742", "ATG", "K17"]
                    if any(term in bestemming for term in zoektermen):
                        boten.append({
                            "naam": naam,
                            "tijd": tijd,
                            "kade": bestemming
                        })
        
        # Schrijf naar het JSON bestand
        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(boten, f, ensure_ascii=False, indent=4)
        
        print(f"Succes: {len(boten)} boten gevonden voor MPET.")
        
    except Exception as e:
        print(f"Fout tijdens scrapen: {e}")

if __name__ == "__main__":
    scrape_mpet()
