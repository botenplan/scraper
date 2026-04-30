import requests
from bs4 import BeautifulSoup
import json

def scrape_mpet():
    url = "https://lisscheldemonden.eu/VerwachteReizen.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        print("Bot start met zoeken...")
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zoek de tabel
        table = soup.find('table')
        if not table:
            print("Geen tabel gevonden!")
            return

        mpet_boten = []
        rows = table.find_all('tr')

        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 6:
                naam = cols[1].text.strip()
                tijd = cols[0].text.strip()
                kade = cols[5].text.strip()

                # Filter op alle kades die met 17 beginnen (MPET)
                if "17" in kade:
                    mpet_boten.append({"naam": naam, "tijd": tijd, "kade": kade})

        # Schrijf het bestand
        with open('mpet_planning.json', 'w', encoding='utf-8') as f:
            json.dump(mpet_boten, f, ensure_ascii=False, indent=4)
        
        print(f"Succes! {len(mpet_boten)} boten gevonden en klaargezet voor opslag.")

    except Exception as e:
        print(f"Fout tijdens het scrapen: {e}")

if __name__ == "__main__":
    scrape_mpet()
