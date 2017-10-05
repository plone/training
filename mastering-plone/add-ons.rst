.. _add-ons-label:

Extend Plone With Add-On Packages
=================================

* There are more than 2,000 add-ons for Plone. We will cover only a handful today.
* Using them saves a lot of time
* The success of a project often depends on finding the right add-on
* Their use, usefulness, quality and complexity varies a lot


.. _add-ons-notable-label:

Some notable add-ons
---------------------

`Products.PloneFormGen <https://docs.plone.org/develop/plone/forms/ploneformgen.html>`_
  A form generator.

`collective.disqus <https://pypi.python.org/pypi/collective.disqus/>`_
  Integrates the Disqus commenting platform API into Plone

`collective.plonetruegallery <https://pypi.python.org/pypi/collective.plonetruegallery>`_
  Photo galleries with a huge selection of various js-libraries.

`plone.app.mosaic <https://github.com/plone/plone.app.mosaic>`_
  Layout solution to easily create complex layouts through the web.

`collective.geo <http://collectivegeo.readthedocs.io/en/latest/>`_
  Flexible bundle of add-ons to geo-reference content and display in maps

`collective.mailchimp <https://pypi.python.org/pypi/collective.mailchimp>`_
  Allows visitors to subscribe to mailchimp newsletters

`eea.facetednavigation <https://pypi.python.org/pypi/eea.facetednavigation/>`_
  Create faceted navigation and searches through the web.

`collective.lineage <https://pypi.python.org/pypi/collective.lineage>`_
  Microsites for Plone - makes subfolders appear to be autonomous Plone sites

`Products.Doormat <https://pypi.python.org/pypi/Products.Doormat>`_
  A flexible doormat

`collective.behavior.banner <https://github.com/collective/collective.behavior.banner>`_
  Add decorative banners and sliders

`plone.app.multilingual <https://pypi.python.org/pypi/plone.app.multilingual>`_
  Allows multilingual sites by translating content.

`Rapido <https://rapidoplone.readthedocs.io/en/latest/>`_
  Allows developers with a little knowledge of HTML and a little knowledge of Python to implement custom elements and insert them anywhere they want.

`Plomino <http://plomino.net/>`_
  Powerful and flexible web-based application builder for Plone

.. warning::

    Some add-ons may not yet run under Plone 5 and will have to be updated to be compatible.


.. _add-ons-find-label:

How to find add-ons
-------------------

* https://plone.org/download/add-ons
* https://pypi.python.org/pypi - use the search form!
* https://github.com/collective >1200 repos
* https://github.com/plone >260 repos
* https://community.plone.org - ask the community
* google (e.g. `Plone+Slider <http://lmgtfy.com/?q=plone+slider>`_)
* ask in irc and on the mailing list

.. seealso::

   * A talk on finding and managing add-ons: https://www.youtube.com/watch?v=Sc6NkqaSjqw


.. _add-ons-installing-label:

Installing Add-ons
------------------

Installation is a two-step process.

Making the add-on packages available to Zope
++++++++++++++++++++++++++++++++++++++++++++

First, we must make the add-on packages available to Zope. This means that Zope can import the code. Buildout is responsible for this.

Look at the :file:`buildout.cfg` file in :file:`/vagrant/buildout`.

.. note::

    If you're using our Vagrant kit, the Plone configuration is available in a folder that is shared between the host and guest operating systems.
    Look in your Vagrant install directory for the :file:`buildout` folder.
    You may edit configuration files using your favorite text editor in the host operating system, then switch into your virtual machine to run buildout on the guest operating system.

In the section ``[instance]`` there is a variable called ``eggs``, which has a list of *eggs* as a value. For example::

    eggs =
        Plone
        Products.PloneFormGen
        plone.app.debugtoolbar

You add an egg by adding a new line containing the package name to the configuration.
You must write the egg name indented: this way, buildout understands that the current line is part of the last variable and not a new variable.

If you add new add-ons here you will have to run buildout and restart the site:

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg

Now the code is available from within Plone.

