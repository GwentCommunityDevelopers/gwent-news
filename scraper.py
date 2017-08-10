#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import re

URL = "https://www.playgwent.com/{0}/news"
LOCALES = ["en","pl", "de"]

def getHtml(locale):
    url = URL.format(locale)
    result = requests.get(url)

    if result.status_code == 200:
        return result.text
    else:
        print("Fetching", url, "failed.")
        return
        
for locale in LOCALES:
    soup = BeautifulSoup(getHtml(locale), 'html.parser')
    
    if soup == None:
        continue

    links = soup.find_all('a', href=True)
    for link in links:
        linkUrl = link['href']
        pattern = re.compile(".*?\/" + locale + "\/news\/\d.*?")
        if pattern.match(linkUrl):
            print(linkUrl)           