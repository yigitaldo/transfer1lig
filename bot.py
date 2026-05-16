import os
import json
import requests
from bs4 import BeautifulSoup

print("Bot çalıştı - TFF kontrol ediliyor...")

URL = "https://www.tff.org/default.aspx?pageID=574"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

print("Sayfa çekildi, bot hazır.")
