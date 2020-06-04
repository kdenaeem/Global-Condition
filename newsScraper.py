from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request
import requests

news_dict = {}

html = requests.get("https://www.bbc.co.uk")
newsObj = BeautifulSoup(html.text, 'html.parser')#creates an object from the Beautiful


def getStart(startingPage):
    html = urlopen('https://www.bbc.co.uk/news/uk'+startingPage)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a", href=re.compile("^(/news/uk.*)")):
        if 'href' in link.attrs:
            print('http://www.bbc.co.uk'+link.attrs['href'])

def log_error(error):
    with open('crash_log.txt', 'a') as f:
        f.write("{}\n".format(error))
        print(error)

def status_check(status):
    html = status.headers['Content-Type'].lower()
    return status.status_code == 200 and html is not None


def fetch_url(url):
    try:
        status = get(url, stream=True)
        if status_check(status):
            return status.content
        else:
            log_error("Web page not found")
            return None
    except RequestException as error:
        log_error('Page : {}\nError : {}'.format(url, str(error)))
        return None
    
    
def scrape_link():
    html = urlopen('https://www.bbc.co.uk/news')
    bsObj = BeautifulSoup(html)
    
    for link in bsObj.findAll("a"):
        if 'href' in link.attrs:
            print(link.attrs['href'])

def getTitle(pageUrl):
    global pages
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html)
    print(pageUrl)
    try:
        return bsObj.h1.get_text()
    except AttributeError:
        print("dodgy link")

pages = []
title_list = []

def add_to_main_dict(country, headline, link):
    news_dict[country] = news_dict.get(country, {})
    if len(news_dict[country]) <= 5:
        news_dict[country].update({headline : link})
        print(news_dict)

def getBBCWorldTab():
    world_page = []
    html = urlopen("https://www.bbc.co.uk/news/world")
    bsObj = BeautifulSoup(html, features="html5lib")
    for link in bsObj.findAll("a", {"class": "nw-o-link"}):
        if 'href' in link.attrs:
                if re.match("\/news\/world\/(?:.*)", link.attrs['href']):
                    if link.attrs['href'] not in world_page:
                        newPage = link.attrs['href']
                        world_page.append('http://www.bbc.co.uk' + newPage)
    return list(set(world_page))

def read_country(filename):
    item_list = []
    with open(filename, "r") as f:
        for line in f:
            item_list.append(line.strip())
    return item_list

def find_country(url_string):
    try:
        html = urlopen(url_string)
    except urllib.error.HTTPError:
        print("HTTP error")
        
    bsObj = BeautifulSoup(html)
    country_list = read_country("country_list.txt")
    highest_key_count = 2
    key_country = ""
    for country in country_list: # iterates through the country list from read_country
        found_list = bsObj.find_all(text=re.compile(country))
        if len(found_list) > highest_key_count:
            highest_key_count = len(found_list) # checks each loop whether or not a higher count has been found
            key_country = country # by comparing current count with the old one
        key_count = len(found_list)
    return key_country

existing = set()
def getLinkBBC(startingPage):
    global pages, existing
    html = urlopen('https://www.bbc.co.uk/news/world')
    bsObj = BeautifulSoup(html, features="html5lib")
    if startingPage == "uk":
        for link in bsObj.findAll("a", href=re.compile("^(/news/uk.*)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in existing:
                    newPage = link.attrs['href']
                    existing.add(newPage)
                    title = getTitle('http://www.bbc.co.uk' + newPage)
                    title_list.append(title)
                    pages.append(['http://www.bbc.co.uk' + newPage, title])
        print(pages)
    
    elif startingPage == "world":
        continent_page = getBBCWorldTab()
        for continent in continent_page:
            html = urlopen(continent)
            bsObj = BeautifulSoup(html, features="html5lib")
            for link in bsObj.findAll("a", href=re.compile("\/news\/world-(?:.*)")):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in existing:
                        newPage = link.attrs['href']
                        existing.add(newPage)
                        page = ("http://www.bbc.co.uk" + link.attrs['href'])
                        key_country = find_country(page)
                        title = getTitle(page)
                        add_to_main_dict(key_country, title, page)


getLinkBBC("world")


#getLinkBBC("")





