---
myst:
  html_meta:
    "description": "Technical view"
    "property=og:description": "Technical view"
    "property=og:title": "What is Plone?"
    "keywords": "Plone, Zope, security, CMS, REST, React, traversing, database, object oriented, acquisition"
---

(intro-what-is-plone-label)=

# What is Plone?

Plone is an Open Source Content Management System (CMS).
A CMS lets non-technical people create and maintain content for a public website or an intranet in a web browser.

- Open Source
- 25 years of experience
- Written and extensible in Python and JavaScript
- {doc}`Plone REST API<plone6docs:plone.restapi/docs/source/index>`
- Volto: React-based frontend and editor
- Based on the web framework {term}`Zope`
- Database: Zope Object Database ({term}`ZODB`) or relational database
- Runs on Linux-based systems
- Docker images available

Plone has a multitude of powerful features, is easily accessible to editors, but also fun for developers.

- Workflow-driven, collaborative management of content
- Industrial-strength security and access control
- Limitless extensibility and huge ecosystem of add-ons

The modular and open component architecture of Plone allows you to change or extend Plone in every aspect!

```{seealso}
Plone documentation on [docs.plone.org](https://6.docs.plone.org/)  
Demo installation on [demo.plone.org](https://demo.plone.org/)
```

## Core concepts

Here are the technical concepts that Plone uses.
They make Plone special and distinguish it from most other systems.


(what-is-plone-traversal-label)=

### Traversal

- Plone uses {ref}`Traversal<plone6docs:backend-traversal-label>` (portal/news/conference-site-online) instead of URL dispatch.
- Python objects exists in an object tree that looks like a huge nested dictionary:

```python
{'site': {'news': {'conference-website-online': page_object}}}
```

- Objects can be accessed like walking through a file system:

```python
portal['news']['conference-site-online']
```

```python
>>> from plone import api
>>> portal = api.portal.get()
>>> portal.keys()
['news', 'events', 'talks']
>>> portal['news']
<Document at /Plone/news>
```

(schema-driven-types-label)=

### Schema-driven content

Plone comes with a list of pre-defined content types.

Content types are defined in schemas.
A schema defines fields to store data.

Values of these fields are attributes on content objects.

```python
>>> obj.title
'A Newsitem'
>>> obj.description
'Some description'
>>> obj.description = 'A new description'
>>> obj.description
'A new description'
>>> obj.image
<plone.namedfile.file.NamedBlobImage object at 0x113793b30 oid 0x7e0b in <Connection at 10e57cdc0>>
>>> obj.image.data
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x01,\x01,...'
```

Objects can have multiple schemas.
Additional schemas are called `behaviors`.
They are meant to be used across content types to add shared functionality.

```python
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
```

Each behavior schema can define fields.
The values of these fields are again attributes on content objects.
Plone creates forms for all these schemas to add and edit content.


(what-is-plone-component-architecture-label)=

### Component Architecture

- Plone logic is wired together by a component architecture.
- The Zope Component Architecture (ZCA) is a Python framework for supporting component-based design and programming.
- It allows component pluggability and complex dispatching based on objects which implement an interface.

```{seealso}
- [Zope Component Architecture](https://zopecomponent.readthedocs.io/en/latest/narr.html)
- The [Keynote](https://www.youtube.com/watch?t=1308&v=eGRJbBI_H2w) by Cris Ewing at PyCon 2016
```


(what-is-plone-traversal-architecture-label)=

## Architecture

Plone is a Python CMS with an object oriented database based on Zope with a React frontend.
Wait, what?

```
  Volto
    ↑
  REST API
    ↑
  Plone
    ↑
  Zope
    ↑
  ZODB
    ↑
  Python
```


### Python

Python is an easy to learn, powerful programming language with a huge ecosystem of feature dedicated packages.
It ranks consistently as one of the most popular programming languages.


(what-is-plone-traversal-architecture-zodb-label)=

### Database (ZODB)

