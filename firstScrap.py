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
import requests


# Toutes les futures opérations auront besoin
# d'une URL à connecter pour l'interroger.
myUrl="http://books.toscrape.com/catalogue/" + \
      "a-light-in-the-attic_1000/index.html"

# Définition de l'outil de récolte d'URL
response = requests.get(myUrl)


# Une fois tous les ingrédients en place,
# préparation de la soupe HTML
pageSoup = soup(response, "lxml")

"""
h1 donne le nom en clair
h2 donne 
"""