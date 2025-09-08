---
myst:
  html_meta:
    "description": "The Anatomy of Plone"
    "property=og:description": "The Anatomy of Plone"
    "property=og:title": "The Anatomy of Plone"
    "keywords": "history, Plone, ZODB, CMF, Zope, Pyramid, Bluebream"
---

(plone5-anatomy-label)=

# The Anatomy of Plone

In this part you will:

- Learn a bit about the history of Plone.

Topics covered:

- ZODB
- CMF
- Zope
- Pyramid
- Bluebream

Plone started as an extension for CMF, which is a extension for Zope. Python, ZODB, Zope, CMF, Plone ... -- how does all that fit together?

## Database

- [ZODB](https://zodb.org/en/latest/): A native object database for Python

  - No separate language for database operations
  - Very little impact on your code to make objects persistent
  - Object database != ORM
  - almost no seam between code and database.

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

(plone5-anatomy-zope2-label)=

## Zope

- Zope is a web application framework that Plone runs on top of.
- The majority of Zope's code is written in Python, like everything else written on top of it.
- It serves applications that communicate with users via http.

```{note}
**The great Version-Confusion**

- Plone was always based on Zope 2.x. Starting with Plone 5.2+ it uses Zope 4.x
- Starting with Zope 4.0, the package is only called Zope (not Zope2 or Zope4)
- *Zope 3* is **not** a version of Zope but an ill-named rewrite of Zope 2 *(sigh)*
- 4.x is a major new release of Zope that supports Python 3 (among many other improvements)
```

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

```{note}
**Acquisition**

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

(plone5-anatomy-cmf-label)=

## Content Management Framework

- [CMF (Content Management Framework)](https://old.zope.dev/Products/CMF/index.html/) is add-on for Zope to build Content Management Systems (like Plone).

```{only} not presentation
After many websites were successfully created using Zope, a number of recurring requirements emerged,
and some Zope developers started to write CMF, the Content Management Framework.

The CMF offers many services that help you to write a CMS based on Zope.
Most objects you see in the ZMI are part of the CMF somehow.

The developers behind CMF do not see CMF as a ready to use CMS.
They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

We are still in prehistoric times here. There were no eggs (Python packages),
Zope did not consist of 100 independent software components but was one big file set.

Many parts of Plone are derived from the CMF, but it's a mixed heritage.
The CMF is an independent software project, and has often moved more slowly than Plone.

Plone is gradually eliminating dependence on most parts of the CMF.
```

(plone5-anatomy-ztk-label)=

## Zope Toolkit / Zope3

- Zope 3 was originally intended as a rewrite of Zope from the ground up.
- Plone uses parts of it provided by the [Zope Toolkit (ZTK)](https://zopetoolkit.readthedocs.io/en/latest/).
- The name was very unfortunate since it was in no way compatible with Zope 2

```{only} not presentation
Unfortunately, only few people started to use Zope 3, nobody migrated to Zope 3 because nobody knew how.

But there were many useful things in Zope 3 that people wanted to use in Zope 2,
thus the Zope community adapted some parts so that they could use them in Zope 2.

Sometimes, a wrapper of some sort was necessary, these usually are being provided by packages
from the {py:mod}`five` namespace.  (Zope 2 + Zope 3 = "five")

To make the history complete, since people stayed on Zope 2, the Zope community renamed Zope 3 to Bluebream,
so that people would not think that Zope 3 was the future.

It wasn't anymore.
```

(plone5-anatomy-zca-label)=

## Zope Component Architecture (ZCA)

The [Zope Component Architecture](https://zopecomponent.readthedocs.io/en/latest/), which was developed as part of Zope 3,
is a system which allows for component pluggability and complex dispatching based on objects
which implement an interface (a description of a functionality).

It is a subset of the ZTK but can be used standalone.
Plone makes extensive use of the ZCA in its codebase.

(plone5-anatomy-pyramid-label)=

## Pyramid

- [Pyramid](https://trypyramid.com) is a Python web application development framework that is often seen as the successor to Zope.
- It does less than Zope, is very pluggable and [uses the Zope Component Architecture](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/zca.html) “under the hood” to perform view dispatching and other application configuration tasks.

````{only} not presentation
You can use it with a relational Database instead of ZODB if you want, or you can use both databases or none of them.

Apart from the fact that Pyramid was not forced to support all legacy functionality,
which can make things more complicated, the original developer had a very different stance on how software must be developed.
While both Zope and Pyramid have good test coverage, Pyramid has good documentation; something that was very neglected in Zope,
and at times in Plone too.

Whether the component architecture is better in Pyramid or not we don't dare say,
but we like it more. But maybe it's just because it was documented.

```{seealso}
- <https://docs.pylonsproject.org/projects/pyramid/en/latest/index.html>
```
````

## Exercise

Definition of the PYTHON_PATH makes up most of the `bin/instance` script's code.
Look at the package list (and maybe also the links provided in the respective sections of this chapter).
Try to identify 3 packages that belong to Zope 4, 3 packages from CMF, 3 Zope Toolkit packages and 3 packages from the ZCA.

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

- Zope 4: Zope, ZODB, Acquisition, AccessControl, ...
- CMF: Products.CMFCore, Products.CMFUid, Products.CMFEditions, ... Products.DCWorkflow doesn't fit the pattern but is a very important part of the CMF
- ZTK: zope.browser, zope.container, zope.pagetemplate, ... You can find a complete list [here](https://dist.plone.org/versions/zopetoolkit-1-0-8-zopeapp-versions.cfg)
- ZCA: zope.component, zope.interface, zope.event
```
