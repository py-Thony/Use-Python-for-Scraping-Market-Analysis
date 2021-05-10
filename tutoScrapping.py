
"""
Web Scraping pour créer un fichier CSV

Nous avons donc besoin de deux packages principaux pour cette tâche, 
                BeautifulSoup et urllib. 

Nous pouvons facilement installer ces deux packages en utilisant la commande pip
            pip install bs4 et pip install urllib. 
"""

# Après avoir installé ces packages avec succès, 
# la prochaine chose à faire est d'importer les packages           
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 

# Mise en service d'une condition booléenne
scrappingInCourse = True
containers = []
pageNumber = 0
i = 0
# Prédiction du nombre de page à éplucher
# la balise _2tDckM indique le nombre de résultats total
# Nous allons donc diviser la lenValeur de _2tDckM par le pageSize (ici 24)
while scrappingInCourse:

    pageNumber += 1
    print(f"Analyse de la page N° {pageNumber} en cours...", end='')
    # Récupérer le lien dont nous avons besoin pour collecter les données:
    my_url="https://www.flipkart.com/search?q=samsung+mobiles&amp;sid=tyy%2C4io&amp;as=on&amp;as-show=on&amp;otracker=AS_QueryStore_HistoryAutoSuggest_0_2&amp;otracker1=AS_QueryStore_HistoryAutoSuggest_0_2&amp;as-pos=0&amp;as-type=HISTORY&amp;as-searchtext=sa&page=" + str(pageNumber)

    uClient = uReq(my_url) 
    page_html = uClient.read()

    uClient.close() 
    page_soup = soup(page_html, "html.parser")

    container = page_soup.findAll("div", { "class": "_2kHMtA"})
    iw = 0
    stop = len(container)
    while iw < (stop -1):
        iw += 1
        
        for reslt in container[iw]:
            print(soup.prettify(reslt))
            input()
            name = container[iw].find("div", {"class": "_4rR01T"})
            price = container[iw].find("div", {"class": "_30jeq3"})

            print(f" -> {name.text} est vendu au prix de {price.text}.")

    if len(container) < 24 or pageNumber > 3:
        scrappingInCourse = False
        print("Nous avons atteint la fin de la liste.")
    else:
        print(f"Qui contient {len(container)} résultats.")
