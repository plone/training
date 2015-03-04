Part 1 in nutshell
==================

The case study
--------------

For this training we will build a website for a fictional Plone conference.

Main features will be:

* As a visitor I want to find current information on the conference
* As a visitor I want to register for the conference
* As a visitor I want to see the talks and sort them by my preferences
* As a speaker I want to be able to submit talks
* As a speaker I want to see and edit my submitted talks
* As a jury-member I want to vote on talks
* As a jury-member I want to decide, which talks to accept, and which not
* As an organizer I want to see a list of all proposed talks

Note that all of our requirements connect roles with capabilities. This is important because we'll want to limit the capabilities to those to whom we assign particular roles.


The Anatomy of Plone
--------------------

Full chapter: :doc:`anatomy`

* Zope2 is a web application framework that Plone runs on top of.
* ZODB is the Object Database used
* `CMF (Content Management Framework) <http://old.zope.org/Products/CMF/index.html/>`_ is an add-on for Zope to build Content Management Systems (like Plone).
* Zope Toolkit / Zope3 was intended as a ground-up rewrite of Zope.
* Plone uses parts of it provided by the `Zope Toolkit (ZTK) <http://docs.zope.org/zopetoolkit/>`_.
* Zope Component Architecture (ZCA) is a system which allows for component pluggability and complex dispatching. I is based on objects which implement an interface (a description of a functionality). Pyramid, and independent Python web application server, uses the ZCA “under the hood” to perform view dispatching and other application configuration tasks.
* Acquisition


The Features of Plone
---------------------

Full chapter: :doc:`features`

Starting/Stopping
*****************

We control Plone with a small script called "instance"::

    $ ./bin/instance fg
    $ ./bin/instance start
    $ ./bin/instance stop
    $ ./bin/instance -O Plone debug
    $ ./bin/instance -O Plone run myscript.py
    $ ./bin/instance adduser

Go to http://localhost:8080/Plone to see the site that comes with the provided database.


Users
*****

Let's create a Plone user which we use for most of the training:

#. :guilabel:`admin` > :guilabel:`Site setup` > :guilabel:`Users and Groups`
#. Add a user ``training`` with password: ``training``. Add him to the group Administrators

We already have the following users in the provided Database:

#. "editor:editor" (groups: None)
#. "jurymember:jurymember" (groups: None)
#. "testuser:testuser" (groups: None)

* The mailserver is already configured. Please do not abuse the account. We'll disable it after the training.


The Plone UI
************


Content-Types
*************

These are the default content-types:

* Document
* News Item
* Event
* File
* Image
* Link
* Folder
* Collection

.. note::

    Please keep in mind that we use `plone.app.contenttypes <http://docs.plone.org/external/plone.app.contenttypes/docs/README.html>`_ for the training. Therefore the types are based on Dexterity and slightly different from the types that you will find in a default-Plone 4.3.x-site.

We created a site-structure:

* Add folder "The Event" and in that ...

  * Folder "Talks"
  * Folder "Training"
  * Folder "Sprint"

* In /news: Added a News Item "Conference Website online!" with some image
* In /news: Added a News Item "Submit your talks!"
* In /events: Added an Event "Deadline for talk-submission" Date: 10.10.2014

* Added a Folder "Register"
* Deleted the Folder "Members" (Users)
* Added a Folder "Intranet"

Some core-features
******************

* folder_contents
* default_pages
* Collections
* Content Rules
* Versioning
* Members, roles and groups
* Workflows
* Working copy
* Placeful workflows


Configuring and Customizing Plone
---------------------------------

Full chapter: :doc:`configuring_customizing`

* The Control Panel  http://localhost:8080/Plone/@@overview-controlpanel
* Portlets http://localhost:8080/Plone/@@manage-portlets
* Viewlets http://localhost:8080/Plone/@@manage-viewlets
* ZMI http://localhost:8080/Plone/manage
* portal_actions (We added a link to ``string:${portal_url}/imprint``)
* portal_skins (we changed some css and changed the logo)
* portal_view_customizations (we customized the footer)


Extending Plone
---------------

Full chapter: :doc:`extending`

* skin_folders
* GenericSetup
* Component Architecture (zcml)

Extend Plone with Add-On Packages
---------------------------------

Full chapter: :doc:`addons`

* Finding addons
* noteable add-ons
* Installing Add-ons

Buildout
--------

Full chapter: :doc:`buildout_1`

* We discussed the buildout used for this training

Since Plone 4.3.4 was released today you could update the buildout to use this version.

Change ``buildout.cfg`` to extend from the ``versions.cfg`` of Plone 4.3.4

.. code-block:: ini
    :emphasize-lines: 2

    extends =
        http://dist.plone.org/release/4.3.4/versions.cfg
        versions.cfg


Creating addons to customize Plone
----------------------------------

Full chapter: :doc:`eggs1`

* We created a egg using ZopeSkel (not mr.bob).
* The egg is called ``ploneconf.site``
* It will contain most of the code we write
* Does everybody have the code from ``ploneconf.site_sneak`` already?

.. code-block:: bash

    $ cd src
    $ git clone https://github.com/collective/ploneconf.site_sneak.git


