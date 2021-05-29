# -*- coding: utf-8 -*-
"""
Deliverable for project 2

This script captures the link of each category, 
then requests each link of categroy to capture 
the link of each book, then retrieves the requested information.
Finally, it saves everything in a CSV file

It is expected to respect PEP8 as best as possible 
and to comment in English
"""

# import statements
import csv                                  # Save csv allows table display
from functions import WriteToTextFile       # Function to replace csv
from functions import scrapLinksOfCategories
from functions import scrapLinksOfBooks
from functions import scrapBookInformations

booksToCSV = ""

# Declaration of the URL to query
url = 'http://books.toscrape.com/index.html'
# to insert to rebuild the relative links of categories
anteUrlCategories = 'http://books.toscrape.com/'
# to insert to rebuild the relative links of books
anteUrlBooks = 'http://books.toscrape.com/catalogue/'

linksOfCategories = scrapLinksOfCategories(url, anteUrlCategories)

for oneCategory in linksOfCategories:

    categoryName = oneCategory[0]
    categoryLink = oneCategory[1]

    linksOfBooksInOneCategory = scrapLinksOfBooks(categoryLink, anteUrlBooks)

    for linkOfBook in linksOfBooksInOneCategory:
        if booksToCSV == "":
            stateOfheader = True
        else:
            stateOfheader = False
        currentBook = scrapBookInformations(linkOfBook, stateOfheader)

        booksToCSV += currentBook
    
    WriteToTextFile("./filesCSV", f"{categoryName}.csv", booksToCSV)

input("Verification du fichier CSV")