# -*- coding: utf-8 -*-

"""
Ce script se charge d'interroger le site www.books.toscrape.com

CONCEPTION:
Etape 1: Extraction des URLS de chaque catégorie et mise en liste.

Etape 2: Epluchage de cette liste pour scraper tous les liens de livre
        et mise en liste générale de tuples (nom catégorie, [liste liens])

Etape 3: Interrogation de chaque lien de livre pour:
                    - Extraction des informations textuelles
                    - Téléchargement de l'image du livre
Etape 3bis: Création de dossiers parents auto-nommés selon le nom de la catégorie,
            Création de dossiers enfants 'CSV' et 'IMAGES'
            Enregistrement des données textuelles dans un fichier CSV dans le dossier CSV
            Enregistrement des images renommées avec le titre du livre dans le dossier IMAGES

Rencontrant des problèmes de contrôle de l'endroit où créer les dossiers,
(sous machine Windows10, VScode) il à été nécessaire de créer une fonction
'CreateFolder' et de définir le Path manuellement.

Rencontrant des cas particuliers dans les titres de livres, il à été necessaire
de gérer ces exceptions en remplaçant certains symboles. (eg: virgules <!> CSV)

ARBORESCENCE:
scrapBooking.py >>> fonctionnement général du programme et paramétrages
scrapBookingFuncions.py >>> routines répétitives passées sous forme de fonctions à appeler

GENERATION DE DOSSIERS ET FICHIERS:
dossier parent portant le nom de la catégorie
    --> Dossier enfant nommé CSV
        --> finchier.csv portant le nom de la catégorie
    --> Dossier enfant nommé IMAGES
        --> enregistrement des images au format JPG et renommées avec le titre du livre

"""

########################################
# Importations des modules nécessaires #
########################################
import os
import csv

##########################################
# Importation des fonctions personnelles #
##########################################

from scrapBookingFunctions import create_folder
from scrapBookingFunctions import scrap_links_of_categories
from scrapBookingFunctions import scrap_links_of_books
from scrapBookingFunctions import scrap_book_informations

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

# Auto remplissage de la liste des liens de catégories
linksOfCategories = scrap_links_of_categories(
                                websiteUrl,
                                baseUrlCategories)

allBooksLinksList = []
for oneCategory in linksOfCategories:
    # Gestion du cas particuliers des catégories à plusieurs pages
    provisionalLinksList = []

    nextPage = 1
    booksScraped = 0
    categoryName = oneCategory[0].capitalize()
    categoryLink = oneCategory[1]
    expectedBooks = oneCategory[2]
    nbPagesToScan = oneCategory[3]

    print(categoryName, "\n", categoryLink)
    while nextPage <= nbPagesToScan:
        
        nbBooksToScan = expectedBooks - booksScraped

        if nextPage == 2:
            print(f"Page N°{nextPage}")
            categoryLink = categoryLink.replace(
                "index.html",
                f"page-{nextPage}.html")

        elif nextPage > 2:
            print(f"Page N°{nextPage}")
            categoryLink = categoryLink.replace(
                f"page-{nextPage-1}.html",
                f"page-{nextPage}.html")

        scanPageInCourse = scrap_links_of_books(
                                categoryLink,
                                baseUrlBooks,
                                nbBooksToScan)

        for element in scanPageInCourse:
            provisionalLinksList.append(element)

        booksScraped += len(scanPageInCourse)
        nextPage += 1
    print(">>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<")
    # Retrieving all book links for the current category
    allBooksLinksList.append((categoryName, provisionalLinksList))


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
    'Book Title','UPC Code','Product Type', 
    'Price (ExclTax)', 'Price (InclTax)', 'Taxes', 
    'Availability', 'number_of_reviews', 'nb_of_stars',
    'Image Url']
countBooks = 0
for linksOfBookInOneCategory in allBooksLinksList:

    categoryName = linksOfBookInOneCategory[0]

    CSVpath = f"{RootDir}\\SCRAPED_FILES\\{categoryName}\\CSV_FILES\\"
    imagePath = f"{RootDir}\\SCRAPED_FILES\\{categoryName}\\IMAGES\\"
    create_folder(CSVpath)
    create_folder(imagePath)

    listOfallBooksInfo = []
    for bookLink in linksOfBookInOneCategory[1]:
        countBooks += 1
        print(countBooks)
        # Retrieving information from the book
        currentBookInfo = scrap_book_informations(bookLink, imagePath)
        listOfallBooksInfo.append(list(currentBookInfo))

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