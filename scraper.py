import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    boten = []
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 5:
            locatie = cols[1].text # De kolom met de kaai/terminal
            if "MPET West" in locatie or "MPET Oost" in locatie:
                boot_info = {
                    "naam": cols[3].text.strip(),
                    "tijd": cols[2].text.strip(),
                    "kade": locatie.strip()
                }
                boten.append(boot_info)
    
    # Sla de resultaten op in een JSON bestand
    with open('mpet_planning.json', 'w') as f:
        json.dump(boten, f)

if __name__ == "__main__":
    scrape_mpet()
