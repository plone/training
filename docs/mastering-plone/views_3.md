---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(views3-label)=

# Views III: A Talk List

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout views_2
```

Code for the end of this chapter:

```shell
git checkout views_3
```
````

In this part you will:

- Write a Python class to get all talks from the catalog
- Write a template to display the talks
- Improve the table

Topics covered:

- BrowserView
- plone.api
- catalog: portal_catalog
- brains and objects
- Acquisition

Now we don't want to provide information about one specific item but on several items. What now? We can't look at several items at the same time as context.

(views3-catalog-label)=

## Using the catalog

Let's say we want to show a list of all the talks that were submitted for our conference. We can just go to the folder and select a display method that suits us. But none does because we want to show the target audience in our listing.

So we need to get all the talks. For this we use the Python class of the view to query the catalog for the talks.

The catalog is like a search engine for the content on our site. It holds information about all the objects as well as some of their attributes like title, description, workflow_state, keywords that they were tagged with, author, content_type, its path in the site etc. But it does not hold the content of "heavy" fields like images or files, richtext fields and fields that we just defined ourselves.

It is the fast way to get content that exists in the site and do something with it. From the results of the catalog we can get the objects themselves but often we don't need them, but only the properties that the results already have.

`browser/configure.zcml`

```{code-block} xml
:linenos:

<browser:page
   name="talklistview"
   for="*"
   layer="zope.interface.Interface"
   class=".views.TalkListView"
   template="templates/talklistview.pt"
   permission="zope2.View"
   />
```

`browser/views.py`

```{code-block} python
:emphasize-lines: 2, 7-26
:linenos:

from Products.Five.browser import BrowserView
from plone import api
from plone.dexterity.browser.view import DefaultView

[...]

class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        results = []
        brains = api.content.find(context=self.context, portal_type='talk')
        for brain in brains:
            talk = brain.getObject()
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'audience': ', '.join(talk.audience),
                'type_of_talk': talk.type_of_talk,
                'speaker': talk.speaker,
                'room': talk.room,
                'uuid': brain.UID,
                })
        return results
```

We query the catalog with two parameters. The catalog returns only items for which **both** apply:

- `context=self.context`
- `portal_type='talk'`

We pass a object as `context` to query only for content in the current path. Otherwise we'd get all talks in the whole site. If we moved some talks to a different part of the site (e.g. a sub-conference for universities with a special talk list) we might not want so see them in our listing. We also query for the `portal_type` so we only find talks.

````{note}
We use the method {py:meth}`find` in {py:mod}`plone.api` to query the catalog. It is one of many convenience-methods provided as a wrapper around otherwise more complex api's. If you query the catalog direcly you'd have to first get the catalog, and pass it the path for which you want to find items:

```python
portal_catalog = api.portal.get_tool('portal_catalog')
current_path = '/'.join(self.context.getPhysicalPath())
brains = portal_catalog(path=current_path, portal_type='talk')
```
````

We iterate over the list of results that the catalog returns.

We create a dictionary that holds all the information we want to show in the template. This way we don't have to put any complex logic into the template.

(views3-brains-label)=

## brains and objects

Objects are normally not loaded into memory but lie dormant in the ZODB database. Waking objects up can be slow, especially if you're waking up a lot of objects. Fortunately our talks are not especially heavy since they are:

- Dexterity objects which are lighter than their Archetypes brothers
- relatively few since we don't have thousands of talks at our conference

We want to show the target audience but that attribute of the talk content type is not in the catalog. This is why we need to get to the objects themselves.

We could also add a new index to the catalog that will add 'audience' to the properties of brains, but we should weigh the pros and cons:

- talks are important and thus most likely always in memory
- prevent bloating of catalog with indexes

````{note}
The code to add such an index would look like this:

```
from plone.indexer.decorator import indexer
from ploneconf.site.talk import ITalk

@indexer(ITalk)
def talk_audience(object, **kw):
     return object.audience
