---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(viewlets-advanced-label)=

# Advanced Viewlets

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

Solve the same tasks in the React frontend in chapter {doc}`volto_components_sponsors`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout resources
```

Code for the end of this chapter:

```shell
git checkout dexterity_3
```
````

In the previous chapter {doc}`dexterity_3` you created the `sponsor` content type.
Now let's learn how to display them at the bottom of every page.

To be solved task in this part:

- Display sponsors on all pages sorted by level

In this part you will:

- Display data from collected content

The topics we cover are:

- Viewlets
- Image scales
- Caching

## The view

For sponsors we will stay with the default view provided by Dexterity since we will only display the sponsors in a viewlet and not in their own page.

````{note}
If we really want a custom view for sponsors it could look like this.

```{code-block} xml
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
  <metal:content-core fill-slot="content-core">
    <h3 tal:content="structure view/w/level/render">
      Level
    </h3>

    <div tal:content="structure view/w/text/render">
      Text
    </div>

    <div class="newsImageContainer">
      <a tal:attributes="href context/url">
        <img tal:condition="python:getattr(context, 'logo', None)"
             tal:attributes="src string:${context/absolute_url}/@@images/logo/preview" />
      </a>
    </div>

    <div>
      <a tal:attributes="href context/url">
        Website
      </a>

      <img tal:condition="python:getattr(context, 'advertisement', None)"
           tal:attributes="src string:${context/absolute_url}/@@images/advertisement/preview" />

      <div tal:condition="python: 'notes' in view.w"
           tal:content="structure view/w/notes/render">
        Notes
      </div>

    </div>
  </metal:content-core>
</body>
</html>
```

Note how we handle the field with special permissions: {samp}`tal:condition="python: 'notes' in view.w"` checks if the convenience-dictionary {py:data}`w` (provided by the base class {py:class}`DefaultView`) holds the widget for the field `notes`.
If the current user does not have the permission {py:mod}`cmf.ManagePortal` it will be omitted from the dictionary and get an error since `notes` would not be a key in {py:data}`w`. By first checking if it's missing we work around that.
````

## The viewlet

Instead of writing a view you will have to display the sponsors at the bottom of the website in a viewlet.
In the chapter {doc}`viewlets_1` you already wrote a viewlet.

Remember:

- A viewlet produces in a snippet of HTML that can be put in various places in the page. These places are called `viewletmanager`.
- They can but don't have to have a association to the current context.
- The logo and searchbox are viewlets for example and they are always the same.
- Viewlets don't save data (portlets do).
- Viewlets have no user interface except the one to sort and hide/unhide viewlets.

Register the viewlet in {file}`browser/configure.zcml`

```{code-block} xml
:linenos:

<browser:viewlet
    name="sponsorsviewlet"
    manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
    for="*"
    layer="..interfaces.IPloneconfSiteLayer"
    class=".viewlets.SponsorsViewlet"
    template="templates/sponsors_viewlet.pt"
    permission="zope2.View"
    />
```

Add the viewlet class in {file}`browser/viewlets.py`

```{code-block} python
:emphasize-lines: 2-3, 5, 7-9, 19-63
:linenos:

# -*- coding: utf-8 -*-
from collections import OrderedDict
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from ploneconf.site.behaviors.featured import IFeatured
from ploneconf.site.content.sponsor import LevelVocabulary
from random import shuffle
from time import time


class FeaturedViewlet(ViewletBase):

    def is_featured(self):
        adapted = IFeatured(self.context)
        return adapted.featured


