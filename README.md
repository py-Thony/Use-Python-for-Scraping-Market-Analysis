<div align="center">

# Using Python Basics for Market Analysis
</div>

<p align="center">
  <img width="200" src="https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png" alt="Material Bread logo">
</p>

<div align="center">

___books.toscrape.com___

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

_This script is responsible for scraping the site www.books.toscrape.com_
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

# Demonstration

### Result in CSV

_Once the textual information of all the books in the category is recovered, everything is saved in a.csv file as below:_

| Book  Title | UPC Code | Product Type | Price(ExclTax) | Price(InclTax) | Taxes | Availability | Number of reviews | nb of stars | Image Url |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| It's  Only  the  Himalayas  | a22124811bfa8350 | Books | £45.17 | £45.17 | £0.00 | In  stock  (19  available)  | 17 | Two | http://books.toscrape.com/media/.../.../foo.jpg |
| Under  the  Tuscan  Sun | a94350ee74deaa07 | Books | £37.33 | £37.33 | £0.00 | In  stock  (7  available) | 5 | Four | http://books.toscrape.com/media/.../.../foo.jpg |

### Tree structure

_While running, the script creates a tree like this:_

![alt text](https://github.com/py-Thony/Use-Python-for-Scraping-Market-Analysis/blob/master/Livrables/tree.JPG?raw=true)