.. _intro-what-is-plone-label:


==============
What is Plone?
==============

Plone is an open source Content Management System (CMS) built in Python. A CMS lets non-technical people create and maintain information for a public website or an intranet using only a web browser.

* Open-Source Enterprise-CMS
* Written in Python
* Plone 5.1 and below support Python 2
* Plone 5.2 supports Python 3 and 2
* Plone 6 supports Python 3
* `RESTful hypermedia API <https://plonerestapi.readthedocs.io/en/latest//>`_
* Optional React frontend and editor `Volto`
* Based on the Web-Framework Zope
* Database: `Zope Object Database` ZODB or ORM & SQL/Postgres/Oracle
* Runs on Linux, macOS, BSD, Solaris, NixOS and Windows

Plone has a multitude of powerful features, is easily accessible to editors but also fun for programmers.

* Workflow-driven, collaborative management of content
* Industrial Strength Security and Access-Control
* Limitless Extensibility

..  note::

    The modular and open component architecture of Plone allows you to change or extend Plone in every respect!

.. seealso::

    * `What Is Plone? <https://docs.plone.org/intro/index.html>`_
    * `Conceptual Overview <https://docs.plone.org/working-with-content/introduction/conceptual-overview.html>`_


Core concepts
=============

Here are the technical concepts that Plone uses.
They make Plone special and distinguish it from most other systems.

Traversal
---------

* Plone uses `Traversal <https://docs.plone.org/develop/plone/serving/traversing.html>`_ (portal/folder/document) instead of Routing
* Python objects exists in a object tree that looks like a huge nested dictionary:

.. code-block:: python

    {'site': {'folder': {'page': page_object}}}

* Objects can be accessed like walking through a file-system:

.. code-block:: python

    root['site']['folder']['page']

.. code-block:: python

    >>> from plone import api
    >>> portal = api.portal.get()
    >>> portal.keys()
    ['folder1', 'document1']
    >>> portal['folder1']
    <Folder at xxxx>


Object publishing
-----------------

Objects can be called and return a representation of itself - usually HTML.

.. code-block:: python

    >>> obj = portal['folder1']['a-newsitem']
    >>> obj
    <NewsItem at xxx>
    >>> obj()
    u'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml...'


.. _schema-driven-types-label:

Schema-driven content
---------------------

Plone comes with a list of pre-defined content-types.

Content types are defined in models/schemas. A schema can define fields to store data.

Values of these fields are attributes on content objects.

.. code-block:: python

    >>> obj.title
    u'A Newsitem'
    >>> obj.description
    u'Some description'
    >>> obj.description = u'A new description'
    >>> obj.description
    u'A new description'
    >>> obj.image
    <plone.namedfile.file.NamedBlobImage object at 0x11634c320>
    >>> obj.image.data
    '\x89PNG\r\n\x1a\n\x00\x00\x00\...'

Objects can have multiple schemata.
Additional schemata are called behaviors.
They are meant to be used across content types to add shared functionality.

.. code-block:: python

    >>> from plone.dexterity.utils import iterSchemata
    >>> [i for i in iterSchemata(self.context)]
    [<InterfaceClass plone.dexterity.schema.generated.Plone_0_News_1_Item>,
     <SchemaClass plone.app.dexterity.behaviors.metadata.IDublinCore>,
     <SchemaClass plone.app.contenttypes.behaviors.richtext.IRichText>,
     <SchemaClass plone.app.dexterity.behaviors.discussion.IAllowDiscussion>,
     <SchemaClass plone.app.dexterity.behaviors.id.IShortName>,
     <SchemaClass plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation>,
     <SchemaClass plone.app.relationfield.behavior.IRelatedItems>,
     <SchemaClass plone.app.contenttypes.behaviors.leadimage.ILeadImage>,
     <SchemaClass plone.app.versioningbehavior.behaviors.IVersionable>]

Each behavior schema can define fields.
The values of these fields are again attributes on content objects.
Plone creates forms for all these schemata to add and edit content.


Component Architecture
----------------------

* Plone logic is wired together by a component architecture.
* A pluggable system of interfaces, adapters, utilities, events and registries.
* ZCA: A Python framework for supporting component based design and programming
* zope.interface
* zope.event
* zope.component

Written by smart people:

* Jim Fulton
* Stephan Richter
* Philipp von Weitershausen
* Guido van Rossum
* Tres Seaver
* Phillip J Eby
* Martijn Faassen
* ...

.. seealso::

    * The Keynote by Cris Ewing at PyCon 2016: https://www.youtube.com/watch?v=eGRJbBI_H2w&feature=youtu.be&t=21m47s


Rest API
--------

`plone.restapi <https://plonerestapi.readthedocs.io/en/latest/>`_
is a hypermedia API to access Plone content using REST (Representational State Transfer).

It is used to connect the Volto frontend with Plone.


Volto Frontend
--------------

`Volto <https://github.com/plone/volto>`_ is a frontend for Plone 6 written in ReactJS. It uses the Rest API to communicate with the backend and offers a modern editing experience.


Classic Frontend
----------------

A stable alternative to the JavaScript frontend Volto is the classic frontend of Plone that uses server-side rendered HTML.
Plone ships with a default theme called Barceloneta.
Since Plone 6 it uses `Bootstrap 4 <https://getbootstrap.com/>`_.
