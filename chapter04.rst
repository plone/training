Configuring and Customising Plone through the web
=================================================


The Control Panel
-----------------

The most important parts of Plone can be configured in the control-panel.

* Click on your username
* Click "Site Setup"

We'll explain every page and mention some of the stuff you can do here.

1. Add-ons (later...)
2. Calendar
3. Configuration Registry
4. Content Rules (we know this already)
5. Discussion
6. Editing
7. Errors
8. HTML Filtering
9. Image Handling
10. Language
11. Mail
12. Maintenance
13. Markup
14. Navigation
15. Search
16. Security
17. Site
18. Syndication
19. Themes
20. TinyMCE Visual Editor
21. Types
22. Users and Groups
24. Zope Management Interface (here be dragons)

Below the links you find information on your Plone-, Zope and Python-Versions



Portlets
---------

explain portlets:

* ``@@manage-portlets``
* UI fit for smart content-editors
* explain various types
* inheritance
* managing them
* ordering/weighting
* will be replaced by tiles?

Example:

* Add a static portlet "Sponsors" on the right side.
* Remove the news-portlet and add a new one on the left side.


Viewlets
--------

* ``@@manage-viewlets``
* no UI - not for content-editors
* not locally addable, no configurable inheritance
* will be replaced by tiles?
* the code is much simpler (we'll create one tomorrow)
* viewlet-manager
* ttw-reordering only within the same viewlet-manager
* the programer descides when it's where and what it shows

Portlets save Data, Viewlets usually don't. Viewlets are often used for UI-Elements.

Example:

* Hide collophon


ZMI
---

Go into the ZMI (explain ``/manage``)

Since Zope is the foundation of Plone. Here you can access the inner working of Zope and PLone alike. Here you can easily break your site so you should know what you are doing.

Here we only cover three parts of customisation in the ZMI now. Later on when we added our own code we'll come back to the ZMI and will look for it.

At some point you'll have to learn what all that stuff is about. But not today.


Actions (portal_actions)
------------------------

Actions are mostly links but really flexible links :-)

Examples:

* Links in the Footer (site_actions)
* Actions-Dropdown (folder_buttons)

Links with properties like:

* description
* url
* i18n-domain
* condition
* permissions

Configurable ttw and through code.

These actions are usually iterated over in viewlets and displayed.

Example:

* Global navigation (portal_tab)
* go to ``portal_actions`` > ``portal_tabs``

Where is my navigation?

The navigation shows content-objects, which are in Plone's root. Plus all actions in portal_tabs

Explain & edit index_html

Add a link to the imprint to the bottom:

* go to ``site_actions`` (we know that because we checked in ``@@manage-viewlets``)
* add a CMF Actions ``imprint``
* set its URL to ``string:${globals_view/navigationRootUrl}/imprint``
* Leave condition empty
* Set permission to ``View``

If time explain:

* user > undo (cool!)
* user > login/logout


Skins (portal_skins)
--------------------

* Go to ZMI
* go to portal_skins
* go to plone_styles
* go to ``ploneCustom.css``
* click ``customize``

Enter the following css:

.. code-block:: css

    #visual-portal-wrapper {
        margin: 0 auto;
        position: relative;
        width: 980px;
    }

Check results in the browser. How did that happen?


CSS-Registry (portal_css)
-------------------------

* go to ZMI > ``portal_css``
* at the bottom there is ``ploneCustom.css``

The UI leaves a lot to be desired.

In a professional context this is no-go (since ther is no version-control). But everybody uses it to make quick fixes to sites that are already online.

Later we'll revisit the same css-code.


Summary
-------

You can configure and customize a lot in Plone through the web. The amount of stuff is overwhelming but you'll get the hang of it through a lot of practice.
