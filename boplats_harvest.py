#!/usr/bin/python

from bs4 import BeautifulSoup
import sys
import re
from time import gmtime, strftime
import time
import requests

from credentials import *

### Create credentials.py file, see example below:
##!/usr/bin/python
#
#BOPLATS_USERNAME = 'your username here'
#BOPLATS_PASSWORD = 'your password here'
#
#

sess = requests.session()
sess.post("https://www.boplatssyd.se/login", data={"login[username]": BOPLATS_USERNAME, "login[password]": BOPLATS_PASSWORD, "form_id": "bologin_form"})

minsida = BeautifulSoup(sess.get("https://www.boplatssyd.se/minsida/").text, "lxml")
links = list()
for descriptor in minsida.find_all('div', attrs={'class':'object-details'}):
    links.append(descriptor.find('span', attrs={'class':'address'}).find('a').get('href'))

for link in links:
    time.sleep(2)
    onepage = BeautifulSoup(sess.get("https://www.boplatssyd.se" + link).text, "lxml")
    topsection = onepage.body.find('div', attrs={'class':'top-section'})
    interest = onepage.body.find('div', attrs={'class':'interest-info block-style'})
    facts = onepage.body.find('div', attrs={'class':'facts block-style'})
    row = list()
    # Id
    row.append(onepage.head.find('link', attrs={'rel':'shortlink'}).get('href'))
    # Harvest date
    row.append(strftime("%Y-%m-%d", gmtime()))
    # District
    row.append(topsection.find('div', attrs={'class':'object-adress'}).find('h3', attrs={'class':'subaddress'}).text)
    # Address
    row.append(topsection.find('div', attrs={'class':'object-adress'}).find('h1').text)
    # Rent
    row.append(facts.find('div', attrs={'class':'fact rent'}).find('div', attrs={'class':'fact-content'}).text)
    row[-1] = re.sub('[^0-9]', '', row[-1])
    # Area
    row.append(facts.find('div', attrs={'class':'fact square'}).find('div', attrs={'class':'fact-content'}).text)
    row[-1] = re.sub('[^0-9]', '', row[-1])
    # Rooms
    row.append(facts.find('div', attrs={'class':'fact size'}).find('div', attrs={'class':'fact-content'}).text)
    # Move in
    row.append(interest.find('div', attrs={'class':'user-queue'}).find('span', attrs={'class':'number'}).text)
    # Application deadline
    row.append(interest.find('div', attrs={'class':'user-queue last'}).find('span', attrs={'class':'number'}).text)
    # Queue rank
    row.append(topsection.find('div', attrs={'class':'interest-container'}).find('span', attrs={'class':'number'}).text)
    row[-1] = re.sub('[^0-9/]', '', row[-1])
    # Queue length
    row.append(topsection.find('div', attrs={'class':'number-interested interest-item'}).find('span', attrs={'class':'number'}).text)
    row[-1] = re.sub('[^0-9/]', '', row[-1])

    for ndx, r in enumerate(row):
        row[ndx] = row[ndx].strip().replace(',','')
    print ','.join(row).encode('utf-8')
