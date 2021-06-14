# -*- coding: utf-8 -*-

"""
This script is responsible for querying the site www.books.toscrape.com

CONCEPTION:
Step 1: Extraction of URLS from each category and listing.

Step 2: Peel this list to scrape all book links
        and generate tuples listing (category name, [link list])

Step 3: Query each book link to:
                    - Extraction of textual information
                    - Download the image of the book
Step 3bis: Creation of self-named parent files according to the name of the category,
            Creation of 'CSV' and 'IMAGES' child folders
            Saving text data to a CSV file in the CSV folder
            Saving images renamed with the title of the book in the IMAGES folder

Having problems controlling where to create folders,
(under Windows 10 machine, VScode) it was necessary to create a function.
'CreateFolder' and define the Path manually.
Encountering particular cases in the titles of books, it was necessary
to manage these exceptions by replacing certain symbols. (eg: commas <!> CSV)

TREE:
scrapBooking.py >>> general operation of the program and settings
scrapBookingFuncions.py >>> repetitive routines passed as functions to call.

GENERATION OF FOLDERS AND FILES:
parent folder with the category name
    -> Child folder named CSV
        -> file.csv with the name of the category
    -> Child folder named IMAGES
        -> saving images in JPG format and renamed with the title of the book

"""

################################
# Imports of necessary modules #
################################
import os
import csv

################################
# Importing personal functions #
################################

from scrapBookingFunctions import create_folder
from scrapBookingFunctions import scrap_links_of_categories
from scrapBookingFunctions import scrap_links_of_books
from scrapBookingFunctions import scrap_book_informations

""" First, you have to connect to the targeted site.

An examination of the HTML code allows to detect the use of URLs
relative, so we will need a base url for the
rebuild categories and product pages into absolute URLs.
"""
WEBSITE_URL = 'http://books.toscrape.com/index.html'

# To reconstruct relative links into absolute links
BASE_URL_CATEGORIES = 'http://books.toscrape.com/'
BASE_URL_IMAGES = 'http://books.toscrape.com/'
BASE_URL_BOOKS = 'http://books.toscrape.com/catalogue/'

# Auto fill the list of category links
links_of_categories = scrap_links_of_categories(
                                WEBSITE_URL,
                                BASE_URL_CATEGORIES)

all_books_links_list = []
for one_category in links_of_categories:
    # Management of the special case of categories with several pages
    provisional_links_list = []

    next_page = 1
    books_scraped = 0
    category_name = one_category[0].capitalize()
    category_link = one_category[1]
    expected_books = one_category[2]
    nb_pages_to_scan = one_category[3]

    print(category_name, "\n", category_link)
    while next_page <= nb_pages_to_scan:
        
        nb_pages_to_scan = expected_books - books_scraped

        if next_page == 2:
            print(f"Page N°{next_page}")
            category_link = category_link.replace(
                "index.html",
                f"page-{next_page}.html")

        elif next_page > 2:
            print(f"Page N°{next_page}")
            category_link = category_link.replace(
                f"page-{next_page-1}.html",
                f"page-{next_page}.html")

        scan_page_in_course = scrap_links_of_books(
                                category_link,
                                BASE_URL_BOOKS,
                                nb_pages_to_scan)

        for element in scan_page_in_course:
            provisional_links_list.append(element)

        books_scraped += len(scan_page_in_course)
        next_page += 1
    print(">>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<")
    # Retrieving all book links for the current category
    all_books_links_list.append(
        (
            category_name,
            provisional_links_list))

""" At this stage we have a general list
containing a sublist per category.

Each sublist is in the form of a tuple,
(catName, (booksListen))
"""
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FIELDS=[
    'Book Title','UPC Code','Product Type', 
    'Price (ExclTax)', 'Price (InclTax)', 'Taxes', 
    'Availability', 'number_of_reviews', 'nb_of_stars',
    'Image Url']
count_books = 0
for links_of_book_in_one_category in all_books_links_list:

    category_name = links_of_book_in_one_category[0]

    CSV_PATH = f"{ROOT_DIR}\\SCRAPED_FILES\\{category_name}\\CSV_FILES\\"
    IMAGE_PATH = f"{ROOT_DIR}\\SCRAPED_FILES\\{category_name}\\IMAGES\\"
    create_folder(CSV_PATH)
    create_folder(IMAGE_PATH)

    list_of_all_books_info = []
    for book_link in links_of_book_in_one_category[1]:
        count_books += 1
        print(count_books)
        # Retrieving information from the book
        current_book_info = scrap_book_informations(book_link, IMAGE_PATH, BASE_URL_IMAGES)
        list_of_all_books_info.append(current_book_info)

    # WRITE name_of_category.CSV with auto-close
    with open(
        f"{CSV_PATH}{category_name}.csv",
        'w',
        encoding="utf-8",
        newline=''
        ) as CSVfile:
        # CSV configuration
        spamwriter = csv.writer(
            CSVfile,
            delimiter=',',
            quotechar=' ',
            quoting=csv.QUOTE_MINIMAL
            )
        # One line
        spamwriter.writerow(FIELDS)
        # All others lines
        spamwriter.writerows(list_of_all_books_info)
        print("------------------------->")
        print(f"ENREGISTRMENT CSV TERMINE {category_name}")
        print("------------------------->")
