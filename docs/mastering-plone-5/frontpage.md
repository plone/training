---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-frontpage-label)=

# Creating a Dynamic Front Page

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout registry
```

Code for the end of this chapter:

```shell
git checkout frontpage
```

{doc}`code`
````

In this chapter we will:

- Create a standalone view used for the front page
- Show dynamic content
- Use ajax to load content
- Embed tweets about ploneconf

The topics we cover are:

- Standalone views
- Querying the catalog by date
- DRY ("Don't Repeat Yourself")
- macros
- patterns

## The Front Page

Register the view in `browser/configure.zcml`:

```xml
<browser:page
    name="frontpageview"
    for="*"
    layer="ploneconf.site.interfaces.IPloneconfSiteLayer"
    class=".frontpage.FrontpageView"
    template="templates/frontpageview.pt"
    permission="zope2.View"
    />
```

Add the view to a file `browser/frontpage.py`. We want a list of all talks that happen today.

```{code-block} python
:linenos:

# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView

import datetime


class FrontpageView(BrowserView):
    """The view of the conference frontpage
    """

    def talks(self):
        """Get today's talks"""
        results = []
        today = datetime.date.today()
        brains = api.content.find(
            portal_type='talk',
            sort_on='start',
            sort_order='descending',
        )
        for brain in brains:
            if brain.start.date() == today:
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(brain.audience or []),
                    'type_of_talk': brain.type_of_talk,
                    'speaker': brain.speaker,
                    'room': brain.room,
                    'start': brain.start,
                    })
        return results
```

- We do not constrain the search to a certain folder to also find the party and the sprints.

- With `if brain.start.date() == today:` we test if the talk is today.

- It would be more effective to query the catalog for events that happen in the daterange between today and tomorrow:

  ```{code-block} python
  :emphasize-lines: 2, 3, 6
  :linenos:

  today = datetime.date.today()
  tomorrow = today + datetime.timedelta(days=1)
  date_range_query = {'query': (today, tomorrow), 'range': 'min:max'}
  brains = api.content.find(
      portal_type='talk',
      start=date_range_query,
      sort_on='start',
      sort_order='ascending'
  )
  ```

- The `sort_on='start'` sorts the results returned by the catalog by start-date.

- By removing the `portal_type='talk'` from the query you could include other events in the schedule (like the party or sightseeing-tours). But you'd have to take care to not create AttributeErrors by accessing fields that are specific to talk. To work around that use `speaker = getattr(brain, 'speaker', None)` and testing with `if speaker is not None:`

- The rest is identical to what the talklistview does.

## The template

Create the template `browser/templates/frontpageview.pt` (for now without talks). Display the rich text field to allow the frontpage to be edited.

```{code-block} html
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>

<metal:content-core fill-slot="content-core">

    <div id="parent-fieldname-text"
        tal:condition="python: getattr(context, 'text', None)"
        tal:content="structure python:context.text.output_relative_to(view.context)" />

</metal:content-core>

