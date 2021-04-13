# -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup

requete = requests.get("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
page = requete.content
soup = BeautifulSoup(page)