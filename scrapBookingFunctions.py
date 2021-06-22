# -*- coding: utf-8 -*-

""" This file groups together the functions created
to manage the different routines of the main script

For the sake of maintaining the version of the comments,
each function has its own explanatory docstring.
"""

################################
# Imports of necessary modules #
################################

import os
import requests
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
    # 1st link != 1st position
    link_incrementation = 3
    PAGINATION_MAX = 20

    for link in categories_soup:
        # (Start at 3, 50 categories == 52 links, stop at 53)
        while link_incrementation < 53:
            # Looking for all the anchors 'a' one by one
            link = categories_soup.find_all('a')[link_incrementation]
            # Specify search by targeting 'href' to target the url
            link = link['href']
            # Extraction of the category name
            category_name = str(link).split("/")[-2].split("_")[-2]
            # Absolute URL reconstruction
            category_link = BASE_URL_CATEGORIES + link
            # Requests and parsing HTML
            response_one_category = requests.get(category_link)
            soup_category = Soup(response_one_category.text, "html.parser")
            # Extraction of the number of books to recover and convert to int
            number_expected_results = \
                soup_category.find(
                    "form", {"class": "form-horizontal"}).find(
                        {"strong": "/strong"}).text
            number_expected_results = int(number_expected_results)
            # Prediction of the number of pages to be scanned
            number_of_pages = ceil(number_expected_results / PAGINATION_MAX)
            # Prints allows a better user experience
            print(category_name)
            print(category_link)
            print(
                f" LIVRES CONTENUS:\
                    {number_expected_results}\n",
                f"PAGES A SCANNER:\
                    {number_of_pages}\n",
                f"DIVISION DE CONTRÔLE:\
                    {number_expected_results / PAGINATION_MAX}",
                "\n")
            
            # Save
            links_of_categories.append((
                category_name,
                category_link,
                number_expected_results,
                number_of_pages))

            link_incrementation += 1
   
    return links_of_categories


def scrap_links_of_books(category_link, BASE_URL_BOOKS, nb_books_to_scan):

    if nb_books_to_scan >= 20:
        nb_books_to_scan = 20

    """Function used to retrieve the links of the books
    and return a list containing these  links.

    This function performs the following tasks:
        - Querying the URL of each link received as a parameter
        - Parsing of the result obtained
        - Selection of targeted tags of books
        - Converting relative URLs to absolute
        - Returns a list of tuples: (catName, links of books)

    """
    book_links_in_one_page = []
    books_iteration_in_page = 0
    # Requests and parsing HTML
    response_one_category = requests.get(category_link)
    soup_category = Soup(response_one_category.text, "html.parser")

    for book_link in soup_category:
        # Selection of the link targeted by incrementation
        while books_iteration_in_page < nb_books_to_scan:
            book_link_large = soup_category.find_all(
                "li",
                {
                    "class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"
                })[books_iteration_in_page]

            # Specify search by targeting 'a' (href link)
            book_link_medium = book_link_large.find('a')
            book_link_small = str(book_link_medium).split('"')
            # We get: ../../../name_of_book/index.html (bookLinkSmall[1])
            book_link_final = str(book_link_small[1]).split('../')
            # We get: name_of_book/index.html (bookLinkFinal[3])

            # Absolute URL reconstruction
            book_link = BASE_URL_BOOKS + book_link_final[3]
            # Save
            book_links_in_one_page.append(book_link)

            books_iteration_in_page += 1
        
    return book_links_in_one_page


