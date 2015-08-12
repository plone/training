.. _addons-label:

Extend Plone With Add-On Packages
=================================

* There are more than 2,000 add-ons for Plone. We will cover only a handful today.
* Using them saves a lot of time
* The success of a project often depends on finding the right add-on
* Their use, usefulness, quality and complexity varies a lot


.. _addons-find-label:

How to find add-ons
-------------------

* https://pypi.python.org/pypi - use the search form!
* https://github.com/collective >1200 repos
* https://github.com/plone >260 repos
* http://news.gmane.org/gmane.comp.web.zope.plone.user
* google (e.g. `Plone+Slider <http://lmgtfy.com/?q=plone+slider>`_)
* Check shortlist `Plone Paragon <http://paragon.plone.org/>`_ (Launched August 2014)
* ask in irc and on the mailing list

.. seealso::

   * A talk on finding and managing add-ons: http://www.youtube.com/watch?v=Sc6NkqaSjqw


.. _add-ons-notable-label:

Some noteable add-ons
---------------------

.. warning::

    Many add-ons will not yet run under Plone 5 and will have to be updated to be compatible. One Example is Products.PloneFormGen: We use our own source-checkout of it from https://github.com/starzel/Products.PloneFormGen that contains small changes that make it compatible with Plone 5.

    Other add-ons will be rendered obsolete by Plone 5. There is no more need for collective.quickupload since Plone 5 already has the functionality to upload multiple files at once.


`Products.PloneFormGen <http://docs.plone.org/develop/plone/forms/ploneformgen.html>`_
  A form generator.

`collective.plonetruegallery <https://pypi.python.org/pypi/collective.plonetruegallery>`_
  Photo galleries with a huge selection of various js-libraries

`collective.cover <https://github.com/collective/collective.cover/blob/master/docs/end-user.rst>`_
  UI to create complex landing-pages

`collective.geo <http://collectivegeo.readthedocs.org/en/latest/>`_
  Flexible bundle of addons to georeference content and display in maps

`collective.mailchimp <https://pypi.python.org/pypi/collective.mailchimp>`_
  Allows visitors to subcribe to mailchimp newsletters

`eea.facetednavigation <https://pypi.python.org/pypi/eea.facetednavigation/>`_
  Create faceted navigation and searches through the web.

`webcouturier.dropdownmenu <https://pypi.python.org/pypi/webcouturier.dropdownmenu>`_
  Turns global navigation into dropdowns

`collective.quickupload <https://pypi.python.org/pypi/collective.quickupload>`_
  Multi-file upload using drag&drop

`Products.Doormat <https://pypi.python.org/pypi/Products.Doormat>`_
  A flexible doormat

`collective.behavior.banner <https://github.com/collective/collective.behavior.banner>`_
  Add decorative banners and sliders

`plone.app.multilingual <http://pypi.python.org/pypi/plone.app.multilingual>`_
  Allows multilingual sites by translating content

`Plomino <http://www.plomino.net/>`_
  Powerful and flexible web-based application builder for Plone



.. _add-ons-installing-label:

Installing Add-ons
------------------

Installation is a two-step process.

Making the add-on packages available to Zope
++++++++++++++++++++++++++++++++++++++++++++

First, we must make the add-on packages available to Zope. This means that Zope can import the code. Buildout is responsible for this.

Look at the ``buildout.cfg`` file in ``/vagrant/buildout``.

.. note::

    If you're using our Vagrant kit, the Plone configuration is available in a folder that is shared between the host and guest operating systems. Look in your Vagrant install directory for the ``buildout`` folder. You may edit configuration files using your favorite text editor in the host operating system, then switch into your virtual machine to run buildout on the guest operating system.

In the section ``[instance]`` there is a variable called ``eggs``, which has a list of *eggs* as a value.

* ``Products.PloneFormGen``
* ``collective.plonetruegallery``

Usually, one enters the eggs by adding one more line per egg into the configuration. You must write the egg name indented, this way buildout understands that the current line is part of the last variable and not a new variable.

