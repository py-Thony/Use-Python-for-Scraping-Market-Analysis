# -*- coding: utf-8 -*-

"""
ce fichier regroupe les fonctions crées pour gérer
les différentes routines du script principal
"""

########################################
# Importations des modules nécessaires #
########################################

# Gestion de l'interaction avec l'os
import os
# Module de captation d'URLs
import requests
import time
# Module de parsage HTML en langage humain
from bs4 import BeautifulSoup as Soup
from math import ceil


def scrap_links_of_categories(WEBSITE_URL, BASE_URL_CATEGORIES):
    """
    Function used to retrieve the links of the categories 
    and return a list containing these links.

    This function performs the following tasks:
        - Html request on the URL passed as a parameter
        - Parsing of the result obtained
        - Selection of targeted tags
        - Converting relative URLs to absolute
        - Returns the list of tuples containing 
          the name of the category and its link
    """

    response_categories = requests.get(WEBSITE_URL)
    categories_soup = Soup(response_categories.text, "html.parser")
    links_of_categories = [] 
    link_incrementation = 3 # 1st link != 1st position
    PAGINATION_MAX = 20


    for link in categories_soup:

        # (Start at 3, 49 categories == 51 links, stop at 52)
        while link_incrementation < 4:

            # Looking for all the anchors 'a'
            # targeting the next one on each round of the loop
            link= categories_soup.find_all('a')[link_incrementation]
            # Specify search by targeting 'href'
            link = link['href']

            # The name of the category being part of the link, 
            # we extract it directly in the form of a character string
            category_name = \
                str(link).split("/")[-2].split("_")[-2]
            print(category_name)

            category_link = BASE_URL_CATEGORIES + link
            # Add reconstituted link in the list
            print(category_link)

            response_one_category = requests.get(category_link)
            # Parsing of the query result
            soup_category = Soup(response_one_category.text, "html.parser")
            number_expected_results = \
                soup_category.find(
                    "form",
                    {"class": "form-horizontal"}
                            ).find(
                                {"strong": "/strong"}
                            ).text

            number_expected_results = int(number_expected_results)
            number_of_pages = ceil(number_expected_results / PAGINATION_MAX)
            print(
                f" LIVRES CONTENUS:\
                    {number_expected_results}\n",
                f"PAGES A SCANNER:\
                    {number_of_pages}\n",
                f"DIVISION DE CONTRÔLE:\
                    {number_expected_results / PAGINATION_MAX}",
                "\n")
            

            links_of_categories.append(
                                (
                                    category_name,
                                    category_link, 
                                    number_expected_results,
                                    number_of_pages
                                )
                                    )

            link_incrementation += 1
   
    return links_of_categories

def scrap_links_of_books(category_link, BASE_URL_BOOKS, nb_books_to_scan):
    if nb_books_to_scan >= 20:
        nb_books_to_scan = 20

    """Function used to retrieve the links of the books 
    and return a list containing these  links.
    
    This function performs the following tasks:
        - Peeling the list of category links
        - Querying the URL of each link (cat. after cat.)
        - Parsing of the result obtained
        - Selection of targeted tags
        - Converting relative URLs to absolute
        - Returns a list of tuples: (catName, links of books)

    """
    book_links_in_one_page = []
    books_iteration_in_page = 0

    response_one_category = requests.get(category_link)

    # Parsing of the query result
    soup_category = Soup(response_one_category.text, "html.parser")


    for book_link in soup_category:
        # Selection of the link targeted 
        # by the incrementation in the soupCategory
        while books_iteration_in_page < nb_books_to_scan :
            book_link_large = \
                soup_category.find_all(
                    "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}
                                )[books_iteration_in_page]

            # Specify search by targeting 'a' (href link)
            book_link_medium = book_link_large.find('a')
            book_link_small = str(book_link_medium).split('"')
            # We get: ../../../name_of_book/index.html (bookLinkSmall[1])
            book_link_final = str(book_link_small[1]).split('../')
            # We get: name_of_book/index.html (bookLinkFinal[3])

            # The base URL is added to the result
            # to reconstruct an absolute URL
            # before being added to our links list
            book_link = BASE_URL_BOOKS + book_link_final[3]
            book_links_in_one_page.append(book_link)

            books_iteration_in_page += 1
        
    return book_links_in_one_page

