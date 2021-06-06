# -*- coding: utf-8 -*-
"""Deliverable for project 2 -- Webscraping of www.book-toscrape.com

This script captures the link of each category,
then requests each link of category to capture
the link of each book, then retrieves the requested informations.
Finally, it saves everything in a CSV file independent for each category.

Since it is not possible to insert images into a CSV file,
the upload of the image is done separately in a specific folder.
The link to this local image will be added to the corresponding CSV line
to be able to link the image and textual information
during the output displayed to the user.

It is expected to respect PEP8
and to comment in English

But, addressed to a French audience,
the messages intended for the user will be in French.
"""

# import statements
import csv
import time

from functions import WriteToTextFile, scrapImageOfBook, scrapLinksOfCategories
from functions import scrapLinksOfBooks
from functions import scrapBookInformations


websiteUrl = 'http://books.toscrape.com/index.html'

# To rebuild the relative links of categories
baseUrlCategories = 'http://books.toscrape.com/'
# To rebuild the relative links of books
baseUrlBooks = 'http://books.toscrape.com/catalogue/'
# Retrieving all category links
linksOfCategories = scrapLinksOfCategories(websiteUrl, baseUrlCategories)
# Peeling links
for oneCategory in linksOfCategories:
    stateOfHeader = True
    # Defining names and links separately
    categoryName = oneCategory[0]
    categoryLink = oneCategory[1]
    # Retrieving all book links for the current category
    linksOfBooksInOneCategory = scrapLinksOfBooks(categoryLink, baseUrlBooks)
    time.sleep(0.5)
    headers = 0
    # Peeling links in current category
    for linkOfBook in linksOfBooksInOneCategory:
        headers += 1
        if headers > 1:
            stateOfHeader = False
        # Retrieving information from the book
        currentBookInfo = scrapBookInformations(linkOfBook, stateOfHeader)
        time.sleep(0.5)
        
        WriteToTextFile("", f"{categoryName}.csv", f"{currentBookInfo}\n", "a")