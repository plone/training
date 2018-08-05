.. _intro-what-is-plone-label:


==============
What is Plone?
==============

Plone is an open source Content Management System (CMS) built in Python.

* Open-Source Enterprise-CMS
* Written in Python
* Plone 5.1 supports Python 2.7
* Plone 5.2 will support Python 3.6+ and 2.7
* `RESTful hypermedia API <https://github.com/plone/plone.restapi/>`_
* Based on the Web-Framework Zope
* Database: "Zope Object Database" (ZODB) or ORM & SQL/Postgres/Oracle
* Runs on Linux, Mac OS, BSD, Solaris, NixOS and Windows

Plone has a multitude of powerful features, is easily accessible to editors but also fun for programmers.

* Workflow-driven, collaborative management of content
* Industrial Strength Security and Access-Control
* Limitless Extensibility

..  note::

    The modular and open component architecture of Plone allows you to change or extend Plone in every respect!


Core concepts
=============

Traversal
---------

* Plone uses `Traversal <https://docs.plone.org/develop/plone/serving/traversing.html>`_ (portal/folder/document) instead of Routing
* Python objects in a object tree that looks like a huge nested dictionary:

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

* Objects can be called and return a representation of itself - usually html.

.. code-block:: python

    >>> obj = portal['folder1']['a-newsitem']
    >>> obj
    <NewsItem at xxx>
    >>> obj()
    u'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml...'


Schema-driven content
---------------------

* Models/Schemas with fields: Content has fields to store data defined in a schema.
* Values of these fields on instances of objects are attributes

    >>> obj.title
    u'A Newsitem'
    >>> obj.description
    u'Some description'
    >>> obj.description = u'A new description'
    >>> obj.description
    u'A new description'
    >>> obj.image
    <plone.namedfile.file.NamedBlobImage object at 0x11634c320>

* Objects can have multiple schemata. Additional schemata are called behaviors.

    >>> from plone.dexterity.utils import iterSchemata
    >>> pp [i for i in iterSchemata(self.context)]
    [<InterfaceClass plone.dexterity.schema.generated.Plone_0_News_1_Item>,
     <SchemaClass plone.app.dexterity.behaviors.metadata.IDublinCore>,
     <SchemaClass plone.app.contenttypes.behaviors.richtext.IRichText>,
     <SchemaClass plone.app.dexterity.behaviors.discussion.IAllowDiscussion>,
     <SchemaClass plone.app.dexterity.behaviors.id.IShortName>,
     <SchemaClass plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation>,
     <SchemaClass plone.app.relationfield.behavior.IRelatedItems>,
     <SchemaClass plone.app.contenttypes.behaviors.leadimage.ILeadImage>,
     <SchemaClass plone.app.versioningbehavior.behaviors.IVersionable>]
    >>> pp [[fieldname for fieldname in schema] for schema in [schemata for schemata in iterSchemata(obj)]]
    [[],
     ['language', 'expires', 'contributors', 'effective', 'rights', 'title', 'creators', 'subjects', 'description'],
     ['text'],
     ['allow_discussion'],
     ['id'],
     ['exclude_from_nav'],
     ['relatedItems'],
     ['image', 'image_caption'],
     ['versioning_enabled', 'changeNote']]

* Plone creates forms from all these schemata to add and edit content.


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

    * The Keynote by Cris Ewing at PyCon 2016: https://youtu.be/eGRJbBI_H2w?t=21m47s


Deployment
----------

A deployment setup could look like this:

.. code-block:: text

    ZEO-Server   ->   ZEO-Server (ZRS)

       / | \

    ZEO Clients (as many as you want)

       \ | /

    Load balancer (haproxy or nginx)

         |

       Cache (varnish)

         |

      Webserver (nginx)

         |

      Internet

Zope comes with its own basic Webserver (ZServer). With 5.2 (Python 3) it is replaced by a WSGI-Server like waitress or uwsgi.


