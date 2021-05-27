# -*- coding: utf-8 -*-

"""
Livrable pour projet 2

Ce script capte le lien de chaque catégorie, puis requête chaque lien
pour capter le lien de chaque livre, puis récupère les infos demandées.

Enfin, il enregistre le tout dans un fichier CSV

Il est attendu de respecter au mieux la PEP8 et de commenter en anglais
"""

# import statements
import requests                         # GET url
from bs4 import BeautifulSoup as soup   # Parse result
import csv

# Declaration of the URL to query
url = 'http://books.toscrape.com/index.html'

# Declaration of the piece of URL 
# to insert to rebuild the relative links
anteUrl = 'http://books.toscrape.com/'

# Querying the URL
response = requests.get(url)

# Parsing of the query result
pageSoup = soup(response.text, "html.parser")

# Declaration of a list to store category links
linksOfCategories = []

i = 3 # The first link is not in the first position
for link in pageSoup:

    while i < 5:   # To stop at the end of list
                    # (Start at 3 + 49 categories == 52)

        # Looking for all the anchors 'a'
        links= pageSoup.find_all('a')[i]
        # Specify search by targeting 'href'
        link = links['href']
        catName = str(link).split("/")[-2].split("_")[-2]


        i += 1
        # Add reconstituted link in the list
        linksOfCategories.append((catName, (anteUrl + link)))


"""
Now that we have retrieved the links for each category, 
we can do much the same operation to retrieve the links 
for each 
"""
# Declaration of a list to books category links

listOfCategories = []
next = 1    # Iteration of URL's

for cat in linksOfCategories:
    
    category = cat[1]
    categoryName = cat[0]

    # Declaration of the piece of URL 
    # to insert to rebuild the relative links
    anteUrl = 'http://books.toscrape.com/catalogue/'

    # Querying the URL
    responseCat = requests.get(category)

    # Parsing of the query result
    catSoup = soup(responseCat.text, "html.parser")
    
    numberOfResults = \
        catSoup.find\
            ("form", {"class": "form-horizontal"}).find({"strong": "/strong"}).text

    numberOfResults = int(numberOfResults)
    if numberOfResults > 1:
        s = 's'
    else:
        s = ''
    print(categoryName, "\n", category)
    #print(f" Contient: {numberOfResults} livre{s}\n")

    i = 0       # Iteration of total books
    ii = -1      # iteration to move to next page
    iii = 0     # Iteration in page
    
    listOfBooks = []
    for link in catSoup:

        while i < numberOfResults:
            ii += 1
            if ii > 19:
                
                next += 1
                if next == 2:
                    category = category.replace("index.html", f"page-{next}.html")
                else:
                    category = category.replace(f"page-{next-1}.html", f"page-{next}.html")

                ii = 0
                iii = 0
            
            # Looking for all the tag of books
            booksLinks= \
                catSoup.find_all\
                    ("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})[iii]

            # Specify search by targeting 'a' (href link)
            bookLink = booksLinks.find('a')

            """
            Not knowing how to isolate a relative URL in a tag, 
            I chose to split the tag after having passed it into a character string 
            to output the desired part (book reference / index.html)
            """
            trunq = str(bookLink).split('"')
            # At this point we get: ../../../name_of_book/index.html (trunq[1])
            save = str(trunq[1]).split('../')
            # At this point we get: name_of_book/index.html (save[3])

            # The base URL is added to the result to reconstruct an absolute URL
            bookLink = anteUrl + save[3]
            listOfBooks.append(bookLink)


            i += 1
            iii += 1
        next = 1
    listOfCategories.append((categoryName,listOfBooks))

b = 0
for category in listOfCategories:
    
    for bookUrl in category[1]:
        myUrl = bookUrl

    # Définition de l'outil de récolte d'URL
    response = requests.get(myUrl)

    # Une fois tous les ingrédients en place,
    # préparation de la soupe HTML
    pageSoup = soup(response.text, "lxml")

    # Le code HTML indique que le nom est contenu dans la balise 'h1'
    nameOfBook = pageSoup.find('h1')

    # En inspectant le code HTML, nous constatons
    # que les infos recherchées sont dans une balise 'tr'
    #
    # Nous ciblons donc les occurences correspondant à 'tr'
    balisesTr = pageSoup.find_all('tr')

    # Nous itérons les sous-balises pour récupérer
    # ce que nous cherchons
    for balise in balisesTr:
        """
        La méthode choisie est un peu répétitive mais
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

    # Nous pouvons ainsi afficher nos informations déjà mises en page
    # pour vérifier que nous obtenons bien ce que nous attendons
    print('Book title :', nameOfBook.text)
    print(upcName.text, ':', upc.text)
    print(productTypeName.text, ':', productType.text.replace('Books', ' Livres'))
    print(priceExclTaxName.text, ':', priceExclTax.text.replace('Â£', ' £ '))
    print(priceInclTaxName.text, ':', priceInclTax.text.replace('Â£', ' £ '))
    print(taxesName.text, ':', taxes.text.replace('Â£', '£ '))
    print(availabilityName.text, ':', availability.text)

    """
    Nous pouvons maintenant enregistrer notre résultat dans un fichier CSV

    """

"""
-> 'with open' permet la fermeture dynamique alors que 'open' nous force
        à fermer le fichier manuellement, causant des erreurs si oubli
-> 'w' indique le mode 'write' pour écrire ou écraser le fichier
'r+' permet lecture + écriture
-> 'as' pour associer le nom du fichier à une variable plus simple à utiliser
"""


with open('firstScrap.csv', 'w', newline='') as fileCSV:
    spamwriter = csv.writer(fileCSV, delimiter=' ',
                        quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    # Maintenant que les noms de colonnes sont définis, nous insérons
    # les valeurs correspondantes (c'est l'ordre qui prime)
    """
    Nous avons déjà récupéré les valeurs donc nous utiliserons ici les variables
    définies plus haut dans le code.
    Nous pourrions directement récupérer les valeurs depuis la soupe html"""

    spamwriter.writerow([nameOfBook.text,
                    upc.text,
                    productType.text,
                    priceExclTax.text,
                    priceInclTax.text,
                    taxes.text,
                    availability.text])