def scrap_book_informations(link_of_book, image_path):
    SPECIAL_CHARS = "!@#$%^&\"*[];,./<>?\|~-=_+"

    my_url = link_of_book

    # Définition de l'outil de récolte d'URL
    response = requests.get(my_url, timeout=300)
    # Une fois tous les ingrédients en place,
    # préparation de la soupe HTML
    page_soup = Soup(response.text, "html.parser")

    # Le code HTML indique que le nom est 
    # contenu dans la balise 'h1'
    name_of_book = page_soup.find('h1').text
    for special_char in SPECIAL_CHARS:
        name_of_book = name_of_book.replace(special_char, " ")

    # Handling of the special case where the name begins with a parenthesis

    if name_of_book[0] != "(":
        name_of_book = name_of_book.split("(")[0]
    else:
        print("Cas particulier, les '(' et ')' sont conservées")
    
    # TOTAL removal of spaces and redistribution with ONE space.
    name_of_book = ' '.join(name_of_book.split())

    balises_tr = page_soup.find_all('tr')
    print('Titre livre:', name_of_book)


    # Nous itérons les sous-balises pour récupérer
    # ce que nous cherchons
    for balise in balises_tr:
        """La méthode choisie est un peu répétitive mais
        elle permet de comprendre précisément ce qui est ciblé
        """
        # Le code UPC (Nom de balise ('th') et valeur ('td'))
        if 'UPC' in balise.find('th'):
            upc = balise.find('td')
        # le type de produit
        if 'Product Type' in balise.find('th'):
            product_type = balise.find('td')
        # Le prix hors taxes
        if 'Price (excl. tax)' in balise.find('th'):
            price_excl_tax = balise.find('td')
        # Le prix TTC
        if 'Price (incl. tax)' in balise.find('th'):
            price_incl_tax = balise.find('td')
        # Le montant de la taxe seule
        if 'Tax' in balise.find('th'):
            taxes = balise.find('td')
        # Si c'est en stock et combien en stock
        if 'Availability' in balise.find('th'):
            availability = balise.find('td')
        # Si c'est en stock et combien en stock
        if 'Number of reviews' in balise.find('th'):
            number_of_reviews = balise.find('td')
    star_rating = page_soup.find('article', {'class':'product_pod'}).find('p')
    # Split of 'p tag' and split result to obtain needed value
    nb_of_stars = str(star_rating).split('"')[1].split(' ')[1]


    imageUrl = page_soup.find("div", {"class": "item active"}).find("img")
    trunq = str(imageUrl).split('"')
    # We get: ../../../media/cache/foo/bar/img.jpg (trunq[3])
    save = str(trunq[3]).split('../')
    imageUrl = 'http://books.toscrape.com/' + save[2]

    currentBookInfo = (f"{name_of_book}",
    f"{upc.text}",
    f"{product_type.text}",
    f"{price_excl_tax.text.replace('Â£', '£')}",
    f"{price_incl_tax.text.replace('Â£', '£')}",
    f"{taxes.text.replace('Â£', '£')}",
    f"{availability.text}",
    f"{number_of_reviews.text}",
    nb_of_stars,
    imageUrl)
    print("Informations récupérées")
    scrap_and_save_book_image(
        image_path,
        imageUrl,
        name_of_book)
    print("Image téléchargée")
    return imageUrl, currentBookInfo

def scrap_and_save_book_image(path, imageUrl, nameOfBook):
    responseImage = requests.get(imageUrl)
    nameOfBook = ' '.join(nameOfBook.split(':'))
    nameOfBook = nameOfBook.replace("'", "-")
    with open(f"{path}{nameOfBook}.jpg", "wb") as imageBook:
        imageBook.write(responseImage.content)

def create_folder(path):
    """
    """
    try: 
        os.makedirs(path)
        return True
    except FileExistsError:
        return False
