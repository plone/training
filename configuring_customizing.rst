Configuring and Customizing Plone through the web
=================================================

 .. sectionauthor:: Philip Bauer <bauer@starzel.de>

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
23. Zope Management Interface (here be dragons)

Below the links you find information on your Plone-, Zope and Python-Versions



Portlets
---------

* ``@@manage-portlets``
* UI fit for smart content-editors
* various types
* portlet-configuration is inherited
* managing
* ordering/weighting
* will maybe be replaced by tiles

Example:

* go to http://localhost:8080/Plone/@@manage-portlets
* Add a static portlet "Sponsors" on the right side.
* Remove the news-portlet and add a new one on the left side.
* Go to the training-folder: http://localhost:8080/Plone/training and click ``Manage portlets``
* Add a static portlet. "Featured training: Become a Plone-Rockstar at Mastering Plone!"


Viewlets
--------

* ``@@manage-viewlets``
* viewlet have no UI
* not aimed at content-editors
* not locally addable, no configurable inheritance.
* usually global (depends on code)
* will be replaced by tiles?
* the code is much simpler (we'll create one tomorrow)
* live in viewlet-managers, can be nested (by adding a viewlet that contains a viewlet-manager)
* ttw-reordering only within the same viewlet-manager
* the code descides when it's where and what it shows

Portlets save Data, Viewlets usually don't. Viewlets are often used for UI-Elements.

Example:

* Go to http://localhost:8080/Plone/@@manage-viewlets
* Hide collophon


ZMI
---

Go to http://localhost:8080/Plone/manage

Zope is the foundation of Plone. Here you can access the inner working of Zope and Plone alike.

.. note::

  Here you can easily break your site so you should know what you are doing.

.. only:: manual

    We only cover three parts of customisation in the ZMI now. Later on when we added our own code we'll come back to the ZMI and will look for it.

    At some point you'll have to learn what all that stuff is about. But not today.


Actions (portal_actions)
************************

* Actions are mostly links. But **really flexible** links.
* Actions are configurable ttw and through code.
* These actions are usually iterated over in viewlets and displayed.

Examples:

* Links in the Footer (site_actions)
* Actions-Dropdown (folder_buttons)

Actions have properties like:

* description
* url
* i18n-domain
* condition
* permissions



site_actions
++++++++++++

These are the links at the bottom of the page:

* Site Map
* Accessibility
* Contact
* Site Setup

We want a new link to legal information, called "Imprint".

* Go to ``site_actions`` (we know that because we checked in ``@@manage-viewlets``)
* Add a CMF Actions ``imprint``
* Set URL to ``string:${portal_url}/imprint``
* Leave *condition* empty
* Set permission to ``View``
* Save

.. only:: manual

  explain

* Check if the link is on the page
* Create new Document `Imprint` and publish

.. seealso::

    http://docs.plone.org/develop/plone/functionality/actions.html


Global navigation
+++++++++++++++++

* The horizontal navigation is called ``portal_tabs``
* go to ``portal_actions`` > ``portal_tabs`` `Link <http://localhost:8080/Plone/portal_actions/portal_tabs/manage_main>`_
* Edit ``index_html``

Where is the navigation?

The navigation shows content-objects, which are in Plone's root. Plus all actions in portal_tabs

Explain & edit index_html

Configuring the navigation itself is done elsewhere: http://localhost:8080/Plone/@@navigation-controlpanel

If time explain:

* user > undo (cool!)
* user > login/logout


Skins (portal_skins)
********************

In portal_skins we can change certain images, css-files and templates.

* portal_skins is deprecated technology
* We only do some minial changes here.

.. only:: manual

    Plone 5 will get rid of a lot of functionality that still lives in portal_skins.

    We used to do this part of the training with `plone.app.themeeditor <https://pypi.python.org/pypi/plone.app.themeeditor>`_ which has a much nicer UI than the ZMI but also has dependencies that are incompatible with ZopeSkel and is not widely used.


Change some css
+++++++++++++++

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
        width: 1024px;
    }

.. only:: presentation

    * Save and check the results

.. only:: manual

    Click 'save' and check results in the a different browser-tab. How did that happen?

    The UI leaves a lot to be desired. In a professional context this is no-go (no version-control, no syntac-highlighting etc. pp.). But everybody uses portal_skins it to make quick fixes to sites that are already online.

    Let's add some more css to make our site a little responsive:

.. only:: presentation

    * Add some more css

.. code-block:: css

    @media only screen and (max-width: 980px) {
       #visual-portal-wrapper {
           position: relative;
           width: auto;
       }
    }

    @media only screen and (max-width: 768px) {
       #portal-columns > div {
           width: 97.75%;
           margin-left: -98.875%;
           clear: both;
       }

       .searchButton,
       .searchSection {
           display: none;
       }
    }

Change the logo
+++++++++++++++

Let's change the Logo.

* Download a old ploneconf logo: http://www.sixfeetup.com/blog/2011PloneConfLogo.gif
* Go to ``portal_skins`` / ``plone_images``
* Click on ``logo.png``, click ``Customize`` and Upload the Logo.

.. seealso::

   http://docs.plone.org/adapt-and-extend/change-the-logo.html


portal_view_customizations
**************************

Change the footer
+++++++++++++++++

* Go to ``portal_view_customizations``
* Search ``plone.footer``, click and customize
* replace the content with the following

  .. code-block:: html

     <div i18n:domain="plone"
          id="portal-footer">
        <p>&copy; 2014 by me! |
          <a href="mailto:info@ploneconf.org">
           Contact us
          </a>
        </p>
     </div>


.. seealso::

   http://docs.plone.org/adapt-and-extend/theming/templates_css/skin_layers.html


CSS-Registry (portal_css)
*************************

* go to ZMI > ``portal_css``
* at the bottom there is ``ploneCustom.css``
* Disable ``Development mode``: The css-files are merged and have a cache-key.


Further tools in the ZMI
************************

There are many more noteable items in the ZMI. We'll visit some of them later.

* acl_users
* error_log
* portal_properties
* portal_setup
* portal_workflow
* portal_catalog


Summary
-------

You can configure and customize a lot in Plone through the web. The most important options are accessible in the `plone control panel <http://localhost:8080/Plone/@@overview-controlpanel>`_ but even more are hidden away in the `ZMI <http://localhost:8080/Plone/manage>`_. The amount of stuff is overwhelming but you'll get the hang of it through a lot of practice.
