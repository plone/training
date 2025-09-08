---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(intro-what-is-plone-label)=

# What is Plone?

Plone is an open source Content Management System (CMS) built in Python. A CMS lets non-technical people create and maintain information for a public website or an intranet using only a web browser.

- Open Source Enterprise `CMS`
- Written in `Python`
- `Plone` 5.2 supports `Python` 3 and 2
- `Plone` 6 supports `Python` 3
- {doc}`plone6docs:plone.restapi/docs/source/index`
- `Volto`: `React` based frontend and editor
- Based on the web framework {term}`Zope`
- Database: `Zope Object Database` {term}`ZODB` or `ORM` & `SQL`/`Postgres`/`Oracle`
- Runs on Linux, macOS, BSD, Solaris, NixOS and Windows

Plone has a multitude of powerful features, is easily accessible to editors but also fun for programmers.

- Workflow-driven, collaborative management of content
- Industrial Strength Security and Access-Control
- Limitless Extensibility

The modular and open component architecture of Plone allows you to change or extend Plone in every respect!

```{seealso}
- [What Is Plone?](https://5.docs.plone.org/intro/index.html)
- [Conceptual Overview](https://5.docs.plone.org/working-with-content/introduction/conceptual-overview.html)
```

## Core concepts

Here are the technical concepts that Plone uses.
They make Plone special and distinguish it from most other systems.

### Traversal

