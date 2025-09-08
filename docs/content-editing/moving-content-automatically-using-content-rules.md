---
myst:
  html_meta:
    "description": "Moving Content Automatically Using Content Rules"
    "property=og:description": "Moving Content Automatically Using Content Rules"
    "property=og:title": "Moving Content Automatically Using Content Rules"
    "keywords": "Plone, Moving, Content, Automatically, Content, Rules"
---

# Move Content Automatically Using Content Rules

Here we show how to use a content rule to move content items automatically to a particular folder on your site. 

This helps keep the site content well organized.

In this example, we create a page called "Resources" that will act as a folder.

Then we create a content rule that automatically moves PDF files to the "Resources" folder.

## Create the Resources "Folder"

1. Click the {guilabel}`add item` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-01.jpeg
   :alt: The add item button
   :target: _static/moving-content-automatically-using-content-rules-01.jpeg
   ```
   +++
   _The add item button_
   ````

2. Click {guilabel}`Page`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-02.jpeg
   :alt: Add a Page
   :target: _static/moving-content-automatically-using-content-rules-02.jpeg
   ```
   +++
   _Add a Page_
   ````

3. Click {guilabel}`Type the title...`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-03.jpeg
   :alt: The title field
   :target: _static/moving-content-automatically-using-content-rules-03.jpeg
   ```
   +++
   The title field_
   ````

4. Type {guilabel}`Resources`


5. If you'd like to hide "Resources" in the header navigation, click {guilabel}`Exclude from navigation`.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-04.jpeg
   :alt: Check the box to exclude the item from navigation
   :target: _static/moving-content-automatically-using-content-rules-04.jpeg
   ```
   +++
   _Check the box to exclude the item from navigation_
   ````

6. Click the {guilabel}`Save` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-05.jpeg
   :alt: The Save button
   :target: _static/moving-content-automatically-using-content-rules-05.jpeg
   ```
   +++
   _The Save button_
   ````
## Create the Content Rule

1. Click the {guilabel}`personal menu` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-07.jpeg
   :alt: The personal menu button
   :target: _static/moving-content-automatically-using-content-rules-07.jpeg
   ```
   +++
   _The personal menu button_
   ````

2. Click {guilabel}`Site Setup`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-08.jpeg
   :alt: Choose Site Setup
   :target: _static/moving-content-automatically-using-content-rules-08.jpeg
   ```
   +++
   _Choose Site Setup_
   ````

3. Click the {guilabel}`Content Rules` control panel icon.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-09.jpeg
   :alt: The Content Rules control panel
   :target: _static/moving-content-automatically-using-content-rules-09.jpeg
   ```
   +++
   _The Content Rules control panel_
   ````

4. We first have to create a content rule. Later on, we will assign it.

    Click {guilabel}`Object added to this container`.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-10.jpeg
   :alt: Choose "Object added to this container"
   :target: _static/moving-content-automatically-using-content-rules-10.jpeg
   ```
   +++
   _Choose "Object added to this container"_
   ````

5. Click {guilabel}`Add content rule`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-11.jpeg
   :alt: Click to add the content rule
   :target: _static/moving-content-automatically-using-content-rules-11.jpeg
   ```
   +++
   _Click to add the content rule_
   ````

6. Click the {guilabel}`Title` field.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-12.jpeg
   :alt: The content rule title field
   :target: _static/moving-content-automatically-using-content-rules-12.jpeg
   ```
   +++
   _The content rule title field_
   ````

7. Type "{kbd}`Add PDFs to the "Resources" content object`"


8. Click the {guilabel}`Description` field.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-13.jpeg
   :alt: The content rule description field
   :target: _static/moving-content-automatically-using-content-rules-13.jpeg
   ```
   +++
   _The content rule description field_
   ````

9. Type "{kbd}`To keep PDFs organized, we will put them in one central place`"


10. Click {guilabel}`Select...`

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-14.jpeg
      :alt: Select the triggering event
      :target: _static/moving-content-automatically-using-content-rules-14.jpeg
      ```
      +++
      _Select the triggering event_
      ````

11. Click {guilabel}`Object added to this container`

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-15.jpeg
      :alt: Choose "Object added to this container"
      :target: _static/moving-content-automatically-using-content-rules-15.jpeg
      ```
      +++
      _Choose "Object added to this container"_
      ````

12. Click {guilabel}`Enabled`

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-16.jpeg
      :alt: Enable the content rule
      :target: _static/moving-content-automatically-using-content-rules-16.jpeg
      ```
      +++
      _Enable the content rule_
      ````

13. Click {guilabel}`Stop Executing rules`.

    In many cases you want Content Rules to be stopping as soon as possible, especially when moving content items. 
    You may have multiple content rules if they are unrelated in their effect, i.e. sending out an email when a PDF is added.

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-17.jpeg
      :alt: Check "Stop Executing Rules"
      :target: _static/moving-content-automatically-using-content-rules-17.jpeg
      ```
      +++
      _Check "Stop Executing Rules"_
      ````

