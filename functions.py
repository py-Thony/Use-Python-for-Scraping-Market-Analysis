# -*- coding: utf-8 -*-

"""
In order to improve the readability and interpretation 
of the general code, the repetitive routine tasks are 
in the form of functions listed here.

Thus, a smaller script (webScraping.py) serves as a bootstrap file 
and only starts the various functions.
"""


# Statements importations
import requests                        # Get url
from bs4 import BeautifulSoup as soup  # Parse result


def scrapLinksOfCategories(url, anteUrlCategories):
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

    response = requests.get(url)
    categoriesSoup = soup(response.text, "html.parser")
    linksOfCategories = [] 
    linkIncrementation = 3 # 1st link != 1st position


    for link in categoriesSoup:
        # (Start at 3 + 49 categories == 52)
        while linkIncrementation < 52:

            # Looking for all the anchors 'a'
            # targeting the next one on each round of the loop
            links= categoriesSoup.find_all('a')[linkIncrementation]
            # Specify search by targeting 'href'
            link = links['href']

            # The name of the category being part of the link, 
            # we extract it directly in the form of a character string
            catName = \
                str(link).split("/")[-2].split("_")[-2]
            
            # Add reconstituted link in the list
            linksOfCategories.append\
                ((catName, (anteUrlCategories + link)))
            linkIncrementation += 1
   
    return linksOfCategories

def scrapLinksOfBooks(categoryLink, anteUrlBooks):
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
    responseCategory = requests.get(categoryLink)

    # Parsing of the query result
    soupCategory = soup(responseCategory.text, "html.parser")
    numberExpectedResults = \
        soupCategory.find(
            "form",
            {"class": "form-horizontal"}
                    ).find(
                        {"strong": "/strong"}
                    ).text

    booksLinksInOneCategory = []
    nextPage = 1    # Iteration of URL's

    allBooksIteration = 0
    booksIterationInPage = 0
    numberExpectedResults = int(numberExpectedResults)

    for bookLink in soupCategory:
        """ The url changes depending on whether 
        we query the first page or the following ones.
        We must provide for 2 scenarios:
            - page1 which increments and changes URLs
            - following pages which only change page number
        """
        while allBooksIteration < numberExpectedResults:

            if booksIterationInPage > 19: # 0-19 => 20 results.
                nextPage += 1
                if nextPage == 2:
                    categoryLink = categoryLink.replace(
                        "index.html",
                        f"page-{nextPage}.html")
                else:
                    categoryLink = categoryLink.replace(
                        f"page-{nextPage-1}.html",
                        f"page-{nextPage}.html")

                booksIterationInPage = 0

            # Selection of the link targeted 
            # by the incrementation in the soupCategory
            bookLink = \
                soupCategory.find_all(
                    "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}
                                )[booksIterationInPage]

            # Specify search by targeting 'a' (href link)
            bookLink = bookLink.find('a')

            trunq = str(bookLink).split('"')
            # We get: ../../../name_of_book/index.html (trunq[1])
            save = str(trunq[1]).split('../')
            # We get: name_of_book/index.html (save[3])

            # The base URL is added to the result
            # to reconstruct an absolute URL
            # before being added to our links list
            bookLink = anteUrlBooks + save[3]
            booksLinksInOneCategory.append(bookLink)

            allBooksIteration += 1
            booksIterationInPage += 1
            # The function is reset on each call, 
            # so there is no need to reset 'nextPage'

    return booksLinksInOneCategory


def scrapBookInformations(linkOfBook, stateOfheader):
    
    myUrl = linkOfBook

    # Définition de l'outil de récolte d'URL
    response = requests.get(myUrl)

    # Une fois tous les ingrédients en place,
    # préparation de la soupe HTML
    pageSoup = soup(response.text, "lxml")

    # Le code HTML indique que le nom est 
    # contenu dans la balise 'h1'
    nameOfBook = pageSoup.find('h1')

    # En inspectant le code HTML, nous constatons
    # que les infos recherchées sont dans une balise 'tr'
    # Nous ciblons donc les occurences correspondant à 'tr'
    balisesTr = pageSoup.find_all('tr')

    # Nous itérons les sous-balises pour récupérer
    # ce que nous cherchons
    for balise in balisesTr:
        """La méthode choisie est un peu répétitive mais
        elle permet de comprendre précisément ce qui est ciblé
        """
        # Le code UPC (Nom de balise ('th') et valeur ('td'))
        if 'UPC' in balise.find('th'):
                upcName = balise.find('th')
                upc = balise.find('td')
        # le type de produit
        if 'Product Type' in balise.find('th'):
                productTypeName = balise.find('th')
                productType = balise.find('td')
        # Le prix hors taxes
        if 'Price (excl. tax)' in balise.find('th'):
            priceExclTaxName = balise.find('th')
            priceExclTax = balise.find('td')
        # Le prix TTC
        if 'Price (incl. tax)' in balise.find('th'):
                priceInclTaxName = balise.find('th')
                priceInclTax = balise.find('td')
        # Le montant de la taxe seule
        if 'Tax' in balise.find('th'):
                taxesName = balise.find('th')
                taxes = balise.find('td')
        # Si c'est en stock et combien en stock
        if 'Availability' in balise.find('th'):
                availabilityName = balise.find('th')
                availability = balise.find('td')

    # Nous pouvons ainsi afficher nos informations
    print('Titre livre:', nameOfBook.text)
    # create header if 1st book
    if stateOfheader:
        currentBook = \
            f"Book title,\
                {upcName.text},\
                    {productTypeName.text},\
                        {priceExclTaxName.text},\
                            {priceInclTaxName.text},\
                                {taxesName.text},\
                                    {availabilityName.text}\n"\
            f"{nameOfBook.text},\
                {upc.text},\
                    {productType.text.replace('Books', ' Livres')},\
                        {priceExclTax.text.replace('Â£', ' £ ')},\
                            {priceInclTax.text.replace('Â£', ' £ ')},\
                                {taxes.text.replace('Â£', '£ ')},\
                                    {availability.text}\n"
    else:
        currentBook = \
            f"{nameOfBook.text},\
                {upc.text},\
                    {productType.text.replace('Books', ' Livres')},\
                        {priceExclTax.text.replace('Â£', ' £ ')},\
                            {priceInclTax.text.replace('Â£', ' £ ')},\
                                {taxes.text.replace('Â£', '£ ')},\
                                    {availability.text}\n"

    return currentBook

def WriteToTextFile(
    Path,
    FileName,
    Text,
    Action = "w"):
    """
        Write (or append) Text to text file 
        depending on action ("w" or "a")
        Return Success or Failure
    """

    try:

        with open(Path + FileName, Action, encoding="utf-8") as MyFile:
            MyFile.write(Text)
        return True
            
    except FileNotFoundError:
        print(f"\nLe fichier {Path}{FileName} n'existe pas.\n")
        return False