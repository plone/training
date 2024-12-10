---
myst:
  html_meta:
    "description": "Add a Link"
    "property=og:description": "Add a Link"
    "property=og:title": "Add a Link"
    "keywords": "Plone, Add, Link"
---

# Add a Link

You use a Link when you would like a page on your site to redirect a visitor to a web address external to your site.

A Link acts as bookmark on your site for something that is elsewhere on the Internet.

Here we show how to create a Link object that sends a visitor to an arbitrary web address.

1. In this example, we create a Link that will take someone to the video at the web address <https://www.youtube.com/watch?v=Yk7tx2zgL98> 

    Click the {guilabel}`add new` button.

   ````{card}
   ```{image} _static/add-a-link-01.jpeg
   :alt: The add item button
   :target: _static/add-a-link-01.jpeg
   ```
   +++
   _The add item button_
   ````

2. Click {guilabel}`Link`

   ````{card}
   ```{image} _static/add-a-link-02.jpeg
   :alt: Add a Link
   :target: _static/add-a-link-02.jpeg
   ```
   +++
   _Add a Link_
   ````

3. Click the {guilabel}`Title` field and enter a title, e.g., "What Is World Plone Day?"

   ````{card}
   ```{image} _static/add-a-link-03.jpeg
   :alt: The title field
   :target: _static/add-a-link-03.jpeg
   ```
   +++
   _The title field_
   ````

4. Click the {guilabel}`Summary` field and enter a summary, e.g., "A video conversation explaining what is World Plone Day"

   ````{card}
   ```{image} _static/add-a-link-04.jpeg
   :alt: The summary field
   :target: _static/add-a-link-04.jpeg
   ```
   +++
   _The summary field_
   ````

5. Click the {guilabel}`URL` field and enter the web address of the video, e.g., <https://www.youtube.com/watch?v=Yk7tx2zgL98>

   ````{card}
   ```{image} _static/add-a-link-05.jpeg
   :alt: The web address or URL field
   :target: _static/add-a-link-05.jpeg
   ```
   +++
   _The web address or URL field_
   ````

6. Click the {guilabel}`Save` button.

   ````{card}
   ```{image} _static/add-a-link-06.jpeg
   :alt: The Save button
   :target: _static/add-a-link-06.jpeg
   ```
   +++
   _The Save button_
   ````

7. The details of the Link you created are visible to you, the creator, and to a site manager, but a regular user or the public will be redirected immediately to the link address.

    We will show this by logging out of the site.

   ````{card}
   ```{image} _static/add-a-link-07.jpeg
   :alt: The saved Link
   :target: _static/add-a-link-07.jpeg
   ```
   +++
   _The saved Link_
   ````

8. Click the {guilabel}`personal menu` button.

   ````{card}
   ```{image} _static/add-a-link-08.jpeg
   :alt: The personal menu button
   :target: _static/add-a-link-08.jpeg
   ```
   +++
   _The personal menu button_
   ````

9. Click the {guilabel}`Logout` button.

   ````{card}
   ```{image} _static/add-a-link-09.jpeg
   :alt: The Logout button
   :target: _static/add-a-link-09.jpeg
   ```
   +++
   _The Logout button_
   ````

10. As soon as you are logged out of Plone, your browser reloads the page. 

    Because you are logged out, when your browser attempts to render the Link item and Plone recognizes that you do not have edit permissions on the Link, it redirects you to the web address of the video.
    
    Anyone visiting the Link will get redirected as well.

    ````{card}
    ```{image} _static/add-a-link-10.jpeg
    :alt: The linked-to video
    :target: _static/add-a-link-10.jpeg
    ```
    +++
    _The linked-to video_
    ````

