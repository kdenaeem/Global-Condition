from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getTitle(pageUrl):
    global pages
    html = urlopen('https://www.bbc.co.uk'+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
    except AttributeError:
        print("This page is missing")
    for link in bsObj.find_all('a', href=re.compile('/news/')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getTitle(newPage)

getTitle("")