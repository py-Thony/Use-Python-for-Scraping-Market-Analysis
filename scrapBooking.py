# -*- coding: utf-8 -*-

"""
script de scraping pour récupérer 1000 livres
sous forme de fichiers CSV individuels par catégories.

Au passage, seront récupérées les images des livres
dans un dossier séparé.
"""

########################################
# Importations des modules nécessaires #
########################################

# Module d'interaction avec le système d'exploitation
import os
# Module de parsage HTML en langage humain
from bs4 import BeautifulSoup as Soup
# Module de gestion du temps pour espacer les requêtes
import time
# Module de gestion du format CSV
import csv

##########################################
# Importation des fonctions personnelles #
##########################################

from scrapBookingFunctions import CreateFolder, scrapLinksOfCategories
from scrapBookingFunctions import scrapLinksOfBooks
from scrapBookingFunctions import scrapBookInformations
from scrapBookingFunctions import scrapAndSaveBookImage

""" Dans un premier temps, il faut se connecter au site ciblé

Un examen du code HTML permet de détecter l'utilisation d'URLs
relative, nous aurons donc besoin d'une URL de base pour les
reconstruire en URLs absolues des catégories et des page des produits
"""

websiteUrl = 'http://books.toscrape.com/index.html'

# To rebuild the relative links of categories
baseUrlCategories = 'http://books.toscrape.com/'
# To rebuild the relative links of books
baseUrlBooks = 'http://books.toscrape.com/catalogue/'

# Une fonction est crée pour récupérer les liens des catégories
linksOfCategories = scrapLinksOfCategories(websiteUrl, baseUrlCategories)

""" Maintenant que nous avons notre liste de liens de catégories
nous pouvons itérer chacun pour récupérer les liens des livres.

La collecte de données se fera plus tard, il ne s'agit ici que de récupérer
les liens et de les lister selon leur catégorie respective

Nous utiliserons donc une simple boucle for
"""

allBooksLinksList = []

for oneCategory in linksOfCategories:
    # Defining names and links separately
    categoryName = oneCategory[0]
    print(categoryName)
    categoryLink = oneCategory[1]
    # Retrieving all book links for the current category
    allBooksLinksList.append(
        (categoryName, scrapLinksOfBooks(categoryLink, baseUrlBooks)))

""" A ce stade nous disposons d'une liste générale
contenant une sous-liste par catégorie.

Chaque sous-liste se présente sous forme d'un tuple,
(nomCat, (listeliensLivres))
"""

# Il s'agit maitenant d'éplucher notre liste, et de passer une
# requête par lien de livre, et d'enregistrer le résultat avant de passer
# à la catégorie suivante
RootDir = os.path.dirname(os.path.abspath(__file__))
fields=[
    'Book Title','UPC Code','Product Type', 'Price (ExclTax)', 
    'Price (InclTax)', 'Taxes', 'Availability', 'Image Url']
countBooks = 0
for linksOfBookInOneCategory in allBooksLinksList:

    categoryName = linksOfBookInOneCategory[0]

    CSVpath = f"{RootDir}\\SCRAPED_FILES\\{categoryName}\\CSV_FILES\\"
    imagePath = f"{RootDir}\\SCRAPED_FILES\\{categoryName}\\IMAGES\\"
    CreateFolder(CSVpath)
    CreateFolder(imagePath)

    listOfInfoForOneBook = []
    listOfallBooksInfo = []
    for bookLink in linksOfBookInOneCategory[1]:
        countBooks += 1
        print(countBooks)
        # Retrieving information from the book
        imageUrl, currentBookInfo = scrapBookInformations(bookLink)
        listOfallBooksInfo.append(list(currentBookInfo))

        #time.sleep(0.5)

        currentBookImage = scrapAndSaveBookImage(
            imagePath, imageUrl, currentBookInfo[0])
    with open(
        f"{CSVpath}{categoryName}.csv",
        'w',
        encoding="utf-8",
        newline=''
        ) as csvfile:

        spamwriter = csv.writer(
            csvfile,
            delimiter=',',
            quotechar=' ',
            quoting=csv.QUOTE_MINIMAL
            )
    
        spamwriter.writerow(fields)
        spamwriter.writerows(listOfallBooksInfo)
        print("-------------------------")
        print("ENREGISTRMENT CSV TERMINE")
        print("-------------------------")