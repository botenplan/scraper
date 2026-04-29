import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    urls = [
        "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=a",
        "https://lisscheldemonden.eu/VerwachteReizen.aspx?soort=v"
    ]
    
    gefilterde_boten = []
    zoektermen = ["MPET", "1700", "1742", "ATG", "K17", "QUAY", "KADE", "MSC"]

    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table', {'id': 'gvReizen'})
            
            if table:
                rows = table.find_all('tr')[1:] # Sla de header over
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        tijd = cols[0].get_text(strip=True)
                        naam = cols[1].get_text(strip=True)
                        bestemming = cols[5].get_text(strip=True).upper()
                        
                        if any(term in bestemming for term in zoektermen) or "MSC" in naam.upper():
                            if not any(b['naam'] == naam for b in gefilterde_boten):
                                gefilterde_boten.append({
                                    "naam": naam,
                                    "tijd": tijd,
                                    "kade": bestemming
                                })
        except Exception as e:
            print(f"Fout bij {url}: {e}")

    with open('mpet_planning.json', 'w', encoding='utf-8') as f:
        json.dump(gefilterde_boten, f, ensure_ascii=False, indent=4)
    
    print(f"Klaar! {len(gefilterde_boten)} boten gevonden.")

if __name__ == "__main__":
    scrape_mpet()