```

We'd have to register this factory function as a named adapter in the {file}`configure.zcml`. Assuming you've put the code above into a file named {file}`indexers.py`

```xml
<adapter name="audience" factory=".indexers.talk_audience" />
```

We will add some indexers later on.
````

Why use the catalog at all? It checks for permissions, and only returns the talks that the current user may see. They might be private or hidden to you since they are part of a top secret conference for core developers (there is no such thing!).

Most objects in Plone act like dictionaries, so you can do {py:meth}`context.values()` to get all its contents.

For historical reasons some attributes of brains and objects are written differently.

```pycon
>>> obj = brain.getObject()

>>> obj.title
u'Talk submission is open!'

>>> brain.Title == obj.title
True

>>> brain.title == obj.title
False
```

Who can guess what {py:attr}`brain.title` will return since the brain has no such attribute?

````{only} not presentation
```{note}
Answer: Acquisition will get the attribute from the nearest parent. `brain.__parent__` is `<CatalogTool at /Plone/portal_catalog>`. The attribute `title` of the `portal_catalog` is 'Indexes all content in the site'.
```
````

Acquisition can be harmful. Brains have no attribute 'getLayout' {py:meth}`brain.getLayout()`:

```pycon
>>> brain.getLayout()
'folder_listing'

>>> obj.getLayout()
'newsitem_view'

>>> brain.getLayout
<bound method PloneSite.getLayout of <PloneSite at /Plone>>
```

The same is true for methods:

```pycon
>>> obj.absolute_url()
'http://localhost:8080/Plone/news/talk-submission-is-open'
>>> brain.getURL() == obj.absolute_url()
True
>>> brain.getPath() == '/'.join(obj.getPhysicalPath())
True
```

(views3-querying-label)=

## Querying the catalog

The are many [catalog indexes](https://5.docs.plone.org/develop/plone/searching_and_indexing/indexing.html) to query. Here are some examples:

```pycon
>>> portal_catalog = getToolByName(self.context, 'portal_catalog')
>>> portal_catalog(Subject=('cats', 'dogs'))
[]
>>> portal_catalog(review_state='pending')
[]
```

Calling the catalog without parameters returns the whole site:

```pycon
>>> portal_catalog()
[<Products.ZCatalog.Catalog.mybrains object at 0x1085a11f0>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a12c0>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a1328>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a13 ...
```

```{seealso}
<https://5.docs.plone.org/develop/plone/searching_and_indexing/query.html>
```

(views3-excercises-label)=

## Exercises

Since you now know how to query the catalog it is time for some exercise.

### Exercise 1

Add a method {py:meth}`get_news` to {py:class}`TalkListView` that returns a list of brains of all News Items that are published and sort them in the order of their publishing date.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} python
:linenos:

def get_news(self):

    portal_catalog = api.portal.get_tool('portal_catalog')
    return portal_catalog(
        portal_type='News Item',
        review_state='published',
        sort_on='effective',
    )
```
````

### Exercise 2

Add a method that returns all published keynotes as objects.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} python
:linenos:

def keynotes(self):

    portal_catalog = api.portal.get_tool('portal_catalog')
    brains = portal_catalog(
        portal_type='talk',
        review_state='published')
    results = []
    for brain in brains:
        # There is no catalog index for type_of_talk so we must check
        # the objects themselves.
        talk = brain.getObject()
        if talk.type_of_talk == 'Keynote':
            results.append(talk)
    return results
