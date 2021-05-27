# coding: utf_8

# Web Scraping pour créer un fichier CSV

"""
Il est demandé de d'abord démontrer sa faculté à interroger et
récupérer les informations d'une fiche produit, raison d'être
de ce fichier 'firstScrap.py'

Les commentaires sont en français et la PEP non respectée concernant
la longueur des lignes car il s'agit ici unquement d'une démonstration de
compréhension lors de la soutenance de projet.

Nous avons besoin de deux packages pour cette tâche, 
                BeautifulSoup pour récupérer les infos HTML
                et requests pour interroger une URL. 

Nous pouvons facilement installer ces deux packages 
en utilisant la commande pip
            pip install bs4 et pip install requests. 
"""

# Après avoir installé ces packages avec succès, 
# la prochaine chose à faire est d'importer les packages           
from bs4 import BeautifulSoup as soup 
import requests
import csv

# Toutes les futures opérations auront besoin
# d'une URL à connecter pour l'interroger.
myUrl="http://books.toscrape.com/catalogue/" + \
      "a-light-in-the-attic_1000/index.html"

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

-> 'with open' permet la fermeture dynamique alors que 'open' nous force
          à fermer le fichier manuellement, causant des erreurs si oubli
-> 'w' indique le mode 'write' pour écrire ou écraser le fichier
   'r+' permet lecture + écriture
-> 'as' pour associer le nom du fichier à une variable plus simple à utiliser
"""

with open('firstScrap.csv', 'w') as fileCSV:
      fileCSV = csv.writer(fileCSV,delimiter=",",quotechar='"')
      # Indication de mise en page (séparation par des ',')
      # '\' permet de couper une ligne sans incidence sur le code
      fileCSV.writerow(["Nom du livre",
                        "Code UPC",
                        "Type de produit",
                        "Prix hors taxes",
                        "Prix TTC",
                        "Montant de la taxe",
                        "Stock disponible"])
      # Maintenant que les noms de colonnes sont définis, nous insérons
      # les valeurs correspondantes (c'est l'ordre qui prime)
      """
      Nous avons déjà récupéré les valeurs donc nous utiliserons ici les variables
      définies plus haut dans le code.
      Nous pourrions directement récupérer les valeurs depuis la soupe html"""

      fileCSV.writerow([nameOfBook.text,
                     upc.text,
                     productType.text,
                     priceExclTax.text,
                     priceInclTax.text,
                     taxes.text,
                     availability.text])