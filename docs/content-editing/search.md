---
myst:
  html_meta:
    "description": "Search"
    "property=og:description": "Search"
    "property=og:title": "Search"
    "keywords": "Plone, Search"
---

# Search

Plone has built-in search that returns results matching text found in titles, summaries, page bodies, and keywords.

Here we demonstrate how Plone's built in search works, by searching (unsuccessfully) for a word, then creating a page that contains that word, and then searching (successfully) for that word.

1. Click the {guilabel}`Search` button.

   ````{card}
   ```{image} _static/search-01.jpeg
   :alt: The Search button
   :target: _static/search-01.jpeg
   ```
   +++
   _The Search button_
   ````

2. Click the {guilabel}`Search Site` field, where we will enter a search term. 

    Search terms can consist of one or more words.

   ````{card}
   ```{image} _static/search-02.jpeg
   :alt: The Search Site text field
   :target: _static/search-02.jpeg
   ```
   +++
   _The Search Site text field_
   ````

3. Type "Oshkosh {kbd}`Enter`"


4. As expected, no results were found matching the search term.

   ````{card}
   ```{image} _static/search-03.jpeg
   :alt: The search results
   :target: _static/search-03.jpeg
   ```
   +++
   _The search results_
   ````

5. Although you don't need to be logged in to use Plone's search, you must be logged in to follow the rest of this example. 

    Now let's create a page that will contain our search term.


6. Click the {guilabel}`add item` button.

   ````{card}
   ```{image} _static/search-04.jpeg
   :alt: The add item button
   :target: _static/search-04.jpeg
   ```
   +++
   _The add item button_
   ````

7. Click {guilabel}`Page`

   ````{card}
   ```{image} _static/search-05.jpeg
   :alt: Add a Page
   :target: _static/search-05.jpeg
   ```
   +++
   _Add a Page_
   ````

8. Type "Oshkosh" in the title block, and press {kbd}`Enter`

9. The page should look like this.

   ````{card}
   ```{image} _static/search-06.jpeg
   :alt: After setting the title
   :target: _static/search-06.jpeg
   ```
   +++
   _After setting the title_
   ````

10. Add text in the next block, below the title.


11. Click {guilabel}`Save`.

   ````{card}
   ```{image} _static/search-07.jpeg
   :alt: The Save button
   :target: _static/search-07.jpeg
   ```
   +++
   _The Save button_
   ````

12. Click {guilabel}`Search`.

   ````{card}
   ```{image} _static/search-08.jpeg
   :alt: The Search button
   :target: _static/search-08.jpeg
   ```
   +++
   _The Search button_
   ````

13. Click the {guilabel}`Search Site` field and type {kbd}`Oshkosh` (case does not matter), then press {kbd}`Enter`.

   ````{card}
   ```{image} _static/search-09.jpeg
   :alt: The Search Site text field
   :target: _static/search-09.jpeg
   ```
   +++
   _The Search Site text field_
   ````

14. You will see one page listed in the search results. Clicking on a search result takes you to the item.

   ````{card}
   ```{image} _static/search-10.jpeg
   :alt: The search results listing
   :target: _static/search-10.jpeg
   ```
   +++
   _The search results listing_
   ````
