<div align="center">

# Using Python Basics for Market Analysis
</div>

<p align="center">
  <img width="200" src="https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png" alt="Material Bread logo">
</p>

<div align="center">

___Scraping of books.toscrape.com___
by [py-Thony](https://github.com/py-Thony "Click to access my GitHub profile and discover my other projects.")

</div>

---

<div align="center">

___A program (a scraper) developed in Python, capable of extracting price information and download images.___
</div>

---
<br/>
<br/>

# Before you start

### Creation of the virtual environment
Official python documentation:
    - [Python3 venv docs](https://docs.python.org/fr/3/library/venv.html "Documentation for creating and using a virtual environment to work free from version conflicts.")
```bash
python3 -m venv /path/to/new/virtual/environment
```

VScode specific documentation:
    - [VScode venv docs](https://code.visualstudio.com/docs/python/environments "Documentation for creating and using a virtual environment to work free from version conflicts.")
```bash
python -m venv .venv
```

### Installation of libraries
_A requirements.txt file allows you to find out the list of libraries necessary for the proper functioning of the program._

__To start the installation automatically:__
>Version Of libraries (Python3)
>>The versions are indicated from the day of creation but you can update them
```bash
pip install -r requirements.txt
```

<br/>

# Description of the program
The program consists of 2 files:

:one:___scrapBooking.py___

_This script is responsible for scraping the site http://books.toscrape.com/_
<details>
  <summary>_Read More_</summary>
  <p>

__CONCEPTION:__

:point_right:__Step 1:__ 

Extraction of URLS from each category and listing.

:point_right:__Step 2:__ 

Peel this list to scrape all book links
        and generate tuples listing (category name, [link list])

:point_right:__Step 3:__ 

Query each book link to:
* Extraction of textual information
* Download the image of the book

:point_right:__Step 3bis:__ 

Creation of self-named parent files according to the name of the category:
* Creation of 'CSV' and 'IMAGES' child folders
* Saving text data to a CSV file in the CSV folder
* Saving images renamed with the title of the book in the IMAGES folder


__GENERATION OF FOLDERS AND FILES:__

* ___Parent folder___ with the category name
    - ___Child folder___ named CSV
        - File.csv with the name of the category
    - ___Child folder___ named IMAGES
        - Saving images in JPG format and renamed with the title of the book
</p>
</details>


:two:___scrapBookingFunctions.py___

_This file groups together the functions created to manage the different routines of the main script_
<details>
  <summary>_Read More_</summary>
  <p>

:arrow_right:__scrap_links_of_categories__

Function used to retrieve the links of the categories.

:arrow_right:__scrap_links_of_books__

Function used to retrieve the links of the books.

:arrow_right:__scrap_book_informations__

This function retrieves the following information:
- Book name
- UPC code
- Type of product
- Price (with and without tax, and tax only)
- The availability
- the number of comments
- the star rating
- the url of the image
And download the images.

:arrow_right:__scrap_and_save_book_image__

Function used to download the image of each book.

:arrow_right:__create_folder__

Function used only to manage
a possible error during file access, 
the path settings are deliberately 
processed in the same place as the calls 
for the sake of readability
</p>
</details>

<br/>

# How do I scrape the entire books.toscrape.com?

___Just start scrapBooking.py !___ _and Enjoy !!_

___The work will be done by itself! And scrap the 1000 books!___

___All you have to do is have a coffee, the operation lasts about 15 minutes___

<br/>

# Presentation of the results obtained

### Result in CSV

_Once the textual information of all the books in the category is recovered, everything is saved in a.csv file as below:_

| Book  Title | UPC Code | Product Type | Price(ExclTax) | Price(InclTax) | Taxes | Availability | Number of reviews | nb of stars | Image Url |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Book  Title | UPC  Code | Product  Description | Price  (ExclTax) | Price  (InclTax) | Taxes |Availability | number_of_reviews | nb_of_stars | Image  Url |
| It's  Only  the  Himalayas | a22124811bfa8350 | Wherever  you  go  whatever  you  do  just  .  .  .  don't  do  anything  stupid. My  MotherDuring  her  yearlong  adventure  backpacking  from  South  Africa  to  Singapore  S. Bedford...[Shortcut for easy readability] | £45.17 | £45.17 | £0.00 | In  stock  (19  available) | 0 | Two | http://books.toscrape.com/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg |
| Full  Moon  over  Noah's  Ark:  An  Odyssey  to  Mount  Ararat  and  Beyond | ce60436f52c5ee68 | Acclaimed  travel  writer  Rick  Antonson  sets  his  adventurous  compass  on  Mount  Ararat  exploring  the  regions  long  history...[Shortcut for easy readability] | £49.43 | £49.43 | £0.00 | In  stock  (15  available) | 0 |Four | http://books.toscrape.com/media/cache/fe/8a/fe8af6ceec7718986380c0fde9b3b34f.jpg |
| See  America:  A  Celebration  of  Our  National  Parks  Treasured  Sites | f9705c362f070608 | To  coincide  with  the  2016  centennial  anniversary  of  the  National  Parks  Service  the  Creative  Action  Network  has  partnered...[Shortcut for easy readability] | £48.87 | £48.87 | £0.00 | In  stock  (14  available) | 0 | Three |http://books.toscrape.com/media/cache/c7/1a/c71a85dbf8c2dbc75cb271026618477c.jpg |
| Vagabonding:  An  Uncommon  Guide  to  the  Art  of  Long  Term  World  Travel | 1809259a5a5f1d8d | With  a  new  foreword  by  Tim  Ferriss  There's  nothing  like  vagabonding:  taking  time  off  from  your  normal  life from  six  weeks  to  four  months  to  two  years to  discover  and  experience...[Shortcut for easy readability] | £36.94 | £36.94 | £0.00 | In  stock  (8  available) | 0 | Two | http://books.toscrape.com/media/cache/ca/30/ca30b1afe1e76ce7ba1db8176d398e53.jpg |
| Under  the  Tuscan  Sun | a94350ee74deaa07 | A  CLASSIC  FROM  THE  BESTSELLING  AUTHOR  OF  UNDER  MAGNOLIA Frances  Mayes widely  published  poet  gourmet  cook  and  travel  writer opens  the  door  to  a  wondrous  new  world....[Shortcut for easy readability] | £37.33 | £37.33 | £0.00 | In  stock  (7  available) | 0 | Three | http://books.toscrape.com/media/cache/45/21/4521c581ba727f5c835e34860cbf53e5.jpg |
| A  Summer  In  Europe | cc1936a9f4e93477 | On  her  thirtieth  birthday  Gwendolyn  Reese  receives  an  unexpected  present  from  her  widowed  Aunt  Bea:  a  grand  tour  of  Europe  in  the  company  of  Bea's  Sudoku  and  Mahjongg  Club...[Shortcut for easy readability]  | £44.34 | £44.34 | £0.00 | In  stock  (7  available) | 0 | Two | http://books.toscrape.com/media/cache/6c/e3/6ce3003931701c7a3fd5354917538ea9.jpg |

### Tree structure

_While running, the script creates a tree like this:_

![alt text](https://github.com/py-Thony/Use-Python-for-Scraping-Market-Analysis/blob/master/Livrables/tree.JPG?raw=true)


# Potential malfunction

_The program may stop working if the site's HTML tags are renamed._
_In this case you will have to update them and either propose a PullRequest_
_or leave me a comment so that I can correct the problem._

</br>

<div align="center">

#### :snake:If you are forking please do not forget to star the repo:snake:

</br>