</body>
</html>
```

Now you could add the whole code that we used for the talklistview again. But instead we go D.R.Y. and reuse the talklistview by turning it into a macro.

Edit `browser/templates/talklistview.pt` and wrap the list in a macro definition:

```{code-block} html
:emphasize-lines: 7, 55
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
  <metal:content-core fill-slot="content-core">

  <metal:talklist define-macro="talklist">
  <table class="listing"
         id="talks"
         tal:define="talks python:view.talks()">
    <thead>
      <tr>
        <th>Title</th>
        <th>Speaker</th>
        <th>Audience</th>
        <th>Time</th>
        <th>Room</th>
      </tr>
    </thead>
    <tbody>
      <tr tal:repeat="talk talks">
        <td>
          <a href=""
             class="pat-contentloader"
             data-pat-contentloader="url:${python:talk['url']}?ajax_load=1;content:#content;target:.talkinfo > *"
             tal:attributes="href python:talk['url'];
                             title python:talk['description']"
             tal:content="python:talk['title']">
             The 7 sins of plone-development
          </a>
        </td>
        <td tal:content="python:talk['speaker']">
            Philip Bauer
        </td>
        <td tal:content="python:talk['audience']">
            Advanced
        </td>
        <td class="pat-moment"
            data-pat-moment="format:calendar"
            tal:content="python:talk['start']">
            Time
        </td>
        <td tal:content="python:talk['room']">
            101
        </td>
      </tr>
      <tr tal:condition="not:talks">
        <td colspan=5>
            No talks so far :-(
        </td>
      </tr>
    </tbody>
  </table>
  <div class="talkinfo"><span /></div>
  </metal:talklist>

  </metal:content-core>
</body>
</html>
```

Now use that macro in `browser/templates/frontpageview.pt`

```{code-block} html
:linenos:

<div class="col-lg-6">
    <h2>Todays Talks</h2>
    <div metal:use-macro="context/@@talklistview/talklist">
        Instead of this the content of the macro will appear...
    </div>
</div>
```

Calling that macro in Python looks like this `metal:use-macro="python: context.restrictedTraverse('talklistview')['talklist']"`

```{note}
In {file}`talklistview.pt` the call {samp}`view/talks"` calls the method {py:meth}`talks` from the browser view {py:class}`TalkListView` to get the talks. Reused as a macro on the frontpage it now uses the method {py:meth}`talks` by the `frontpageView` to get a different list!
It is not always smart to do that since you might want to display other data. E.g. for a list of todays talks you don't want show the date but only the time using `data-pat-moment="format:LT"`
Also this frontpage will probably not win a beauty-contest. But that's not the task of this training.
```

### Exercise 1

Change the link to open the talk-info in a [modal](https://plone.github.io/mockup/dev/#pattern/modal).

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 2

 <a href=""
    class="pat-plone-modal"
    tal:attributes="href string:${talk/url};
                    title talk/description"
    tal:content="talk/title">
    The 7 sins of plone development
 </a>
```
````

## Twitter

You might also want to embed a twitter feed into the page. Luckily twitter makes it easy to do that.
When you browse to the [publish.twitter.com](https://publish.twitter.com/) and have them create a snippet for @ploneconf and paste it in the template wrapped in a `<div class="col-lg-6">...</div>` to have the talklist next to the feeds:

```{code-block} html
:emphasize-lines: 19-22

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>

<metal:content-core fill-slot="content-core">

  <div id="parent-fieldname-text"
      tal:condition="python: getattr(context, 'text', None)"
      tal:content="structure python:context.text.output_relative_to(view.context)" />

  <div class="col-lg-6">
    <h2>Todays Talks</h2>
    <div metal:use-macro="context/@@talklistview/talklist">
        Instead of this the content of the macro will appear...
    </div>
  </div>

  <div class="col-lg-6">
    <a class="twitter-timeline" data-height="600" data-dnt="true" href="https://x.com/ploneconf?ref_src=twsrc%5Etfw">Tweets by ploneconf</a> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
  </div>

</metal:content-core>

</body>
</html>
```

## Activating the view

The view is meant to be used with documents (or any other type that has a rich text field 'text'). The easiest way to use it is setting it as the default view for the Document that is currently the default page for the portal. By default that document has the id `front-page`.

You can either access it directly at <http://localhost:8080/Plone/front-page> or by disabling the default page for the portal and it should show up in the navigation. Try out the new view like this: <http://localhost:8080/Plone/front-page/frontpageview>.

To set that view by hand as the default view for `front-page` in the ZMI: <http://localhost:8080/Plone/front-page/manage_propertiesForm>. Add a new property `layout` and set it to `frontpageview`.

Done. This way you can still use the button _Edit_ to edit the frontpage.

```{seealso}
- Querying by date: <https://5.docs.plone.org/develop/plone/searching_and_indexing/query.html#querying-by-date>
```
