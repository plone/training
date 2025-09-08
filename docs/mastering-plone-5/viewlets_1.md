---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-viewlets1-label)=

# Writing Viewlets

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout behaviors_1
```

Code for the end of this chapter:

```shell
git checkout viewlets_1
```

{doc}`code`
````

In this part you will:

- Display data from a behavior in a viewlet

Topics covered:

- Viewlets

(plone5-viewlets1-featured-label)=

## A viewlet for the featured behavior

```{only} not presentation
A viewlet is not a view but a snippet of HTML and logic that can be put in various places in the site.
These places are called `viewletmanager`.
```

- Inspect existing viewlets and their managers by going to http://localhost:8080/Plone/@@manage-viewlets.
- We already customized a viewlet ({file}`colophon.pt`). Now we add a new one.
- Viewlets don't save data (portlets do)
- Viewlets have no user interface (portlets do)

(plone5-viewlets1-featured2-label)=

## Featured viewlet

```{only} not presentation
Let's add a link to the site that uses the information that we collected using the featured behavior.
```

We register the viewlet in {file}`browser/configure.zcml`.

```{code-block} xml
:linenos:

<browser:viewlet
    name="featured"
    for="ploneconf.site.behaviors.featured.IFeatured"
    manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
    class=".viewlets.FeaturedViewlet"
    layer="zope.interface.Interface"
    template="templates/featured_viewlet.pt"
    permission="zope2.View"
    />
```

`for`, `manager`, `layer` and `permission` are constraints that limit the contexts in which the viewlet is loaded and rendered,
by filtering out all the contexts that do not match those constraints.

```{only} not presentation
This registers a viewlet called `featured`.
It is visible on all content that implements the interface {py:class}`IFeatured` from our behavior.
It is also good practice to bind it to a specific `layer`, so it only shows up if our add-on is actually installed.
We will return to this in a later chapter.
```

The viewlet class {py:class}`FeaturedViewlet` is expected in a file {file}`browser/viewlets.py`.

```{code-block} python
:linenos:

from plone.app.layout.viewlets import ViewletBase

class FeaturedViewlet(ViewletBase):
    pass
```

```{only} not presentation
This class does nothing except rendering the associated template (That we have yet to write)
```

Let's add the missing template {file}`templates/featured_viewlet.pt`.

```{code-block} html
:linenos:

<div id="featured">
    <p tal:condition="python:view.is_featured">
        This is hot news!
    </p>
</div>
```

```{only} not presentation
As you can see this is not a valid HTML document.
That is not needed, because we don't want a complete view here, a HTML snippet is enough.

There is a {samp}`tal:define` statement, querying for {samp}`view/is_featured`.
Same as for views, viewlets have access to their class in page templates, as well.
```

We have to extend the Featured Viewlet now to add the missing attribute:

```{code-block} python
:emphasize-lines: 2, 6-8
:linenos:

from plone.app.layout.viewlets import ViewletBase
from ploneconf.site.behaviors.featured import IFeatured

class FeaturedViewlet(ViewletBase):

    def is_featured(self):
        adapted = IFeatured(self.context)
        return adapted.featured
```

So far, we

> - register the viewlet to content that has the IFeatured Interface.
> - adapt the object to its behavior to be able to access the fields of the behavior
> - return the link

````{only} not presentation
```{note}
**Why not to access context directly**

In this example, {samp}`IFeatured(self.context)` does return the context directly.
It is still good to use this idiom for two reasons:

> 1. It makes it clear that we only want to use the IFeatured aspect of the object
> 2. If we decide to use a factory, for example to store our attributes in an annotation, we would `not` get back our context, but the adapter.

