.. _theming-label:

Theming
=======

..  warning::

    This chapter has not yet been updated for Plone 5!

We don't do any real theming during the training. We'll just explain the options you have.

Theming a Plone site has two major parts:

* **Structural theming**: the construction of the HTML skeleton of a page and getting the right content elements into the right spots. Also, providing the CSS and Javascript elements to finish the presentation and provide dynamic behaviors.

* **Templating**, which itself has two aspects:

  * Viewlet templates, which we might think of as the micro formatting of the page. Remember when we looked at the viewlet map of a page? (Look again via ``@@manage-viewlets``.) All those viewlets are provided via individual, editable templates.

  * Content type view templates. Whenever we create a new content type or modify an existing one, we'll typically want to create or modify a view template.

*Structural theming* is best accomplished via the Diazo theme engine. Diazo provides a rule based mechanism for mapping content provided by Plone into one or more master page designs.

*Templating* is accomplished by editing page template files which allow us to mix object content from the ZODB with HTML. Plone uses its own (actually Zope's) Template Attribute Language (TAL) for this purpose.

.. _theming-diazo-label:

Diazo example
-------------

* Activate Diazo via the add-ons control panel form
* Go to the ``theming`` control panel
* Activate the Bootstrap theme
* Look at the site changes
* Replace "localhost" in your URL with "127.0.0.1"
* Return to the theming control panel, take a look at the advanced pane
* Deactivate the theme
* Copy the Bootstrap Theme, use the ``Modify Theme`` button to see the Diazo rules.

.. _theming-templating-label:

Templating example
------------------

* Use the ZMI to view portal_view_customizations
* Take a look at ``plone.belowcontenttitle.documentbyline`` — get an idea how TAL logic is used to pull in context content.
* Change "History" to "Herstory" :)

.. _theming-right-tool-label:

Choosing the right tool
-----------------------

*If all you have is a hammer, everything looks like a nail*

Doing a good job with Plone theming means picking the right tool for the job.

If you're very good with Diazo, you can do very nearly everything with Diazo rules. It's entirely possible to replace and reorder the tiniest components of a viewlet with a clever application of a Diazo rule or a little bit of XSL.

It's also entirely possible to do all your theming by customizing template files. After all, your original Plone site is themed (with a theme called Sunburst) even without turning on Diazo. Before Diazo joined Plone (as an add-on in Plone 4.0), this is the way Plone was themed.

So, what's your strategy?

* For simple site themes that are structurally similar to out-of-the-box Plone, just add CSS. Nothing more needed.

* For more complex themes or ones where you are provided with a theme HTML, CSS and JS, use Diazo to move things around, to put the puzzle pieces where they belong.

* If it's necessary to change a viewlet or the view of a content type, use TAL templating.

But, **do not** bother to learn how to work with Plone's viewlet managers. Yes, it was once necessary, but Diazo is a much better solution to this problem.


.. _theming-serious-label:

Want to really learn theming?
-----------------------------

Good starting places:

* Diazo (plone.app.theming): This is the modern way to go and the `default theme in Plone 5 <https://github.com/plone/plonetheme.barceloneta/>`_ will be a Diazo theme! Diazo is available from Plone 4.2+.
* You can use (and adapt) one of many publicly available Diazo themes: https://pypi.python.org/pypi?%3Aaction=search&term=plonetheme&submit=search (try `plonetheme.onegov <https://pypi.python.org/pypi/plonetheme.onegov>`_ for example)
* Creating a custom theme
* A starting point can be the built-in Diazo Theme editor
* Old-school Theming (extending the built-in default theme)
* Deliverance/XDV

If you seek a training about Diazo we recommend a training by `Chrissy Wainwright <https://twitter.com/cdw9>`_ or `Maik DerStappen <http://www.derstappen-it.de/>`_


.. seealso::

    Diazo: How it Works by Steve McMahon from Plone Conference 2013 https://www.youtube.com/watch?v=Vvr26Q5IriE

.. seealso::

    http://docs.plone.org/adapt-and-extend/theming/index.html
