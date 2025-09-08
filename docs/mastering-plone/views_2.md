---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(views2-label)=

# Views II: A Default View for "Talk"

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

Solve the same tasks in the React frontend in chapter {doc}`volto_talkview`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout zpt_2
```

Code for the end of this chapter:

```shell
git checkout views_2
```
````

In this part you will:

- Register a view with a Python class
- Write a template used in the default view for talks

Topics covered:

- View classes
- BrowserView and DefaultView
- displaying data from fields

(views2-classes-label)=

## View Classes

Earlier we wrote a demo view which we also used to experiment with page templates.
Now we are going to enhance that view so that it will have some Python code, in addition to a template.
Let us have a look at the ZCML and the code.

`browser/configure.zcml`

```{code-block} xml
:emphasize-lines: 8
:linenos:

<configure xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    i18n_domain="ploneconf.site">

    <browser:page
       name="training"
       for="*"
       class=".views.DemoView"
       template="templates/training.pt"
       permission="zope2.View"
       />

</configure>
```

We are adding a file called {file}`views.py` in the {file}`browser` folder.

{file}`browser/views.py`

```{code-block} python
:linenos:

from Products.Five.browser import BrowserView

class DemoView(BrowserView):

    def the_title(self):
        return u'A list of great trainings:'
```

In the template {file}`training.pt` we can now use this view as `view` and access all its methods and properties:

```html
<h2 tal:content="python: view.the_title()" />
```

The logic contained in the template can now be moved to the class:

```{code-block} python
:emphasize-lines: 3, 12-36
:linenos:

# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from operator import itemgetter


