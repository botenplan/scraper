import requests
from bs4 import BeautifulSoup

# Instellingen
URL = "DE_LINK_NAAR_DE_PLANNING_WEBSITE"
TOPIC = "mijn_mpet_boten_123" # Zelfde naam als in de app

def check_planning():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Zoek alle rijen in de tabel
    rows = soup.find_all('tr')
    found_ships = []

    for row in rows:
        text = row.get_text()
        if "MPET West" in text or "MPET Oost" in text:
            # Pak de relevante info (naam, tijd, etc.)
            found_ships.append(text.strip())

    if found_ships:
        bericht = "\n".join(found_ships)
        # Stuur naar je app via ntfy
        requests.post(f"https://ntfy.sh/{TOPIC}", 
                      data=bericht.encode('utf-8'),
                      headers={"Title": "Nieuwe MPET Planning"})

check_planning()
