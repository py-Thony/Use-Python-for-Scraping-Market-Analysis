<div align="center">

# Using Python Basics for Market Analysis
</div>

<p align="center">
  <img width="200" src="https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png" alt="Material Bread logo">
</p>

<div align="center">

___A program (a scraper) developed in Python, capable of extracting price information from other online bookstores.___
</div>

_Horizontal line :_
====

## Creation of the virtual environment
Official python documentation:
    - [Python3 venv docs](https://docs.python.org/fr/3/library/venv.html "Documentation for creating and using a virtual environment to work free from version conflicts.")

VScode specific documentation:
    - [VScode venv docs](https://code.visualstudio.com/docs/python/environments "Documentation for creating and using a virtual environment to work free from version conflicts.")

## requirements.txt
_A requirements.txt file allows you to find out the list of libraries necessary for the proper functioning of the program._

__To start the installation automatically:__
>Version Of libraries (Python3)
>>The versions are indicated from the day of creation but you can update them
```bash
pip install -r requirements.txt
```


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




    Markup :  #### Heading 4 ####


Common text

    Markup :  Common text

_Emphasized text_

    Markup :  _Emphasized text_ or *Emphasized text*

~~Strikethrough text~~

    Markup :  ~~Strikethrough text~~

__Strong text__

    Markup :  __Strong text__ or **Strong text**

___Strong emphasized text___

    Markup :  ___Strong emphasized text___ or ***Strong emphasized text***

[Named Link](http://www.google.fr/ "Named link title") and http://www.google.fr/ or <http://example.com/>

    Markup :  [Named Link](http://www.google.fr/ "Named link title") and http://www.google.fr/ or <http://example.com/>

[heading-1](#heading-1 "Goto heading-1")
    
    Markup: [heading-1](#heading-1 "Goto heading-1")

Table, like this one :

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

```
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

Adding a pipe `|` in a cell :

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | \|

```
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  |  \| 
```

Left, right and center aligned table

Left aligned Header | Right aligned Header | Center aligned Header
| :--- | ---: | :---:
Content Cell  | Content Cell | Content Cell
Content Cell  | Content Cell | Content Cell

```
Left aligned Header | Right aligned Header | Center aligned Header
| :--- | ---: | :---:
Content Cell  | Content Cell | Content Cell
Content Cell  | Content Cell | Content Cell
```

`code()`

    Markup :  `code()`

```javascript
    var specificLanguage_code = 
    {
        "data": {
            "lookedUpPlatform": 1,
            "query": "Kasabian+Test+Transmission",
            "lookedUpItem": {
                "name": "Test Transmission",
                "artist": "Kasabian",
                "album": "Kasabian",
                "picture": null,
                "link": "http://open.spotify.com/track/5jhJur5n4fasblLSCOcrTp"
            }
        }
    }
```

    Markup : ```javascript
             ```

* Bullet list
    * Nested bullet
        * Sub-nested bullet etc
* Bullet list item 2

~~~
 Markup : * Bullet list
              * Nested bullet
                  * Sub-nested bullet etc
          * Bullet list item 2

-OR-

 Markup : - Bullet list
              - Nested bullet
                  - Sub-nested bullet etc
          - Bullet list item 2 
~~~

1. A numbered list
    1. A nested numbered list
    2. Which is numbered
2. Which is numbered

~~~
 Markup : 1. A numbered list
              1. A nested numbered list
              2. Which is numbered
          2. Which is numbered
~~~

- [ ] An uncompleted task
- [x] A completed task

~~~
 Markup : - [ ] An uncompleted task
          - [x] A completed task
~~~

- [ ] An uncompleted task
    - [ ] A subtask

~~~
 Markup : - [ ] An uncompleted task
              - [ ] A subtask
~~~

> Blockquote
>> Nested blockquote

    Markup :  > Blockquote
              >> Nested Blockquote

_Horizontal line :_
- - - -

    Markup :  - - - -

_Image with alt :_

![picture alt](http://via.placeholder.com/200x150 "Title is optional")

    Markup : ![picture alt](http://via.placeholder.com/200x150 "Title is optional")

Foldable text:

<details>
  <summary>Title 1</summary>
  <p>Content 1 Content 1 Content 1 Content 1 Content 1</p>
</details>
<details>
  <summary>Title 2</summary>
  <p>Content 2 Content 2 Content 2 Content 2 Content 2</p>
</details>

    Markup : <details>
               <summary>Title 1</summary>
               <p>Content 1 Content 1 Content 1 Content 1 Content 1</p>
             </details>

```html
<h3>HTML</h3>
<p> Some HTML code here </p>
```

Link to a specific part of the page:

[Go To TOP](#TOP)
   
    Markup : [text goes here](#section_name)
              section_title<a name="section_name"></a>    

Hotkey:

<kbd>⌘F</kbd>

<kbd>⇧⌘F</kbd>

    Markup : <kbd>⌘F</kbd>

Hotkey list:

| Key | Symbol |
| --- | --- |
| Option | ⌥ |
| Control | ⌃ |
| Command | ⌘ |
| Shift | ⇧ |
| Caps Lock | ⇪ |
| Tab | ⇥ |
| Esc | ⎋ |
| Power | ⌽ |
| Return | ↩ |
| Delete | ⌫ |
| Up | ↑ |
| Down | ↓ |
| Left | ← |
| Right | → |

Emoji:

:exclamation: Use emoji icons to enhance text. :+1:  Look up emoji codes at [emoji-cheat-sheet.com](http://emoji-cheat-sheet.com/)

    Markup : Code appears between colons :EMOJICODE:
