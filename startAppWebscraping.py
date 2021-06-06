# -*- coding: utf8 -*-

import time   # gestion du temps d'attente pour espacer les requetes
import requests # interrogation des url
from bs4 import BeautifulSoup as soup # mise en lecture humaine du html

## Pseudo code

# récupérer la soupe html du site a son index
""" Une fonction rapide peut se charger d'interroger l'url
puis de récupérer chaque lien et de directement les interroger
pour sauveagarder les liens des livres.
"""
## Une variableList est assignée au résultat de la fonction rapide
""" Nous obtenons ainsi une liste composée de tuples
    [(NomCategorie, (listesLiensLivres)))
"""
### Une fonction se charge alors de faire une requete pour chaque livre
""" Le nom de la catégorie sert à nommer et créer le dossier, la fonction
capte les infos textuelles avec une première requête, et les images avec une
requête.