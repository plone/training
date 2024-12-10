---
myst:
  html_meta:
    "description": "Moving Content Automatically Using Content Rules"
    "property=og:description": "Moving Content Automatically Using Content Rules"
    "property=og:title": "Moving Content Automatically Using Content Rules"
    "keywords": "Plone, Moving, Content, Automatically, Content, Rules"
---

# Moving Content Automatically Using Content Rules

Here we show how to use a content rule to move content items automatically to a particular folder on your site. 

This helps keep the site content well organized.

In this example, we create a page called "Resources" that will act as a folder.

We create a content rule that automatically moves PDF files automatically to the "Resources" folder.

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

7. Click the {guilabel}`site logo` to return to the home page.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-06.jpeg
   :alt: The site logo
   :target: _static/moving-content-automatically-using-content-rules-06.jpeg
   ```
   +++
   _The site logo_
   ````

8. Click the {guilabel}`personal menu` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-07.jpeg
   :alt: The personal menu button
   :target: _static/moving-content-automatically-using-content-rules-07.jpeg
   ```
   +++
   _The personal menu button_
   ````

9. Click {guilabel}`Site Setup`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-08.jpeg
   :alt: Choose Site Setup
   :target: _static/moving-content-automatically-using-content-rules-08.jpeg
   ```
   +++
   _Choose Site Setup_
   ````

10. Click the {guilabel}`Content Rules` control panel icon.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-09.jpeg
   :alt: The Content Rules control panel
   :target: _static/moving-content-automatically-using-content-rules-09.jpeg
   ```
   +++
   _The Content Rules control panel_
   ````

11. We first have to create a content rule. Later on, we will assign it.

    Click {guilabel}`Object added to this container`.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-10.jpeg
   :alt: Choose "Object added to this container"
   :target: _static/moving-content-automatically-using-content-rules-10.jpeg
   ```
   +++
   _Choose "Object added to this container"_
   ````

12. Click {guilabel}`Add content rule`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-11.jpeg
   :alt: Click to add the content rule
   :target: _static/moving-content-automatically-using-content-rules-11.jpeg
   ```
   +++
   _Click to add the content rule_
   ````

13. Click the {guilabel}`Title` field.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-12.jpeg
   :alt: The content rule title field
   :target: _static/moving-content-automatically-using-content-rules-12.jpeg
   ```
   +++
   _The content rule title field_
   ````

14. Type "{kbd}`Add PDFs to the "Resources" content object`"


15. Click the {guilabel}`Description` field.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-13.jpeg
   :alt: The content rule description field
   :target: _static/moving-content-automatically-using-content-rules-13.jpeg
   ```
   +++
   _The content rule description field_
   ````

16. Type "{kbd}`To keep PDFs organized, we will put them in one central place`"


17. Click {guilabel}`Select...`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-14.jpeg
   :alt: Select the triggering event
   :target: _static/moving-content-automatically-using-content-rules-14.jpeg
   ```
   +++
   _Select the triggering event_
   ````

18. Click {guilabel}`Object added to this container`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-15.jpeg
   :alt: Choose "Object added to this container"
   :target: _static/moving-content-automatically-using-content-rules-15.jpeg
   ```
   +++
   _Choose "Object added to this container"_
   ````

19. Click {guilabel}`Enabled`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-16.jpeg
   :alt: Enable the content rule
   :target: _static/moving-content-automatically-using-content-rules-16.jpeg
   ```
   +++
   _Enable the content rule_
   ````

20. Click {guilabel}`Stop Executing rules`.

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

21. Click {guilabel}`Save`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-18.jpeg
   :alt: Save the content rule
   :target: _static/moving-content-automatically-using-content-rules-18.jpeg
   ```
   +++
   _Save the content rule_
   ````

22. Click {guilabel}`Configure`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-19.jpeg
   :alt: Configure the content rule actions
   :target: _static/moving-content-automatically-using-content-rules-19.jpeg
   ```
   +++
   _Configure the content rule actions_
   ````

23. Click the {guilabel}`Condition" drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-20.jpeg
   :alt: Click to set a condition
   :target: _static/moving-content-automatically-using-content-rules-20.jpeg
   ```
   +++
   _Click to set a condition_
   ````

24. Click {guilabel}`File Extension`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-21.jpeg
   :alt: Choose "File Extension"
   :target: _static/moving-content-automatically-using-content-rules-21.jpeg
   ```
   +++
   _Choose "File Extension"_
   ````

25. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-22.jpeg
   :alt: Add the condition
   :target: _static/moving-content-automatically-using-content-rules-22.jpeg
   ```
   +++
   _Add the condition_
   ````

26. Type {kbd}`pdf`


27. Click the {guilabel}`right arrow` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-23.jpeg
   :alt: The right arrow button
   :target: _static/moving-content-automatically-using-content-rules-23.jpeg
   ```
   +++
   _The right arrow button_
   ````

28. Click the {guilabel}`Action` drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-24.jpeg
   :alt: Click to set the action
   :target: _static/moving-content-automatically-using-content-rules-24.jpeg
   ```
   +++
   _Click to set the action_
   ````

29. Click {guilabel}`Move to folder`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-25.jpeg
   :alt: Choose "Move to folder"
   :target: _static/moving-content-automatically-using-content-rules-25.jpeg
   ```
   +++
   _Choose "Move to folder"_
   ````

30. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-26.jpeg
   :alt: Add the action
   :target: _static/moving-content-automatically-using-content-rules-26.jpeg
   ```
   +++
   _Add the action_
   ````

31. Click the {guilabel}`Navigate` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-27.jpeg
   :alt: The navigate button
   :target: _static/moving-content-automatically-using-content-rules-27.jpeg
   ```
   +++
   _The navigate button_
   ````

32. Click {guilabel}`Resources`.

    This is the content item we created earlier.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-28.jpeg
   :alt: Choose the target location
   :target: _static/moving-content-automatically-using-content-rules-28.jpeg
   ```
   +++
   _Choose the target location_
   ````

33. Click the {guilabel}`right arrow` button to apply the changes.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-29.jpeg
   :alt: The right arrow button
   :target: _static/moving-content-automatically-using-content-rules-29.jpeg
   ```
   +++
   _The right arrow button_
   ````

34. Click the {guilabel}`left arrow` button to return to the content rule view.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-30.jpeg
   :alt: Return to the Content Rules control panel
   :target: _static/moving-content-automatically-using-content-rules-30.jpeg
   ```
   +++
   _Return to the Content Rules control panel_
   ````

35. Click the {guilabel}`left arrow` button to return to Site Setup.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-31.jpeg
   :alt: Return to Site Setup
   :target: _static/moving-content-automatically-using-content-rules-31.jpeg
   ```
   +++
   _Return to Site Setup_
   ````

36. Click the {guilabel}`site logo` to return to the home page.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-32.jpeg
   :alt: Return to the home page
   :target: _static/moving-content-automatically-using-content-rules-32.jpeg
   ```
   +++
   _Return to the home page_
   ````

37. We want to apply the new content rule here, the root of the site.

    Click the {guilabel}`More` button.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-33.jpeg
   :alt: The More button
   :target: _static/moving-content-automatically-using-content-rules-33.jpeg
   ```
   +++
   _The More button_
   ````

38. Click {guilabel}`Rules`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-34.jpeg
   :alt: Choose Rules
   :target: _static/moving-content-automatically-using-content-rules-34.jpeg
   ```
   +++
   _Choose Rules_
   ````

39. Click the {guilabel}`Select rule` drop down list.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-35.jpeg
   :alt: Click to select a content rule
   :target: _static/moving-content-automatically-using-content-rules-35.jpeg
   ```
   +++
   _Click to select a content rule_
   ````

40. Click "{guilabel}`Add PDFs to the "Resources" content object`"

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-36.jpeg
   :alt: Choose the content rule
   :target: _static/moving-content-automatically-using-content-rules-36.jpeg
   ```
   +++
   _Choose the content rule_
   ````

41. Click {guilabel}`Add`

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-37.jpeg
   :alt: Add the content rule here
   :target: _static/moving-content-automatically-using-content-rules-37.jpeg
   ```
   +++
   _Add the content rule here_
   ````

42. Click the checkbox next to the rule.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-38.jpeg
   :alt: Check the box to select the rule
   :target: _static/moving-content-automatically-using-content-rules-38.jpeg
   ```
   +++
   _Check the box to select the rule_
   ````

43. Click {guilabel}`Enable`.

    The content rule is now enabled for the entire site.

   ````{card}
   ```{image} _static/moving-content-automatically-using-content-rules-39.jpeg
   :alt: Enable the selected rule
   :target: _static/moving-content-automatically-using-content-rules-39.jpeg
   ```
   +++
   _Enable the selected rule_
   ````
