# coding: utf_8

"""
Web Scraping pour créer un fichier CSV

Nous avons besoin de deux packages pour cette tâche, 
                BeautifulSoup et urllib. 

Nous pouvons facilement installer ces deux packages 
en utilisant la commande pip
            pip install bs4 et pip install urllib. 
"""

# Après avoir installé ces packages avec succès, 
# la prochaine chose à faire est d'importer les packages           
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 


myUrl="http://books.toscrape.com/catalogue/" + \
      "a-light-in-the-attic_1000/index.html"

uClient = uReq(myUrl) 
pageHtml = uClient.read()

uClient.close() 
pageSoup = soup(pageHtml, "html.parser")

productInformation = pageSoup.find("div", {"class" : "col-sm-6 product_main"})
print(productInformation)