class SponsorsViewlet(ViewletBase):

    @ram.cache(lambda *args: time() // (60 * 60))
    def _sponsors(self):
        results = []
        for brain in api.content.find(portal_type='sponsor'):
            obj = brain.getObject()
            scales = api.content.get_view(
                name='images',
                context=obj,
                request=self.request)
            scale = scales.scale(
                'logo',
                width=200,
                height=80,
                direction='down')
            tag = scale.tag() if scale else None
            if not tag:
                # only display sponsors with a logo
                continue
            results.append({
                'title': obj.title,
                'description': obj.description,
                'tag': tag,
                'url': obj.url or obj.absolute_url(),
                'level': obj.level
            })
        return results

    def sponsors(self):
        sponsors = self._sponsors()
        if not sponsors:
            return
        results = OrderedDict()
        levels = [i.value for i in LevelVocabulary]
        for level in levels:
            level_sponsors = []
            for sponsor in sponsors:
                if level == sponsor['level']:
                    level_sponsors.append(sponsor)
            if not level_sponsors:
                continue
            shuffle(level_sponsors)
            results[level] = level_sponsors
        return results
```

- {py:meth}`_sponsors` returns a list of dictionaries containing all necessary info about sponsors.
- We create the complete `img` tag using a custom scale (200x80) using the view `images` from {py:mod}`plone.namedfile.` This actually scales the logos and saves them as new blobs.
- In {py:meth}`sponsors` we return an ordered dictionary of randomized lists of dicts (containing the information on sponsors). The order is by sponsor-level since we want the platinum sponsors on top and the bronze sponsors at the bottom. The randomization is for fairness among equal sponsors.

{py:meth}`_sponsors` is cached for an hour using [plone.memoize](https://5.docs.plone.org/manage/deploying/performance/decorators.html#timeout-caches). This way we don't need to keep all sponsor objects in memory all the time. But we'd have to wait for up to an hour until changes will be visible.

Instead we should cache until one of the sponsors is modified by using a callable {py:func}`_sponsors_cachekey` that returns a number that changes when a sponsor is modified.

> ```python
> ...
> def _sponsors_cachekey(method, self):
>     brains = api.content.find(portal_type='sponsor')
>     cachekey = sum([int(i.modified) for i in brains])
>     return cachekey
>
> @ram.cache(_sponsors_cachekey)
> def _sponsors(self):
>     catalog = api.portal.get_tool('portal_catalog')
> ...
> ```

```{seealso}
- [Guide to Caching](https://5.docs.plone.org/manage/deploying/caching/index.html)
- [Cache decorators](https://5.docs.plone.org/manage/deploying/performance/decorators.html)
- [Image Scaling](https://5.docs.plone.org/develop/plone/images/content.html#creating-scales)
```

## The template for the viewlet

Add the template {file}`browser/templates/sponsors_viewlet.pt`

```{code-block} xml
:linenos:

<div metal:define-macro="portal_sponsorbox"
     i18n:domain="ploneconf.site">
    <div id="portal-sponsorbox" class="container"
         tal:define="sponsors view/sponsors;"
         tal:condition="sponsors">
        <div class="row">
            <h2>We ❤ our sponsors</h2>
        </div>
        <div tal:repeat="level sponsors"
             tal:attributes="id python:'level-' + level"
             class="row">
            <h3 tal:content="python: level.capitalize()">
                Gold
            </h3>
            <tal:images tal:define="items python:sponsors[level];"
                        tal:repeat="item items">
                <div class="sponsor">
                    <a href=""
                       tal:attributes="href python:item['url'];
                                       title python:item['title'];">
                        <img tal:replace="structure python:item['tag']" />
                    </a>
                </div>
            </tal:images>
        </div>
    </div>
</div>
```

You can now add some CSS in {file}`browser/static/ploneconf.css` to make it look OK.

```css
.sponsor {
  display: inline-block;
  margin: 0 1em 1em 0;
}

.sponsor:hover {
  box-shadow: 0 0 8px #000;
  -moz-box-shadow: 0 0 8px #000;
  -webkit-box-shadow: 0 0 8px #000;
}
```

Result:

```{figure} _static/dexterity_3_sponsor_schema.png
:alt: The result of the newly created content type.
:scale: 50%

The result of the newly created content type.
```

### Exercise 2

This is more of a Python exercise. The gold and bronze sponsors should also have a bigger logo than the others. Scale the sponsors' logos to the following sizes without using CSS.

- Platinum: 500x200
- Gold: 350x150
- Silver: 200x80
- Bronze: 150x60

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} python
:emphasize-lines: 10-15, 41, 44-45
:linenos:

# -*- coding: utf-8 -*-
from collections import OrderedDict
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from ploneconf.site.behaviors.social import ISocial
from ploneconf.site.content.sponsor import LevelVocabulary
from random import shuffle

LEVEL_SIZE_MAPPING = {
    'platinum': (500, 200),
    'gold': (350, 150),
    'silver': (200, 80),
    'bronze': (150, 60),
}


class SocialViewlet(ViewletBase):

    def lanyrd_link(self):
        adapted = ISocial(self.context)
        return adapted.lanyrd


class SponsorsViewlet(ViewletBase):

    def _sponsors_cachekey(method, self):
        brains = api.content.find(portal_type='sponsor')
        cachekey = sum([int(i.modified) for i in brains])
        return cachekey

    @ram.cache(_sponsors_cachekey)
    def _sponsors(self):
        results = []
        for brain in api.content.find(portal_type='sponsor'):
            obj = brain.getObject()
            scales = api.content.get_view(
                name='images',
                context=obj,
                request=self.request)
            width, height = LEVEL_SIZE_MAPPING[obj.level]
            scale = scales.scale(
                'logo',
                width=width,
                height=height,
                direction='down')
            tag = scale.tag() if scale else None
            if not tag:
                # only display sponsors with a logo
                continue
            results.append({
                'title': obj.title,
                'description': obj.description,
                'tag': tag,
                'url': obj.url or obj.absolute_url(),
                'level': obj.level
            })
        return results

    def sponsors(self):
        sponsors = self._sponsors()
        if not sponsors:
            return
        results = OrderedDict()
        levels = [i.value for i in LevelVocabulary]
        for level in levels:
            level_sponsors = []
            for sponsor in sponsors:
                if level == sponsor['level']:
                    level_sponsors.append(sponsor)
            if not level_sponsors:
                continue
            shuffle(level_sponsors)
            results[level] = level_sponsors
        return results
```
````
