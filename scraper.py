import json

def test_bot():
    # We maken handmatig een lijstje om te kijken of je app het ontvangt
    test_data = [
        {"naam": "TEST MSC AMSTERDAM", "tijd": "14:30", "kade": "1742"},
        {"naam": "TEST MAERSK ANTWERP", "tijd": "18:00", "kade": "1712"}
    ]
    
    with open('mpet_planning.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    print("Test-boten zijn verstuurd naar de app!")

if __name__ == "__main__":
    test_bot()
