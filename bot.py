import requests
import json
import os
from bs4 import BeautifulSoup

print("Bot başlatıldı...")

URL = "https://www.tff.org/default.aspx?pageID=574"

DATA_FILE = "data.json"

# Daha önce paylaşılanları yükle
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        seen = json.load(f)
else:
    seen = {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

def fetch_data():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    # Basit test: sayfadaki linkleri çekiyoruz
    items = []

    for link in soup.find_all("a"):
        text = link.get_text().strip()
        if len(text) > 10:
            items.append(text)

    return items

def check_changes(items):
    new_items = []

    for item in items:
        if item not in seen:
            new_items.append(item)
            seen[item] = True

    return new_items

def tweet(text):
    # ŞU AN SADECE TEST (API bağlayacağız birazdan)
    print("TWEET ATILDI:", text)

def main():
    items = fetch_data()
    new_items = check_changes(items)

    if not new_items:
        print("Yeni veri yok.")
        return

    for item in new_items[:5]:
        tweet(f"📄 TFF Güncelleme: {item}")

    save_data()

main()