Therefore in this example you could simply write {samp}`return self.context.featured`.
```
````

(plone5-viewlets1-excercises-label)=

## Exercise 1

Register a viewlet 'number_of_talks' in the footer that is only visible to admins (the permission you are looking for is {py:class}`cmf.ManagePortal`).
Use only a template (no class) to display the number of talks already submitted.

Hint: Use Acquisition to get the catalog (You know, you should not do this but there is plenty of code out there that does it...)

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Register the viewlet in {file}`browser/configure.zcml`

```xml
<browser:viewlet
  name="number_of_talks"
  for="*"
  manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
  layer="zope.interface.Interface"
  template="templates/number_of_talks.pt"
  permission="cmf.ManagePortal"
  />
```

For the `for` and `layer`-parameters `*` is shorthand for {py:class}`zope.interface.Interface` and the same effect as omitting them: The viewlet will be shown for all types of pages and for all Plone sites within your Zope instance.

Add the template {file}`browser/templates/number_of_talks.pt`:

```html
<div class="number_of_talks"
     tal:define="catalog python:context.portal_catalog;
                 number_of_talks python:len(catalog(portal_type='talk'));">
    There are <span tal:replace="number_of_talks" /> talks.
</div>
```

{samp}`python:context.portal_catalog` will return the catalog through Acquisition. Be careful if you want to use path expressions: {samp}`context/portal_catalog` calls the catalog (and returns all brains). You need to prevent this by using {samp}`nocall:context/portal_catalog`.

Relying on Acquisition is a bad idea. It would be much better to use the helper view `plone_tools` from {file}`plone/app/layout/globals/tools.py` to get the catalog.

```html
<div class="number_of_talks"
     tal:define="catalog context/@@plone_tools/catalog;
                 number_of_talks python:len(catalog(portal_type='talk', review_state='pending'));">
    There are <span tal:replace="number_of_talks" /> talks.
</div>
```

{samp}`context/@@plone_tools/catalog` traverses to the view `plone_tools` and calls its method {py:meth}`catalog`. In python it would look like this:

```html
<div class="number_of_talks"
     tal:define="catalog python:context.restrictedTraverse('plone_tools').catalog();
                 number_of_talks python:len(catalog(portal_type='talk'));">
    There are <span tal:replace="number_of_talks" /> talks.
</div>
```

It is not a good practice to query the catalog within a template since even simple logic like this should live in Python.
But it is very powerful if you are debugging or need a quick and dirty solution.

In Plone 5 you could even write it like this:

```html
<?python

from plone import api
catalog = api.portal.get_tool('portal_catalog')
number_of_talks = len(catalog(portal_type='talk'))

?>

<div class="number_of_talks">
    There are ${python:number_of_talks} talks.
</div>
```
````

## Exercise 2

Register a viewlet 'days_to_conference' in the header.
Use a class and a template to display the number of days until the conference.

You get bonus points if you display it in a nice format (think "In 2 days" and "Last Month") by using either JavaScript or a Python library.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

In {file}`configure.zcml`:

```xml
<browser:viewlet
  name="days_to_conference"
  for="*"
  manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
  layer="*"
  class=".viewlets.DaysToConferenceViewlet"
  template="templates/days_to_conference.pt"
  permission="zope2.View"
  />
```

In {file}`viewlets.py`:

```python
from plone.app.layout.viewlets import ViewletBase
from datetime import datetime
import arrow

CONFERENCE_START_DATE = datetime(2015, 10, 12)


class DaysToConferenceViewlet(ViewletBase):

    def date(self):
        return CONFERENCE_START_DATE

    def human(self):
        return arrow.get(CONFERENCE_START_DATE).humanize()
```

Setting the date in python is not very user-friendly. In the chapter {ref}`plone5-registry-label` you learn how store global configuration and easily create control panels.

And in {file}`templates/days_to_conference.pt`:

```html
<div class="days_to_conf">
    ${python: view.human()}
</div>
```

Or using the moment pattern in Plone 5:

```html
<div class="pat-moment"
     data-pat-moment="format: relative">
    ${python: view.date()}
</div>
```
````

[plone5_browserlayer]: https://5.docs.plone.org/develop/plone/views/layers.html?highlight=browserlayer#introduction
