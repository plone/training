Extend Plone with Add-ons
=========================

* There are more than 2000 addons for Plone. We will cover only a handfull today.
* Using them can saves a lot of time
* The success of a project often depends on finding the right addon
* Their use, usefulness, quality and complexity varies a lot


How to find addons
------------------

* https://pypi.python.org/pypi - use the search form!
* https://github.com/collective >1000 repos
* https://github.com/plone >240 repos
* http://news.gmane.org/gmane.comp.web.zope.plone.user
* google (e.g. `Plone+Slider <http://lmgtfy.com/?q=plone+slider>`_)
* Check shortlist (Plone Paragon) that will come in 2014 on plone.org
* ask in irc and on the mailing list

.. seealso::

   * A talk on finding and managing addons: http://www.youtube.com/watch?v=Sc6NkqaSjqw


Some noteable addons
--------------------

`Products.PloneFormGen <http://docs.plone.org/develop/plone/forms/ploneformgen.html>`_
  A form generator

`collective.plonetruegallery <https://pypi.python.org/pypi/collective.plonetruegallery>`_
  Photo galleries with a huge selection of various js-libraries

`collective.cover <https://github.com/collective/collective.cover/blob/master/docs/end-user.rst>`_
  UI to create complex landing-pages

`collective.geo <http://collectivegeo.readthedocs.org/en/latest/>`_
  Flexible bundle of addons to georeference content and display in maps

`collective.mailchimp <https://pypi.python.org/pypi/collective.mailchimp>`_
  Allows visitors to subcribe to mailchimp newsletters

`eea.facetednavigation <https://pypi.python.org/pypi/eea.facetednavigation/>`_
  Create faceted navigation and searches throught the web.

`webcouturier.dropdownmenu <https://pypi.python.org/pypi/webcouturier.dropdownmenu>`_
  Turns global navigation into dropdowns

`collective.quickupload <https://pypi.python.org/pypi/collective.quickupload>`_
  Multi-file upload using drag&drop

`Products.Doormat <https://pypi.python.org/pypi/Products.Doormat>`_
  A flexible doormat

`collective.behavior.banner <https://github.com/starzel/collective.behavior.banner>`_
  Add decorative banners and sliders

`plone.app.multilingual <http://pypi.python.org/pypi/plone.app.multilingual>`_
  Allows multilingual sites by translating content

`Plomino <http://www.plomino.net/>`_
  Powerful and flexible web-based application builder for Plone



Installing Addons
-----------------

Installation is a two-step process.

Making the addons code available to Zope
++++++++++++++++++++++++++++++++++++++++

First, we must make the addons code available to Zope. This means, that Zope can import the code. Buildout is responsible for this.

Look at ``buildout.cfg`` file in ``/vagrant/buildout``.

In the section ``[instance]`` there is a variable called ``eggs``, which has multiple *eggs* as a value. Add the following eggs:

We already have added the addons that we will use now:

* ``Products.PloneFormGen``
* ``collective.plonetruegallery``

Usually, one enters the eggs by adding one more line per egg into the configuration. You must write the egg name indented, this way buildout understands that the current line is part of the last variable and not a new variable.

If you add new addons here you will have to run buildout and restart the site:

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg

Now the code is importable from within Plone and everything got registered via ZCML.

Installing addons in your Plone Site
++++++++++++++++++++++++++++++++++++

Your Plone-site has not yet been told to use the addon. For this, you have to install the addons in your Plone Site.

In your browser, go the control panel ``@@plone_control_panel``, and open the ``Addons`` Panel. You will see that you can install the addons there.

Install **PloneFormGen** and  **Plone True Gallery** them now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

* configuring new actions,
* registering new content types
* registering css- and js-files
* creating some content/configuration objects in your Plone site.

Let' have a look at what we just installed.


PloneFormGen
------------

Creating forms in Plone:

* pure: html and python in a view
* framework: z3c.form, formlib, deform
* ttw: Products.PloneFormGen

Registration-form:

* Add a object of the new type 'Form Folder' in the site-root. Call it "Registration"
* Save and view the result
* Click in QuickEdit
* Remove field "Subject"
* Add fields for food-preference and shirt-size
* Add a DataSave Adapter


Add Photogallery with collective.plonetruegallery
-------------------------------------------------

To advertice the conference we want to show some photos showing past conferences and the city where conference is taking place in.

collective.plonetruegallery is a role model on how to write a Plone Extension.

Instead of creating custom content types for galleries, it integrates with the Plone functionality to choose different views for folderish content types.

https://pypi.python.org/pypi/collective.plonetruegallery

* Install the addon: http://localhost:8080/Plone/prefs_install_products_form
* Enable the behavior ``Plone True Gallery`` on the type ``Folder``: http://localhost:8080/Plone/dexterity-types/Folder/@@behaviors
* Add a folder /the-event/location
* Upload some fotos from http://lorempixel.com/600/400/city/
* Enable the view ``galleryview``


Internationalisation
--------------------

Plone can run the same site in many different languages.

We're not doing this with the conference-site since the lingua franca of the plone-community is english.

We would use http://pypi.python.org/pypi/plone.app.multilingual for this. It is the successor of Producs.LinguaPlone (which only works with Archetypes).


Summary
-------

We are now able to customize and extend many parts of our wesite. We can even install extensions that add new functionality.

But:

* Can we submit talks now?
* Can we create lists with the most important properties of each tasks?
* Can we allow a jury to vote on talks?

We often have to work with structured data. Up to a degree we can do all this TTW, but at some point we reach barriers. In the next part of the training, we'll teach you, how to break through these barriers.



