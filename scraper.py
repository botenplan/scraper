import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    # We checken zowel Aankomst (soort=a) als Vertrek (soort=v)
    urls = [
        "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=a",
        "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=v"
    ]
    
    gefilterde_boten = []
    zoektermen = ["MPET", "1700", "1742", "ATG", "K17", "QUAY 17"]

    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'gvReizen'})
            
            if table:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) > 5:
                        naam = cols[1].text.strip()
                        bestemming = cols[5].text.strip().upper()
                        tijd = cols[0].text.strip()
                        
                        # Check of een van onze zoektermen in de bestemming staat
                        if any(term in bestemming for term in zoektermen):
                            # Voorkom dubbele boten als ze in beide lijsten staan
                            if not any(b['naam'] == naam for b in gefilterde_boten):
                                gefilterde_boten.append({
                                    "naam": naam,
                                    "tijd": tijd,
                                    "kade": bestemming
                                })
        except Exception as e:
            print(f"Fout bij {url}: {e}")

    # Opslaan
    with open('mpet_planning.json', 'w', encoding='utf-8') as f:
        json.dump(gefilterde_boten, f, ensure_ascii=False, indent=4)
    
    print(f"Klaar! {len(gefilterde_boten)} boten gevonden.")

if __name__ == "__main__":
    scrape_mpet()
