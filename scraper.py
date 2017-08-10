#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import re
import unicodedata
import json
from pprint import pprint
import datetime

BASE_URL = "https://www.playgwent.com{0}"
URL = BASE_URL.format("/{0}/news")
LOCALES = ["en", "pl", "de", "es", "fr", "it", "ja", "pt-BR", "ru"]

def saveJson(filepath, data):
    print("Saving news to: %s" % (filepath))
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, sort_keys=True, indent=2, separators=(',', ': '))

def getHtml(locale):
    url = URL.format(locale)
    result = requests.get(url)

    if result.status_code == 200:
        return result.text
    else:
        print("Fetching", url, "failed.")
        return
        
def getNews(newsId, url):
    result = requests.get(url)
    if result.status_code != 200:
        raise(Exception("Fetching " + url + " failed."))
    newsSoup = BeautifulSoup(result.text, 'html.parser')
    newsItem = {}
    newsItem['id'] = newsId

    for image in newsSoup.find_all(itemprop = 'image'):
        pattern = re.compile(".*?playgwent\.com\/news\/.*?")
        if pattern.match(image['src']):
            newsItem['image'] = image['src']
    newsItem['title'] = newsSoup.find(itemprop = 'headline').text
    body = newsSoup.find(itemprop = 'articleBody').text
    newsItem['body'] = unicodedata.normalize("NFKD", body)
    newsItem['url'] = url
    newsItem['timestamp'] = newsSoup.find('time')['datetime']

    return newsItem

news = {}

for locale in LOCALES:
    soup = BeautifulSoup(getHtml(locale), 'html.parser')
    
    if soup == None:
        continue

    news[locale] = {}
    links = soup.find_all('a', href=True)
    for link in links:
        linkUrl = link['href']
        pattern = re.compile(".*?\/" + locale + "\/news\/\d.*?")
        if pattern.match(linkUrl):
            newsId = re.search('news\/(\d+)\/', linkUrl).group(1)
            news[locale][newsId] = getNews(newsId, BASE_URL.format(linkUrl))

saveJson('news.json', news)