class DemoView(BrowserView):
    """A demo listing"""

    def the_title(self):
        return u'A list of talks:'

    def talks(self):
        results = []
        data = [
            {'title': 'Dexterity is the new default!',
             'subjects': ('content-types', 'dexterity')},
            {'title': 'Mosaic will be the next big thing.',
             'subjects': ('layout', 'deco', 'views'),
             'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
            {'title': 'The State of Plone',
             'subjects': ('keynote',)},
            {'title': 'Diazo is a powerful tool for theming!',
             'subjects': ('design', 'diazo', 'xslt')},
            {'title': 'Magic templates in Plone 5',
             'subjects': ('templates', 'TAL'),
             'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'},
        ]
        for item in data:
            url = item.get('url', 'https://www.google.com/search?q={}'.format(item['title']))
            talk = {
                'title': item['title'],
                'subjects': ', '.join(item['subjects']),
                'url': url
                }
            results.append(talk)
        return sorted(results, key=itemgetter('title'))
```

And the template will now be much simpler.

```{code-block} html
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>

<metal:content-core fill-slot="content-core">

<h2 tal:content="python: view.the_title()" />

<table class="listing">
    <tr>
        <th>Title</th>
        <th>Topics</th>
    </tr>

    <tr tal:repeat="talk python:view.talks()">
        <td>
            <a href="${python:talk['url']}">
                ${python:talk['title']}
            </a>
        </td>
        <td>
            ${python:talk['subjects']}
        </td>
    </tr>
</table>

</metal:content-core>

</body>
</html>
```

```{note}
It is a very common pattern that you prepare the data you want to display in Python.
```

## Browser Views

In the next example you will access the `context` in which the view is called.

Edit `browser/views.py` and add a method `context_info` to the view `DemoView` that returns information on the context.

In a method of a Browser View the content object which was `context` in the template is now accessed as `self.context`.

```{code-block} python
:linenos:

def context_info(self):
    context = self.context
    title = context.title
    portal_type = context.portal_type
    url = context.absolute_url()
    return u"This is the {0} '{1}' at {2}".format(portal_type, title, url)
```

````{note}
The result is the same as in {ref}`python-expressions-label` where you wrote
```html
<p tal:content="python: 'This is the {0} {1} at {2}'.format(context.portal_type, context.title, context.absolute_url()">
</p>
```
in the template.
````

The template {file}`training.pt` still needs to display that:

```{code-block} xml
:linenos:

<p tal:content="python: view.context_info()">
    Info on the context
</p>
```

Open the view on a talk and it will show you information on that talk.

```{note}
Changes in Python files are picked up by restarting Plone or using the add-on `plone.reload`: <http://localhost:8080/@@reload>
```

## Reusing Browser Views

- Browser Views can be called by accessing their name in the browser.
  Append `/training` to any URL and the view will be called.
- Browser Views can be associated with a template (like `training.pt`) to return some HTML.
- Browser Views can be reused in your code using `plone.api.content.get_view('<name of the view>', context, request)`.
  This allows you to reuse code and methods.

The method `context_info` that returned information on the current object can be reused any time like this:

```{code-block} python
:linenos:

from Products.Five.browser import BrowserView
from plone import api

class SomeOtherView(BrowserView):

    def __call__(self):
        training_view = api.content.get_view('training', self.context, self.request)
        return training_view.context_info()
```

You would still need to register the view in configure.zcml:

```{code-block} xml
:linenos:

<browser:page
    name="some_view"
    for="*"
    class=".views.SomeOtherView"
    permission="zope2.View"
    />
```

Using `/some_view` would now return infomation of the current object in the browser without a template.

You can define which `context`-object should be used:

```{code-block} python
:linenos:

from Products.Five.browser import BrowserView
from plone import api

class SomeOtherView(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        some_talk = portal['dexterity-for-the-win']
        training_view = api.content.get_view('training', some_talk, self.request)
        return training_view.context_info()
```

`typeinfo` will now be "This is the talk 'Dexterity for the win' at <http://localhost:8080/Plone/dexterity-for-the-win>"

```{note}
Browser Views

- are the Swiss Army knife of every Plone developer
- can be called by appending their name to a URL in the browser.
  Append `/training` to any URL and the view will be called.
- can be associated with a template (like `training.pt`) to return some HTML.
- can be reused in your code using `plone.api.content.get_view('<name of the view>', context, request)`.
- can be protected with permissions
- can be constrained to certain content types by using `for="plonconf.site.content.sponsor.ISponsor"`
- can be constrained to certain addons by using `layer="plonconf.site.interfaces.IPloneconfSiteLayer"`
```

(views2-default-label)=

## The default view

Now you know everything to create a nice view for talks in {file}`views.py`.

First we will not write any methods for `view` but access the fields from the talk schema as `context.<fieldname>`.

Register a view `talkview` in {file}`browser/configure.zcml`:

```{code-block} xml
:linenos:

<browser:page
   name="talkview"
   for="*"
   layer="zope.interface.Interface"
   class=".views.TalkView"
   template="templates/talkview.pt"
   permission="zope2.View"
   />
```

{file}`browser/views.py`

```{code-block} python
:linenos:

class TalkView(BrowserView):
    """ The default view for talks"""
```

Add the template {file}`templates/talkview.pt`:

```{code-block} xml
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    lang="en"
    metal:use-macro="context/main_template/macros/master"
    i18n:domain="ploneconf.site">
<body>
    <metal:content-core fill-slot="content-core">
        <p>Suitable for <em tal:content="python: ', '.join(context.audience)"></em>
        </p>

        <div tal:condition="python: context.details"
             tal:content="structure python: context.details.output" />

        <div tal:content="python: context.speaker">
            User
        </div>
    </metal:content-core>
</body>
</html>
```

After a restart, we can test our view by going to a talk and adding _/talkview_ to the URL.

## Using helper methods from {py:class}`DefaultView`

In the previous section we used {py:class}`BrowserView` as the base class for {py:class}`TalkView`.

Dexterity comes with a nice helper class suited for views of content types: the {py:class}`DefaultView` base class in {py:mod}`plone.dexterity`.
It has some very useful properties available to use in the template:

- {py:attr}`view.w` is a dictionary of all the display widgets, keyed by field names. This includes widgets from alternative fieldsets.
- {py:attr}`view.widgets` contains a list of widgets in schema order for the default fieldset.
- {py:attr}`view.groups` contains a list of fieldsets in fieldset order.
- {py:attr}`view.fieldsets` contains a dict mapping fieldset name to fieldset
- On a fieldset (group), you can access a widget list to get widgets in that fieldset

You can now change the {py:class}`TalkView` to use it

```{code-block} python
:linenos:

from plone.dexterity.browser.view import DefaultView

...

class TalkView(DefaultView):
    """ The default view for talks
    """
```

The template {file}`templates/talkview.pt` still works but now you can modify it
to use the pattern {samp}`view/w/<fieldname>/render` to render the widgets:

```{code-block} xml
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    lang="en"
    metal:use-macro="context/main_template/macros/master"
    i18n:domain="ploneconf.site">
<body>
    <metal:content-core fill-slot="content-core">
        <p>Suitable for <em tal:replace="structure view/w/audience/render"></em>
        </p>

        <div tal:content="structure view/w/details/render" />

        <div tal:content="python: context.speaker">
            User
        </div>
    </metal:content-core>
</body>
</html>
```

After a restart, we can test the modified view by going to a talk and adding `/talkview` to the URL.

We should tell Plone that the talkview should be used as the default view for talks instead of the built-in view.

This is a configuration that you can change during runtime and is stored in the database, as such it is also managed by GenericSetup profiles.

open {file}`profiles/default/types/talk.xml`:

```{code-block} xml
:emphasize-lines: 2,4
:linenos:

...
<property name="default_view">talkview</property>
<property name="view_methods">
    <element value="talkview"/>
    <element value="view"/>
</property>
...
```

We will have to either reinstall our add-on or run the GenericSetup import step `typeinfo` so Plone learns about the change.

```{note}
To change it TTW go to the ZMI (<http://localhost:8080/Plone/manage>), go to `portal_types` and select the type for which the new view should be selectable (*talk*).

Now add `talkview` to the list *Available view methods*.
Now the new view is available in the menu *Display*.
To make it the default view enter it in `Default view method`.
```

## The complete template for talks

Now you can improve the talkview to show data for all fields in the talk schema:

- type_of_talk
- details
- audience
- room
- speaker
- email
- image
- speaker_biography

Since we will use the macro `content-core` the values for `title` and `description` of the talk will be rendered for us and we do not have to deal with them.

{file}`templates/talkview.pt`:

```{code-block} xml
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
    <metal:content-core fill-slot="content-core">

        <p>
            <span tal:content="python:context.type_of_talk">
                Talk
            </span>
            suitable for
            <span tal:replace="structure view/w/audience/render">
                Audience
            </span>
        </p>

        <p tal:content="structure view/w/room/render">
            Room
        </p>

        <div tal:content="structure view/w/details/render">
            Details
        </div>

        <div class="newsImageContainer">
            <img tal:condition="python:getattr(context, 'image', None)"
                 tal:attributes="src python:context.absolute_url() + '/@@images/image/thumb'" />
        </div>

        <div>
            <a class="email-link" tal:attributes="href python:'mailto:' + context.email">
                <strong tal:content="python: context.speaker">
                    Jane Doe
                </strong>
            </a>
            <div tal:content="structure view/w/speaker_biography/render">
                Biography
            </div>
        </div>

    </metal:content-core>
</body>
</html>
```

````{note}
If you want to customize the rendering of `title` and `description` simply use the macro `main` and add your own version to your template.
The default rendering is defined in {py:mod}`Products.CMFPlone` in {file}`/Products/CMFPlone/browser/templates/main_template.pt`.

```xml
<header>
  <div id="viewlet-above-content-title" tal:content="structure provider:plone.abovecontenttitle" />
  <metal:title define-slot="content-title">
      <h1 class="documentFirstHeading"
          tal:define="title context/Title"
          tal:condition="title"
          tal:content="title">Title or id</h1>
  </metal:title>
  <div id="viewlet-below-content-title" tal:content="structure provider:plone.belowcontenttitle" />

  <metal:description define-slot="content-description">
      <div class="documentDescription description"
           tal:define="description context/Description"
           tal:content="description"
           tal:condition="description">
          Description
      </div>
  </metal:description>
</header>
```

Note that both `title` and `description` are wrapped in `slots` and can be overwritten like this example:

```xml
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>

<metal:foo fill-slot="content-title">
  <h1 class="documentFirstHeading">
    <span tal:replace="python:context.title" />
    (<span class="pat-moment"
           data-pat-moment="format:relative"
           tal:content="python:context.Date()">
    </span>)
  </h1>
</metal:foo>

<metal:content-core fill-slot="content-core">
    [...]
</metal:content-core>

</body>
</html>
```

Since in `DefaultView` you have access to the widget you can also use other information, like `label` which is the title of the field: `<label tal:content="view/w/room/label"></label>`.
One benefit of this approach is that you automatically get the translated title.
This is used in the default-view for dexterity content `plone/dexterity/browser/item.pt`.
````

## Behind the scenes

```{code-block} python
:linenos:

from Products.Five.browser import BrowserView

class DemoView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # Implement your own actions

        # This renders the template that was registered in zcml like this:
        #   template="templates/training.pt"
        return super(DemoView, self).__call__()
        # If you don't register a template in zcml the Superclass of
        # DemoView will have no __call__-method!
        # In that case you have to call the template like this:
        # from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
        # class DemoView(BrowserView):
        # template = ViewPageTemplateFile('templates/training.pt')
        # def __call__(self):
        #    return self.template()
```

Do you remember the term {py:class}`MultiAdapter`?

The BrowserView is just a MultiAdapter.
The ZCML statement {samp}`browser:page` registers a {py:class}`MultiAdapter` and adds additional things needed for a browser view.

An adapter adapts things, a {py:class}`MultiAdapter` adapts multiple things.

When you enter a URL, Zope tries to find an object for it.
At the end, when Zope does not find any more objects but there is still a path item left,
or there are no more path items, Zope looks for an adapter that will reply to the request.

The adapter adapts the request and the object that Zope found with the URL.
The adapter class gets instantiated with the objects to be adapted, then it gets called.

The code above does the same thing that the standard implementation would do.
It makes {py:attr}`context` and {py:attr}`request` available as variables on the object.

I have written down these methods because it is important to understand some important concepts.

The {py:meth}`__init__` method gets called while Zope is still _trying_ to find a view. At that phase, the security has not been resolved.
Your code is not security checked.

For historical reasons, many errors that happen in the {py:meth}`__init__` method can result
in a page not found error instead of an exception.

Use the {py:meth}`__init__` method to do as little as possible, if at all.
Instead, you have the guarantee that the {py:meth}`__call__` method is called before anything else (but after the {py:meth}`__init__` method).

It has the security checks in place and so on.

From a practical standpoint, consider the {py:meth}`__call__` method your {py:meth}`__init__` method,
the biggest difference is that this method is supposed to return the HTML already.

Let your base class handle the HTML generation.

```{seealso}
<https://5.docs.plone.org/develop/plone/views/browserviews.html>
```
