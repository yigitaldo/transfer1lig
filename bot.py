import os
import json
import requests
from bs4 import BeautifulSoup
import tweepy

print("Bot başlatıldı...")

URL = "https://www.tff.org/default.aspx?pageID=574"
DATA_FILE = "data.json"

# X API bağlantısı
client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_SECRET"]
)

# eski veriyi yükle
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

    items = []

    # TFF sayfasındaki tüm metinleri çekiyoruz (basit versiyon)
    for tag in soup.find_all(["a", "p", "td"]):
        text = tag.get_text().strip()
        if len(text) > 15:
            items.append(text)

    return list(set(items))

def tweet(text):
    try:
        client.create_tweet(text=text)
        print("Tweet atıldı:", text)
    except Exception as e:
        print("Tweet hatası:", e)

def check_changes(items):
    new_items = []

    for item in items:
        if item not in seen:
            seen[item] = True
            new_items.append(item)

    return new_items

def main():
    items = fetch_data()
    new_items = check_changes(items)

    if not new_items:
        print("Yeni değişiklik yok.")
        save_data()
        return

    for item in new_items[:3]:
        tweet(f"📄 TFF Güncelleme:\n{item}\n#1Lig #TFF")

    save_data()

main()
print("API KEY var mı:", "X_API_KEY" in os.environ)
print("API SECRET var mı:", "X_API_SECRET" in os.environ)
print("ACCESS TOKEN var mı:", "X_ACCESS_TOKEN" in os.environ)
print("ACCESS SECRET var mı:", "X_ACCESS_SECRET" in os.environ)