If you add new add-ons here you will have to run buildout and restart the site:

.. sourcecode:: bash

    $ cd /vagrant/buildout
    $ bin/buildout
    $ bin/instance fg

Now the code is available from within Plone.

Installing add-ons in your Plone Site
+++++++++++++++++++++++++++++++++++++

Your Plone site has not yet been told to use the add-on. For this, you have to activate the add-ons in your Plone Site.

.. note::

    Why the extra step of activating the add-on package? You my have multiple Plone sites in a single Zope installation. It's common to want to activate some add-ons in one site, others in another.

In your browser, go to Site Setup (shortcut: add ``/@@overview-controlpanel`` to the Plone site URL), and open the ``Add-ons`` Panel. You will see that you can install the add-ons there.

Install **PloneFormGen** and **Plone True Gallery** now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

* configuring new actions
* registering new content types
* registering css and js files
* creating some content/configuration objects in your Plone site.

Let's have a look at what we just installed.


.. _add-ons-PFG-label:

PloneFormGen
------------

There are many ways to create forms in Plone:

* pure: html and python in a view
* framework: z3c.form, formlib, deform
* TTW: Products.PloneFormGen

The basic concept of PloneFormGen is that you build a form by adding a Form Folder, to which you add form fields as content items. Fields are added, deleted, edited and moved just as with any other type of content. Form submissions may be automatically emailed and/or saved for download. There are many PFG add-ons that provide additional field types and actions.

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

    Need CAPTCHAs? Add the ``collective.recaptcha`` package to your buildout and PFG will have a CAPTCHA field.

    Need encryption? Add GPG encryption to your system, add a GPG configuration for the Plone daemon user that includes a public key for the mail targets, and you'll be able to encrypt email before sending.

    Think PFG is too complicated for your site editors? Administrators (and we're logged in as an administrator) see lots of more complex options that are invisible to site editors.

By the way, while PloneFormGen is good at what it does, is not a good model for designing your own extensions. It was created before the Zope Component Architecture became widely used. The authors would write it much differently if they were starting from scratch.


.. _add-ons-ptg-label:

Add Photogallery with collective.plonetruegallery
-------------------------------------------------

To advertise the conference we want to show some photos showing past conferences and the city where the conference is taking place.

Instead of creating custom content types for galleries, it integrates with the Plone functionality to choose different views for folderish content types.

https://pypi.python.org/pypi/collective.plonetruegallery

* Activate the add-on
* Enable the behavior ``Plone True Gallery`` on the type ``Folder``: http://localhost:8080/Plone/dexterity-types/Folder/@@behaviors (This step is only required because plonetruegallery does not yet know about the newer plone.app.contenttypes, which we activated to replace Plone's old content types with newer, Dexterity-style, ones.)
* Add a folder /the-event/location
* Upload some fotos from http://lorempixel.com/600/400/city/
* Enable the view ``galleryview``

collective.plonetruegallery is a better model for how to write a Plone Extension.

.. _addons-i18n-label:

Internationalization
--------------------

Plone can run the same site in many different languages.

We're not doing this with the conference site since the *lingua franca* of the Plone community is English.

We would use http://pypi.python.org/pypi/plone.app.multilingual for this. It is the successor of Products.LinguaPlone (which only works with Archetypes).

.. note::

    Building a multi-lingual site requires activating ``plone.app.multilingual``, but no add-on is necessary to build a site in a single language other than English. Just select a different site language when creating a Plone site, and all the basic messages will be translated and LTR or RTL needs will be handled.


.. _add-ons-summary-label:

Summary
-------

We are now able to customize and extend many parts of our website. We can even install extensions that add new functionality.

But:

* Can we submit talks now?
* Can we create lists with the most important properties of each talk?
* Can we allow a jury to vote on talks?

We often have to work with structured data. Up to a degree we can do all this TTW, but at some point we run into barriers. In the next part of the training, we'll teach you how to break through these barriers.