```
````

(views3-template-listing-label)=

## The template for the listing

Next you create a template in which you use the results of the method 'talks'.

Try to keep logic mostly in Python. This is for two\* reasons (and by "two", we mean "three"):

Readability:

: It's much easier to read Python than complex TAL structures

Speed:

: Python code is faster than code executed in templates. It's also easy to add caching to methods.

DRY, or "Don't Repeat Yourself":

: In Python you can reuse methods and easily refactor code. Refactoring TAL usually means having to do big changes in the HTML structure which results in incomprehensible diffs.

The MVC schema does not directly apply to Plone but look at it like this:

Model:

: the object

View:

: the template

Controller:

: the view

The view and the controller are very much mixed in Plone. Especially when you look at some of the older code of Plone you'll see that the policy of keeping logic in Python and representation in templates was not always enforced.

But you should nevertheless do it! You'll end up with more than enough logic in the templates anyway.

Add this simple table to {file}`templates/talklistview.pt`:

```{code-block} html
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
  <metal:content-core fill-slot="content-core">
  <table class="listing"
         id="talks"
         tal:define="talks python:view.talks()">
    <thead>
      <tr>
        <th>Title</th>
        <th>Speaker</th>
        <th>Audience</th>
      </tr>
    </thead>
    <tbody>
      <tr tal:repeat="talk talks">
        <td>
          <a href=""
             tal:attributes="href python:talk['url'];
                             title python:talk['description']"
             tal:content="python:talk['title']">
             The 7 sins of Plone development
          </a>
        </td>
        <td tal:content="python:talk['speaker']">
            Philip Bauer
        </td>
        <td tal:content="python:talk['audience']">
            Advanced
        </td>
        <td tal:content="python:talk['room']">
            101
        </td>
      </tr>
      <tr tal:condition="python: not talks">
        <td colspan=4>
            No talks so far :-(
        </td>
      </tr>
    </tbody>
  </table>

  </metal:content-core>
</body>
</html>
```

Again we use `class="listing"` to give the table a nice style.

There are some things that need explanation:

{samp}`tal:define="talks python:view.talks()"`

: This defines the variable `talks`.
We do this since we reuse it later and don't want to call the same method twice.
Since TAL's path expressions for the lookup of values in dictionaries is the same as for the attributes of objects and methods of classes we can write {samp}`view/talks` as we could {samp}`view/someattribute`.
Handy but sometimes irritating since from looking at the page template alone we often have no way of knowing if something is an attribute, a method or the value of a dict.

{samp}`tal:repeat="talk talks"`

: This iterates over the list of dictionaries returned by the view. Each {py:obj}`talk` is one of the dictionaries that are returned by this method.

{samp}`tal:content="python:talk['speaker']"`

: 'speaker' is a key in the dict 'talk'. We could also write {samp}`tal:content="talk/speaker"`

{samp}`tal:condition="python: not talks"`

: This is a fallback if no talks are returned. It then returns an empty list (remember {samp}`results = []`?)

### Exercise

Modify the view to only use path expressions.
This is **not** best practice but there is plenty of code in Plone and in add-ons so you have to know how to use them.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
  <metal:content-core fill-slot="content-core">
  <table class="listing" id="talks"
         tal:define="talks view/talks">
    <thead>
      <tr>
        <th>Title</th>
        <th>Speaker</th>
        <th>Audience</th>
      </tr>
    </thead>
    <tbody>
      <tr tal:repeat="talk talks">
        <td>
          <a href=""
             tal:attributes="href talk/url;
                             title talk/description"
             tal:content="talk/title">
             The 7 sins of Plone development
          </a>
        </td>
        <td tal:content="talk/speaker">
            Philip Bauer
        </td>
        <td tal:content="talk/audience">
            Advanced
        </td>
      </tr>
      <tr tal:condition="not:talks">
        <td colspan=3>
            No talks so far :-(
        </td>
      </tr>
    </tbody>
  </table>

  </metal:content-core>
</body>
</html>
```
````

(views3-custom-label)=

## Setting a custom view as default view on an object

We don't want to always have to append {samp}`/@@talklistview` to our folder to get the view. There is a very easy way to set the view to the folder using the ZMI.

If we append {samp}`/manage_propertiesForm` we can set the property "layout" to {samp}`talklistview`.

To make views configurable so that editors can choose them we have to register the view for the content type at hand in its FTI. To enable it for all folders we add a new file {file}`profiles/default/types/Folder.xml`

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<object name="Folder">
 <property name="view_methods" purge="False">
  <element value="talklistview"/>
 </property>
</object>
```

After re-applying the typeinfo profile of our add-on (or simply reinstalling it) the content type "Folder" is extended with our additional view method and appears in the display dropdown.

The {samp}`purge="False"` appends the view to the already existing ones instead of replacing them.

(views3-summary-label)=

## Summary

- You created a nice listing, that can be called at any place in the website
- You wrote your first fully grown BrowserView that combines a template, a class and a method in that class
- You learned about portal_catalog, brains and how they are related to objects
- You learned about acquisition and how it can have unintended effects
- You extended the FTI of an existing content type to allow editors to configure the new view as default