- Plone uses [Traversal](https://5.docs.plone.org/develop/plone/serving/traversing.html) (portal/folder/document) instead of URL dispatch.
- Python objects exists in a object tree that looks like a huge nested dictionary:

```python
{'site': {'folder': {'page': page_object}}}
```

- Objects can be accessed like walking through a file-system:

```python
root['site']['folder']['page']
```

```python
>>> from plone import api
>>> portal = api.portal.get()
>>> portal.keys()
['folder1', 'document1']
>>> portal['folder1']
<Folder at xxxx>
```

### Object publishing

Objects can be called and return a representation of itself - usually HTML.

```python
>>> obj = portal['folder1']['a-newsitem']
>>> obj
<FolderishNewsItem at /Plone/folder1/a-newsitem>
>>> obj()
'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml...'
```

(schema-driven-types-label)=

### Schema-driven content

Plone comes with a list of pre-defined content-types.

Content types are defined in models/schemas. A schema can define fields to store data.

Values of these fields are attributes on content objects.

```python
>>> obj.title
'A Newsitem'
>>> obj.description
'Some description'
>>> obj.description = u'A new description'
>>> obj.description
'A new description'
>>> obj.image
<plone.namedfile.file.NamedBlobImage object at 0x113793b30 oid 0x7e0b in <Connection at 10e57cdc0>>
>>> obj.image.data
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x01,\x01,...'
```

Objects can have multiple schemata.
Additional schemata are called `behaviors`.
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

Each `behavior` schema can define fields.
The values of these fields are again attributes on content objects.
Plone creates forms for all these schemata to add and edit content.

### Component Architecture

- Plone logic is wired together by a component architecture.
- The Zope Component Architecture (ZCA) is a Python framework for supporting component based design and programming.
- It allows component pluggability and complex dispatching based on objects which implement an interface.

```{seealso}
- [Zope Component Architecture](https://zopecomponent.readthedocs.io/en/latest/narr.html)
- The Keynote by Cris Ewing at PyCon 2016: <https://www.youtube.com/watch?v=eGRJbBI_H2w&feature=youtu.be&t=21m47s>
```

(intro-architecture)=

## Architecture

Plone started as an extension for CMF, which is a extension for Zope... wait, what?

```
  VOLTO
    ↑
  RESTAPI
    ↑
  PLONE
    ↑
  ZOPE
    ↑
  ZODB
    ↑
  Python
```


### Python

Python is an easy to learn, powerful programming language.
It ranks consistently as one of the most popular programming languages.

Plone 6 supports Python 3.8 and newer.

### Database (ZODB)

To store data Plone uses a database called `ZODB`.

- [ZODB](https://zodb.org/en/latest/): A native object database for Python

  - There is no separate language for database operations like SQL
  - There is very little impact on code to make objects persistent
  - Object database != ORM
  - There is almost no seam between code and database.

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

- "NoSQL"
- [ZEO](https://github.com/zopefoundation/ZEO): Server + many clients
- [ZRS](https://github.com/zopefoundation/zc.zrs): DB-Replication
- [RelStorage](https://relstorage.readthedocs.io/en/latest/) (store pickles in a relational database) for Postgres, MySQL etc.
- blobstorage (binary large objects) in filesystem


### Zope

- Zope is a web application framework that Plone runs on top of.
- Zope is written in Python, some performance-critical things are implemented in C.
- It serves applications that communicate with users via `http`.
- Plone 6 uses Zope 5.x


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

### CMF

- `CMF` was an add-on for Zope to build Content Management Systems (like Plone).
- It provides libraries for building content management applications together with the Zope Application Server.

### Plone (the backend)

This is the backend of the CMS.
This is what we are extending and using during this training.


### Rest API

{doc}`plone6docs:plone.restapi/docs/source/index`
is a hypermedia API to access Plone content using REST (Representational State Transfer).

It is used to connect the Volto frontend with Plone.


(volto-basics-label)=
### Volto Frontend

[Volto](https://github.com/plone/volto) is the default frontend for Plone 6 written in ReactJS.
It uses the Rest API to communicate with the backend and offers a modern editing experience.

Here are some basics that you need to understand if you are new to Volto:

- All data is stored in Plone backend.
  The Volto frontend comes in to display and edit the content.
- Volto is built in [ReactJS](https://www.reactjs.dev), a modern Javascript Framework.
- Volto uses {doc}`plone6docs:plone.restapi/docs/source/index` to communicate with the Plone backend.
- Volto is installed separately from the Plone backend.
  See chapter {ref}`instructions-install-frontend-label` for instructions.
- Volto runs in a different process than the Plone backend.
  By default Volto runs on port 3000. If you start Volto with `yarn start` you can see the frontend on <http://localhost:3000>.
  The Plone backend runs by default on <http://localhost:8080>
- You create a new Plone instance in an already set up Zope environment via the backend.
  This is by now not possible in Volto.
- Volto takes advantage of [Semantic UI React components](https://react.semantic-ui.com/) to compose most of the views.
  For example the component [Image](https://react.semantic-ui.com/elements/image/) is used to render images.
- The Volto default theme is based on Semantic UI theme and is called [Pastanaga](https://www.youtube.com/watch?v=wW9mTl1Tavc&t=133s).
- Same as Plone Classic, Volto is highly extendable with add-ons for further features.
- Existing Volto components are customizable with a technology similar to `z3c.jbot` called {ref}`volto-overrides-componentshadowing-label`.
- Volto provides server side rendering (SSR), important for SEO-purposes.
- Volto aims to provide 100% of the features of the current Plone backend.
  Not all features of Plone are implemented in Volto yet.
- Volto provides additional functionality that Plone does not have.
- For example Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks.
  This feature is enabled for content types that have the behavior `volto.blocks` enabled.
- Using the `Volto` editor, the content you add in blocks and the arrangement of blocks is stored as JSON in the schema fields `blocks` and `blocks_layout` provided by the dexterity behavior `volto.blocks`.
  Additionally you can edit all fields of the content type schema in a sidebar.
- If you do not use the behavior `volto.blocks`, the fields from a content-type schema are edited and stored exactly like previously in Plone Classic.


### Classic Frontend

A stable alternative to the `React` frontend Volto is the classic frontend of Plone that uses server-side rendered HTML.
Plone ships with a default theme called Barceloneta.
Since Plone 6 it uses [Bootstrap 5](https://getbootstrap.com/).
The Plone Classic frontend uses the template-engine [Chameleon](https://chameleon.readthedocs.io/en/latest/) to create html.


```{note} Choosing the right frontend

Here are some pointers that may help you decide:

- The new Plone 6 frontend is recommended for new projects.
- Existing projects that are updated to Plone 6 can decide which frontend to use.
  If a lot of customizations were done and you don't want to reimplement a lot of custom templates and features in Volto, it is a good idea to use Plone Classic.
- For a selection of awesome Volto add-ons see <https://github.com/collective/awesome-volto/>
- There are a growing ecosystem of add-ons for the React frontend.
  Be aware that a Plone Classic add-on may not have value for your project, if it has a theming component or anything that concerns the UI.
  That could be for example a backend add-on that implements the logic and storage of bookmarks.
  The UI needs to be implemented in React, be it an open source add-on or your custom add-on.
  Both, frontend and backend, communicate via REST API.
- Most existing add-ons for Plone will have to be adapted to Volto if they touch the UI (e.g. templates for content types, control panels or viewlets).
- Ask the community for advice if you are not certain what to choose.
```