14. Click {guilabel}`Save`

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-18.jpeg
      :alt: Save the content rule
      :target: _static/moving-content-automatically-using-content-rules-18.jpeg
      ```
      +++
      _Save the content rule_
      ````
## Configure the Content Rule

1. Click {guilabel}`Configure`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-19.jpeg
   :alt: Configure the content rule actions
   :target: _static/moving-content-automatically-using-content-rules-19.jpeg
   ```
   +++
   _Configure the content rule actions_
   ````

2. Click the {guilabel}`Condition" drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-20.jpeg
   :alt: Click to set a condition
   :target: _static/moving-content-automatically-using-content-rules-20.jpeg
   ```
   +++
   _Click to set a condition_
   ````

3. Click {guilabel}`File Extension`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-21.jpeg
   :alt: Choose "File Extension"
   :target: _static/moving-content-automatically-using-content-rules-21.jpeg
   ```
   +++
   _Choose "File Extension"_
   ````

4. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-22.jpeg
   :alt: Add the condition
   :target: _static/moving-content-automatically-using-content-rules-22.jpeg
   ```
   +++
   _Add the condition_
   ````

5. Type {kbd}`pdf`


6. Click the {guilabel}`right arrow` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-23.jpeg
   :alt: The right arrow button
   :target: _static/moving-content-automatically-using-content-rules-23.jpeg
   ```
   +++
   _The right arrow button_
   ````

7. Click the {guilabel}`Action` drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-24.jpeg
   :alt: Click to set the action
   :target: _static/moving-content-automatically-using-content-rules-24.jpeg
   ```
   +++
   _Click to set the action_
   ````

8. Click {guilabel}`Move to folder`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-25.jpeg
   :alt: Choose "Move to folder"
   :target: _static/moving-content-automatically-using-content-rules-25.jpeg
   ```
   +++
   _Choose "Move to folder"_
   ````

9. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-26.jpeg
   :alt: Add the action
   :target: _static/moving-content-automatically-using-content-rules-26.jpeg
   ```
   +++
   _Add the action_
   ````

10. Click the {guilabel}`Navigate` button.

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-27.jpeg
      :alt: The navigate button
      :target: _static/moving-content-automatically-using-content-rules-27.jpeg
      ```
      +++
      _The navigate button_
      ````

11. Click {guilabel}`Resources`.

    This is the content item we created earlier.

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-28.jpeg
      :alt: Choose the target location
      :target: _static/moving-content-automatically-using-content-rules-28.jpeg
      ```
      +++
      _Choose the target location_
      ````

12. Click the {guilabel}`right arrow` button to apply the changes.

      ````{card}
      ```{image} _static/moving-content-automatically-using-content-rules-29.jpeg
      :alt: The right arrow button
      :target: _static/moving-content-automatically-using-content-rules-29.jpeg
      ```
      +++
      _The right arrow button_
      ````

## Assign the Content Rule

1. Click the {guilabel}`site logo` to return to the home page.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-32.jpeg
   :alt: Return to the home page
   :target: _static/moving-content-automatically-using-content-rules-32.jpeg
   ```
   +++
   _Return to the home page_
   ````

2. We want to apply the new content rule here, the root of the site.

    Click the {guilabel}`More` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-33.jpeg
   :alt: The More button
   :target: _static/moving-content-automatically-using-content-rules-33.jpeg
   ```
   +++
   _The More button_
   ````

3. Click {guilabel}`Rules`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-34.jpeg
   :alt: Choose Rules
   :target: _static/moving-content-automatically-using-content-rules-34.jpeg
   ```
   +++
   _Choose Rules_
   ````

4. Click the {guilabel}`Select rule` drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-35.jpeg
   :alt: Click to select a content rule
   :target: _static/moving-content-automatically-using-content-rules-35.jpeg
   ```
   +++
   _Click to select a content rule_
   ````

5. Click "{guilabel}`Add PDFs to the "Resources" content object`"

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-36.jpeg
   :alt: Choose the content rule
   :target: _static/moving-content-automatically-using-content-rules-36.jpeg
   ```
   +++
   _Choose the content rule_
   ````

6. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-37.jpeg
   :alt: Add the content rule here
   :target: _static/moving-content-automatically-using-content-rules-37.jpeg
   ```
   +++
   _Add the content rule here_
   ````

7. Click the checkbox next to the rule.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-38.jpeg
   :alt: Check the box to select the rule
   :target: _static/moving-content-automatically-using-content-rules-38.jpeg
   ```
   +++
   _Check the box to select the rule_
   ````

8. Click {guilabel}`Enable`.

    The content rule is now enabled for the entire site.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-39.jpeg
   :alt: Enable the selected rule
   :target: _static/moving-content-automatically-using-content-rules-39.jpeg
   ```
   +++
   _Enable the selected rule_
   ````
