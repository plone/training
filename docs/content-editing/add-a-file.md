---
myst:
  html_meta:
    "description": "Add a File"
    "property=og:description": "Add a File"
    "property=og:title": "Add a File"
    "keywords": "Plone, Add, File"
---

# Add a File

You can add any type of file to your Plone site. Files can be any "binary file", including PDFs, text files, videos, and Word documents. 

You could follow this method to add an image, but rather than add an image as a file, you should add an image as an image! (see {ref}`Add an Image <add-an-image-label>`).

## Add a File

We add a file and look at other metadata that can be set on it and all content items in general.

1. Click the {guilabel}`add item` button.

   ````{card}
   ```{image} _static/add-a-file-01.jpeg
   :alt: The add item button
   :target: _static/add-a-file-01.jpeg
   ```
   +++
   _The add item button_
   ````

2. Click {guilabel}`File`

   ````{card}
   ```{image} _static/add-a-file-02.jpeg
   :alt: Add a File
   :target: _static/add-a-file-02.jpeg
   ```
   +++
   _Add a File_
   ````

3. Click the {guilabel}`Title` field and type a title.

   If you don't provide a title, Plone will use the name of the file you upload.

   The title will be indexed by Plone's built-in search and will appear in listings, such as in search results.

   ````{card}
   ```{image} _static/add-a-file-03.jpeg
   :alt: The title field
   :target: _static/add-a-file-03.jpeg
   ```
   +++
   _The title field_
   ````

4. Use the {guilabel}`Description` field to describe the file.

   This description, or summary, will be indexed by Plone's search, and appears in listings such as in search results.

   ````{card}
   ```{image} _static/add-a-file-04.jpeg
   :alt: The description field
   :target: _static/add-a-file-04.jpeg
   ```
   +++
   _The description field_
   ````

5. Click {guilabel}`Choose a file` and use the dialog to select the file you want to upload, then press the dialog's {guilabel}`OK` button.

   Alternatively, you can drag the file to the {guilabel}`Drop file here` target area.

   ````{card}
   ```{image} _static/add-a-file-05.jpeg
   :alt: Choose a file
   :target: _static/add-a-file-05.jpeg
   ```
   +++
   _Choose a file_
   ````

## Set Categorization Metadata (Tags, Language, Related Items)

1. Let's look at the other metadata you can set.

    Click {guilabel}`Categorization`.

   ````{card}
   ```{image} _static/add-a-file-06.jpeg
   :alt: Categorization settings
   :target: _static/add-a-file-06.jpeg
   ```
   +++
   _Categorization settings_
   ````

2. This lets you assign tags, or keywords, to the current content item. 

    Tags are another way to describe the current content item.

    Tags can be assigned to multiple content items, and are indexed by Plone's built-in search.

   ````{card}
   ```{image} _static/add-a-file-07.jpeg
   :alt: Set tags
   :target: _static/add-a-file-07.jpeg
   ```
   +++
   _Set tags_
   ````

3. You can select existing tags.

    To create new tags, you type each one followed by {kbd}`enter`.

    For example, type "zope {kbd}`Enter` zope3 {kbd}`Enter` unit tests {kbd}`Enter` introduction {kbd}`Enter`"

4. Click on the {guilabel}`Language` drop down list to specify the language of the content item.

   ````{card}
   ```{image} _static/add-a-file-08.jpeg
   :alt: Set the language
   :target: _static/add-a-file-08.jpeg
   ```
   +++
   _Set the language_
   ````

5. Click on the {guilabel}`Related Items` field to select other content items on the current site that are related to this one. 

    This lets you guide users to other content that may also be of interest to them.

   ````{card}
   ```{image} _static/add-a-file-09.jpeg
   :alt: Set related items
   :target: _static/add-a-file-09.jpeg
   ```
   +++
   _Set related items_
   ````

6. You can select one or more related items by navigating and by searching the site.

    In this example, we select as a related item the page "Content Types" by clicking on its icon.

   ````{card}
   ```{image} _static/add-a-file-10.jpeg
   :alt: Choose the related item
   :target: _static/add-a-file-10.jpeg
   ```
   +++
   _Choose the related item_
   ````