Installing add-ons in your Plone Site
+++++++++++++++++++++++++++++++++++++

Your Plone site has not yet been told to use the add-on. For this, you have to activate the add-on in your Plone Site.

.. note::

    Why the extra step of activating the add-on package? You may have multiple Plone sites in a single Zope installation. It's common to want to activate some add-ons in one site, others in another.

In your browser, go to Site Setup (shortcut: add ``/@@overview-controlpanel`` to the Plone site URL), and open the ``Add-ons`` Panel. You will see that you can install the add-ons there.

Install **PloneFormGen** now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

* Configuring new actions
* Registering new contenttypes
* Registering css and js files
* Creating some content/configuration objects in your Plone site.

Let's have a look at what we just installed.


.. _add-ons-PFG-label:

PloneFormGen
------------

There are many ways to create forms in Plone:

* Pure: html and python in a view
* Framework: z3c.form, formlib, deform
* TTW: Products.PloneFormGen

The basic concept of PloneFormGen is that you build a form by adding a Form Folder, to which you add form fields as content items. Fields are added, deleted, edited and moved just as with any other type of content. Form submissions may be automatically emailed and/or saved for download. There are many add-ons to PloneFormGen that provide additional field types and actions.

Let's build a registration form:

* Activate PloneFormGen for this site via the add-on configuration panel in site setup
* Add an object of the new type 'Form Folder' in the site root. Call it "Registration"
* Save and view the result, a simple contact form that we may customize
* Click in QuickEdit
* Remove field "Subject"
* Add fields for food preference and shirt size
* Add a DataSave Adapter
* Customize the mailer

.. note::

    Need CAPTCHAs? Add the :py:mod:`collective.recaptcha` package to your buildout and PFG will have a CAPTCHA field.

    Need encryption? Add GPG encryption to your system, add a GPG configuration for the Plone daemon user that includes a public key for the mail targets, and you'll be able to encrypt email before sending.

    Think PFG is too complicated for your site editors? Administrators (and we're logged in as an administrator) see lots of more complex options that are invisible to site editors.

By the way, while PloneFormGen is good at what it does, it is not a good model for designing your own extensions. It was created before the Zope Component Architecture became widely used. The authors would write it much differently if they were starting from scratch.

.. note::

   `collective.easyform <https://pypi.python.org/pypi/collective.easyform>`_ is a alternative form-generator that uses dexterity. It is still under development.


.. _add-ons-ptg-label:

Add Photo Gallery with :py:mod:`collective.plonetruegallery`
------------------------------------------------------------

To advertise the conference we want to show some photos showing past conferences and the city where the conference is taking place.

Instead of creating new contenttypes for galleries, it integrates with the Plone functionality to choose different views for folderish contenttypes.

https://pypi.python.org/pypi/collective.plonetruegallery

* Activate the add-on
* Enable the behavior ``Plone True Gallery`` on the type ``Folder``: http://localhost:8080/Plone/dexterity-types/Folder/@@behaviors
* Add a folder ``/the-event/location``
* Upload some photos from lorempixel.com
* Enable the view ``galleryview``


.. _add-ons-i18n-label:

Internationalization
--------------------

Plone can run the same site in many different languages.

We're not doing this with the conference site since the *lingua franca* of the Plone community is English.

We would use the built-in addon https://pypi.python.org/pypi/plone.app.multilingual for this.

Building a multi-lingual site requires activating :py:mod:`plone.app.multilingual`, but no add-on is necessary to build a site in only one language. Just select a different site language when creating a Plone site, and all text in the user-interface will be switched to that language.


.. _add-ons-summary-label:

Summary
-------

We are now able to customize and extend many parts of our website. We can even install extensions that add new functionality.

But:

* Can we submit talks now?
* Can we create lists with the most important properties of each talk?
* Can we allow a jury to vote on talks?

We often have to work with structured data.
Up to a degree we can do all this TTW, but at some point we run into barriers.
In the next part of the training, we'll teach you how to break through these barriers.