def scrap_book_informations(link_of_book, IMAGE_PATH, BASE_URL_IMAGES):
    """ This function retrieves the following information:
        - Book name
        - UPC code
        - Description of Book
        - Price (with and without tax, and tax only)
        - The availability
        - the number of comments
        - the star rating
        - the url of the image
        
        Once all the operations have been correctly executed,
        everything is returned as a simple list

        Taking advantage of the access to the URL of the image,
        the function automatically calls the function
        allowing to download it during peeling.
    """
    # Defining a constant containing unwanted characters
    # avoids stacking '.replace ()'
    SPECIAL_CHARS = '!@#$%^&"*[];,./<>?\~-=_+'

    # Requests and parsing HTML
    my_url = link_of_book
    response = requests.get(my_url, timeout=300)
    page_soup = Soup(response.text, "html.parser")

    # The HTML code indicates that the name is
    # contained in the 'h1' tag
    name_of_book = page_soup.find('h1').text
    # Read character by character and replace if unwanted
    for special_char in SPECIAL_CHARS:
        name_of_book = name_of_book.replace(special_char, " ")
    # Handling of the special case where the name begins with a parenthesis
    if name_of_book[0] != "(":
        name_of_book = name_of_book.split("(")[0]
    else:
        print("Cas particulier, les '(' et ')' sont conservées")
    # TOTAL removal of spaces and redistribution with ONE space.
    name_of_book = ' '.join(name_of_book.split())

    # The HTML code that our information is in 'tr'
    balises_tr = page_soup.find_all('tr')
    print('Titre livre:', name_of_book)

    for balise in balises_tr:
        # (Tag name ('th') and value ('td'))
        if 'UPC' in balise.find('th'):
            upc = balise.find('td')
        if 'Price (excl. tax)' in balise.find('th'):
            price_excl_tax = balise.find('td')
        if 'Price (incl. tax)' in balise.find('th'):
            price_incl_tax = balise.find('td')
        if 'Tax' in balise.find('th'):
            taxes = balise.find('td')
        if 'Availability' in balise.find('th'):
            availability = balise.find('td')

    # The star rating is contained elsewhere
    star_rating = page_soup.find(
        'div', {'class': 'col-sm-6 product_main'}).findAll('p')
    # Split of 'p tag' and split result to obtain needed value
    reviews_rating = str(star_rating[2]).split('"')[1].split(' ')[1]

    product_description = page_soup.find_all('p')[3].text

    BANNED_CHARS = 'âÂ@#$%^&"*[];,/<>\~-=_+'
    for replaced_char in BANNED_CHARS:
        product_description = product_description.replace(replaced_char, "")

    product_description = product_description[:-8]
    ' '.join(product_description.split())

    image_url = page_soup.find("div", {"class": "item active"}).find("img")

    trunq = str(image_url).split('"')
    # We get: ../../../media/cache/foo/bar/img.jpg (trunq[3])
    save = str(trunq[3]).split('../')
    # Absolute URL reconstruction
    image_url = BASE_URL_IMAGES + save[2]

    current_book_info = (
        f"{name_of_book}",
        f"{upc.text}",
        f"{product_description}",
        f"{price_excl_tax.text.replace('Â£', '£')}",
        f"{price_incl_tax.text.replace('Â£', '£')}",
        f"{taxes.text.replace('Â£', '£')}",
        f"{availability.text}",
        reviews_rating,
        image_url)
    print("Informations récupérées")

    scrap_and_save_book_image(
        IMAGE_PATH,
        image_url,
        name_of_book)
    print("Image téléchargée")

    return current_book_info


def scrap_and_save_book_image(IMAGE_PATH, image_url, name_of_book):
    """ Function used to download
        the image of each book.
    """
    # Parsing
    response_image = requests.get(image_url)
    # Name normalization
    name_of_book = ' '.join(name_of_book.split(':'))
    name_of_book = name_of_book.replace("'", "-")
    #Save
    with open(f"{IMAGE_PATH}{name_of_book}.jpg", "wb") as image_book:
        # contents refers to Binary Response content
        image_book.write(response_image.content)


def create_folder(PATH):
    """ Function used only to manage
    a possible error during file access,
    the path settings are deliberately
    processed in the same place as the calls
    for the sake of readability
    """
    try:
        # Create folderS (Entire tree)
        os.makedirs(PATH)
        return True
    except FileExistsError:
        return False