Data is stored in an object-oriented database called [ZODB](https://zodb.org/en/latest/): Zope Object Database.

  - There is no separate language for database operations like SQL
  - There is very little impact on code to make objects persistent
  - Object database != ORM
  - There is almost no seam between code and database.
  - "NoSQL"

```python
import persistent

class Account(persistent.Persistent):

    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):
        self.balance += amount

    def cash(self, amount):
        assert amount < self.balance
        self.balance -= amount
```

```{seealso}
- [ZEO](https://github.com/zopefoundation/ZEO): Server + many clients
- [RelStorage](https://relstorage.readthedocs.io/en/latest/) stores ZODB objects in PostgreSQL, MySQL, etc.
- `blobstorage` (binary large objects) in filesystem
```


(what-is-plone-traversal-architecture-zope-label)=

### Zope

[Zope](https://www.zope.dev/) is a web application framework that Plone runs on top of.

Zope is mostly written in Python (some performance-critical things are implemented in C).
It serves applications that communicate with users via `HTTP`.
Plone 6.2 uses Zope 6.1.

````{only} not presentation
Before Zope, web applications were often realized using plain [CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface).
An Apache web server would execute a script with the request data passed to it on standard input and as environment variables.
The script would then just print HTML to the standard output.
Apache returned that to the user.
Opening database connections, checking permission constraints, generating valid HTML, configuring caching,
interpreting form data and everything else: you had to do it on your own.

When the second request comes in, you have to do everything again.

Jim Fulton thought that this was slightly tedious.
So he wrote code to handle requests.
He believed that site content is object-oriented and that the URL should somehow point directly into the object hierarchy,
so he wrote an object-oriented database, called [ZODB](https://zodb.org/en/latest/).

The ZODB is a fully [ACID](https://en.wikipedia.org/wiki/ACID) compliant database with automatic transactional integrity.
It automatically maps traversal in the object hierarchy to URL paths, there is no need to "wire" objects or database nodes to URLs.

This gives Plone its easy SEO-friendly URLs.

Traversal through the object database is security checked at every point via very fine grained access-control lists.

```{note} Acquisition

One missing piece is important and complicated: `Acquisition`.

Acquisition is a kind of magic. Imagine a programming system where you do not access the file system and where you do not need to import code.
You work with objects.
An object can be a folder that contains more objects, an HTML page, data, or another script.

To access an object, you need to know where the object is.
Objects are found by paths that look like URLs, but without the domain name.
Now Acquisition allows you to write an incomplete path.

An incomplete path is a relative path, it does not explicitly state that the path starts from the root,
it starts relative to where the content object is -- its context.

If Zope cannot resolve the path to an object relative to your code, it tries the same path in the containing folder.
And then the folder containing the folder.

This might sound weird, what do I gain with this?

You can have different data or code depending on your {py:obj}`context`.
Imagine you want to have header images differing for each section of your page, sometimes even differing for a specific subsection of your site.

You define a path `header_image` and put a header image at the root of your site.
If you want a folder with a different header image, you put the header image into this folder.

Please take a minute to let this settle and think about what this allows you to do.

- contact forms with different e-mail addresses per section
- different CSS styles for different parts of your site
- One site, multiple customers, everything looks different for each customer.

As with all programming magic, acquisition exacts a price.
Zope code must be written carefully in order to avoid inheriting side effects via acquisition.

The Zope community expresses this with the Python (Monty) maxim: Beware the `Spammish Acquisition`.
```

```{seealso}
- <https://www.zope.dev/world.html>
- <https://zope.readthedocs.io/en/latest/zopebook/>
```
````


(what-is-plone-traversal-architecture-plone-label)=

### Plone content management system

This is the backend of the CMS.
Indeed it is a collection of Python packages extending a Zope application.

Plone adds to a Zope application: workflows, a framework to define content types, the feature to maintain multi-language content, a catalog indexing content, and many more features.


(what-is-plone-traversal-architecture-rest-api-label)=


### REST API

The Plone {doc}`plone6docs:plone.restapi/docs/source/index`
is a hypermedia API to access Plone content using REST (Representational State Transfer).

It is used to connect the Volto frontend with the Plone backend.


(volto-basics-label)=

### Volto frontend

[Volto](https://github.com/plone/volto) is the default frontend for Plone 6, built using the React library.
It uses the REST API to communicate with the backend and offers a modern editing experience.

Here are some basics that you need to understand if you are new to Volto:

- All data is stored in the Plone backend.
  The Volto frontend provides the user interface to display and edit the content.
- Volto is built in [React](https://www.react.dev), a Javascript library for creating web components.
- Volto uses the Plone {doc}`plone6docs:plone.restapi/docs/source/index` to communicate with the Plone backend.
- Volto is installed separately from the Plone backend.
  See chapter {ref}`installation-install-frontend-label` for instructions.
- Volto runs in a different process than the Plone backend.
  By default Volto runs on port 3000. If you start Volto with `make start` you can see the frontend on <http://localhost:3000>.
  The Plone backend runs by default on <http://localhost:8080>
- Volto uses [Semantic UI React components](https://react.semantic-ui.com/) to compose most of the views.
- The Volto default theme is based on Semantic UI theme and is called [Pastanaga](https://www.youtube-nocookie.com/embed/wW9mTl1Tavc?t=133s&privacy_mode=1).
- Same as Plone Blicca, Volto is highly extendable with add-ons for further features.
- Existing Volto components are customizable with a technique called {ref}`volto-overrides-componentshadowing-label`.
- Volto provides server-side rendering (SSR), important for SEO-purposes.
- Volto aims to provide 100% of the features of the current Plone backend.
  However, a few features of Plone are not implemented in Volto yet.
- Volto provides additional functionality that Plone does not have.
- For example Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks.
  This feature is enabled for content types that have the behavior `volto.blocks` enabled.
- Using the `Volto` editor, the content you add in blocks and the arrangement of blocks is stored as JSON in the schema fields `blocks` and `blocks_layout` provided by the dexterity behavior `volto.blocks`.
  Additionally you can edit all fields of the content type schema in a sidebar.
- If you do not use the behavior `volto.blocks`, the fields from a content-type schema are edited and stored exactly like previously in Plone Classic.

```{note}
There is a new React-based Plone frontend under development, called [Aurora](https://github.com/plone/aurora).

Aurora intends to replace Volto using updated technologies including TypeScript, Vite, React Router 8, and a new Plone-specific component library.
However, it is not yet feature complete enough to use for this training.
```

### Blicca frontend

The Plone Blicca frontend is a stable alternative to the Volto frontend that uses server-side rendered HTML.

* It is similar to the frontend used in Plone 5, and is also sometimes called the "Classic UI."
* Blicca includes a default theme called Barceloneta.
  Since Plone 6 it uses [Bootstrap 5](https://getbootstrap.com/).
* Blicca uses the template engine [Chameleon](https://chameleon.readthedocs.io/en/latest/) to create HTML.
* Interactivity is implemented using [Patternslib](https://patternslib.com/), a JavaScript library that can attach functionality to HTML using special classes and data attributes.


```{note} Choosing the right frontend

Here are some pointers that may help you decide:

- The Volto frontend is recommended for new projects, especially for developers who are more familiar with JavaScript than Python.
  It is also the frontend we will focus on in this training.
- Existing projects that are updated to Plone 6 can decide which frontend to use.
  If a lot of customizations were done and you don't want to reimplement a lot of custom templates and features in Volto, it is a good idea to use the Blicca frontend.
- If you plan to use add-ons, pay attention to which frontend they support.
  Some add-ons support both Volto and Blicca, but others only support one specific frontend.
  For a selection of awesome Volto add-ons see <https://github.com/collective/awesome-volto/>
- Ask the community for advice if you are not certain what to choose: https://community.plone.org/
```