7. Click the {guilabel}`X` button to exit from the related items selection widget.

   ````{card}
   ```{image} _static/add-a-file-11.jpeg
   :alt: Close the related item chooser panel
   :target: _static/add-a-file-11.jpeg
   ```
   +++
   _Close the related item chooser panel_
   ````
## Set Dates Metadata (Publication and Expiration Dates)

1. Click {guilabel}`Dates`

   ````{card}
   ```{image} _static/add-a-file-12.jpeg
   :alt: Date settings
   :target: _static/add-a-file-12.jpeg
   ```
   +++
   _Date settings_
   ````

2. The Expiration Date lets you set when this item should no longer be shown in the site's navigation, e.g., in site headings.

   ````{card}
   ```{image} _static/add-a-file-13.jpeg
   :alt: The expiration date
   :target: _static/add-a-file-13.jpeg
   ```
   +++
   _The expiration date_
   ````

3. Set the expiration date by clicking on the {guilabel}`Date` field. You can set the expiration time by clicking on the {guilabel}`Time` field.

   ````{card}
   ```{image} _static/add-a-file-14.jpeg
   :alt: The calendar widget
   :target: _static/add-a-file-14.jpeg
   ```
   +++
   _The calendar widget_
   ````

4. The "Publishing Date" will be set automatically when you publish the item, so there is usually no need to set it.

    You can set a publishing date in the future if you want to publish the item now but not have it highlighted in the site navigation until that future date and time.

   ````{card}
   ```{image} _static/add-a-file-14.jpeg
   :alt: The publication date
   :target: _static/add-a-file-14.jpeg
   ```
   +++
   _The publication date_
   ````
## Set Ownership Metadata (Creators, Contributors, Rights)

1. Click {guilabel}`Ownership`

   ````{card}
   ```{image} _static/add-a-file-15.jpeg
   :alt: Ownership settings
   :target: _static/add-a-file-15.jpeg
   ```
   +++
   _Ownership settings_
   ````

2. The Ownership fields let you set who created and contributed to the item. You can also set a copyright statement.

    Click {guilabel}`Settings`.

   ````{card}
   ```{image} _static/add-a-file-16.jpeg
   :alt: Other settings
   :target: _static/add-a-file-16.jpeg
   ```
   +++
   _Other settings_
   ````
## Set Other Metadata (Short Name, Exclude from Navigation)

1. The "short name" for an item is what appears as part of the web address of the item. 

    By default, Plone takes the title of the item, lower cases it, and replaces spaces and other punctuation with hyphens ("-").

    The "Short name" field lets you override what Plone will set by default.

    Click the {guilabel}`Save` button.

   ````{card}
   ```{image} _static/add-a-file-17.jpeg
   :alt: The Save button
   :target: _static/add-a-file-17.jpeg
   ```
   +++
   _The Save button_
   ````

## Review the Added File

1. You see the saved file's title, description (summary), a link to download the file, the file type and size.

   ````{card}
   ```{image} _static/add-a-file-18.jpeg
   :alt: The saved file
   :target: _static/add-a-file-18.jpeg
   ```
   +++
   _The saved file_
   ````

2. Click {guilabel}`demo1.pdf` to download the file.

   ````{card}
   ```{image} _static/add-a-file-19.jpeg
   :alt: The file download link
   :target: _static/add-a-file-19.jpeg
   ```
   +++
   _The file download link_
   ````

3. You also see the tags or keywords you assigned to the item.

   ````{card}
   ```{image} _static/add-a-file-20.jpeg
   :alt: The clickable tags
   :target: _static/add-a-file-20.jpeg
   ```
   +++
   _The clickable tags_
   ````

4. Click a tag to see other content items that have been assigned that tag.

   ````{card}
   ```{image} _static/add-a-file-21.jpeg
   :alt: Click on a tag
   :target: _static/add-a-file-21.jpeg
   ```
   +++
   _Click on a tag_
   ````

5. You see a list of all content items on the site that have been assigned that tag.

   ````{card}
   ```{image} _static/add-a-file-22.jpeg
   :alt: Tag search results
   :target: _static/add-a-file-22.jpeg
   ```
   +++
   _Tag search results_
   ````
