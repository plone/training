---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(events-classic-label)=

# Turning Talks into Events

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Solve the same tasks in the React frontend in chapter {doc}`events`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout dexterity_2
```

Code for the end of this chapter:

```shell
git checkout events
```
````

We forgot something: a list of talks is great, especially if you can sort it according to your preferences. But if a visitor decides she wants to actually go to see a talk she needs to know when it will take place.

We need a schedule and for this we need to store the information when a talk will happen.

Luckily the default type _Event_ is based on reusable behaviors from the package {py:mod}`plone.app.event` that we can reuse.

In this chapter you will

- enable this behavior for talks
- display the date in the talkview and talklistview

First enable the behavior {py:class}`IEventBasic` for talks in {file}`profiles/default/types/talk.xml`

```{code-block} xml
:emphasize-lines: 6
:linenos:

<property name="behaviors">
  <element value="plone.dublincore"/>
  <element value="plone.namefromtitle"/>
  <element value="plone.versioning"/>
  <element value="ploneconf.featured"/>
  <element value="plone.eventbasic"/>
</property>
```

After you activate the behavior by hand or you reinstalled the add-on you will now have some additional fields for `start`, `end`, `open_end` and `whole_day`.

To display the new data we reuse a default event summary view as documented in <https://ploneappevent.readthedocs.io/en/latest/development.html#reusing-the-event-summary-view-to-list-basic-event-information>

Edit {file}`browser/templates/talkview.pt`

```{code-block} html
:emphasize-lines: 7
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
    <metal:content-core fill-slot="content-core" tal:define="widgets view/w">

        <tal:eventsummary replace="structure context/@@event_summary"/>

        <p>
            <span tal:content="context/type_of_talk">
                Talk
            </span>
            suitable for
            <span tal:replace="structure widgets/audience/render">
                Audience
            </span>
        </p>

        <div tal:content="structure widgets/details/render">
            Details
        </div>

        <div class="newsImageContainer">
            <img tal:condition="python:getattr(context, 'image', None)"
                 tal:attributes="src string:${context/absolute_url}/@@images/image/thumb" />
        </div>

        <div>
            <a class="email-link" tal:attributes="href string:mailto:${context/email}">
                <strong tal:content="context/speaker">
                    Jane Doe
                </strong>
            </a>
            <div tal:content="structure widgets/speaker_biography/render">
                Biography
            </div>
        </div>

    </metal:content-core>
</body>
</html>
```

Similar to the field `room`, the problem now appears that speakers submitting their talks should not be able to set a time and day for their talks.
Sadly it is not easy to modify permissions of fields provided by behaviors (unless you write the behavior yourself).
At least in this case we can take the easy way out since the field does not contain secret information: we will simply hide the fields from contributors using css and show them for reviewers. We will do so in chapter {doc}`theming` when we add some CSS files.

Modify {file}`browser/static/ploneconf.css` and add:

```css
body.userrole-contributor #formfield-form-widgets-IEventBasic-start,
body.userrole-contributor #formfield-form-widgets-IEventBasic-end > *,
body.userrole-contributor #formfield-form-widgets-IEventBasic-whole_day,
body.userrole-contributor #formfield-form-widgets-IEventBasic-open_end {
  display: none;
}

body.userrole-reviewer #formfield-form-widgets-IEventBasic-start,
body.userrole-reviewer #formfield-form-widgets-IEventBasic-end > *,
body.userrole-reviewer #formfield-form-widgets-IEventBasic-whole_day,
body.userrole-reviewer #formfield-form-widgets-IEventBasic-open_end {
  display: block;
}
```

You can now display the start date of a talk in the talklist.
Modify the class {py:class}`TalkListView` and the template {file}`browser/templates/talklistview.pt` to show the new info:

```{code-block} python
:emphasize-lines: 17
:linenos:

class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        results = []
        brains = api.content.find(context=self.context, portal_type='talk')
        for brain in brains:
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

```{code-block} html
:emphasize-lines: 5-9
:linenos:

[...]
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
[...]
```

```{note}
If you changed the view {py:class}`TalkListView` to only return brains as described in {ref}`plone5-dexterity2-use-indexes-label` you can save yourself a lot of work and simply use the existing index `start` (generously provided by {py:mod}`plone.app.event`) in the template as `python:brain.start`.
```

## Exercise 1

Find out where `event_summary` comes from and describe how you could override it.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Use your editor or grep to search all ZCML files in the folder {file}`packages` for the string `name="event_summary"`

```shell
$ grep -siRn --include \*.zcml 'name="event_summary"' ./packages
./packages/plone/app/event/browser/configure.zcml:66:        name="event_summary"
./packages/plone/app/event/browser/configure.zcml:75:        name="event_summary"
```

The relevant registration is:

```xml
<browser:page
    for="plone.event.interfaces.IEvent"
    name="event_summary"
    class=".event_summary.EventSummaryView"
    template="event_summary.pt"
    permission="zope2.View"
    layer="..interfaces.IBrowserLayer"
    />
```

So there is a class {py:class}`plone.app.event.browser.event_summary.EventSummaryView` and a template {file}`event_summary.pt` that could be overridden with {py:mod}`z3c.jbot` by copying it as {file}`plone.app.event.browser.event_summary.pt` in {file}`browser/overrides`.
````

## Exercise 2

Find out where the event behavior is defined and which fields it offers.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

The id with which the behavior is registered in {file}`Talk.xml` is a Python path. So {py:class}`plone.app.event.dx.behaviors.IEventBasic` can be found in {file}`packages/plone.app.event/plone/app/event/dx/behaviors.py`

```python
class IEventBasic(model.Schema, IDXEvent):

    """ Basic event schema.
    """
    start = schema.Datetime(
        title=_(
            u'label_event_start',
            default=u'Event Starts'
        ),
        description=_(
            u'help_event_start',
            default=u'Date and Time, when the event begins.'
        ),
        required=True,
        defaultFactory=default_start
    )
    directives.widget(
        'start',
        DatetimeFieldWidget,
        default_timezone=default_timezone,
        klass=u'event_start'
    )

    end = schema.Datetime(
        title=_(
            u'label_event_end',
            default=u'Event Ends'
        ),
        description=_(
            u'help_event_end',
            default=u'Date and Time, when the event ends.'
        ),
        required=True,
        defaultFactory=default_end
    )
    directives.widget(
        'end',
        DatetimeFieldWidget,
        default_timezone=default_timezone,
        klass=u'event_end'
    )

    whole_day = schema.Bool(
        title=_(
            u'label_event_whole_day',
            default=u'Whole Day'
        ),
        description=_(
            u'help_event_whole_day',
            default=u'Event lasts whole day.'
        ),
        required=False,
        default=False
    )
    directives.widget(
        'whole_day',
        SingleCheckBoxFieldWidget,
        klass=u'event_whole_day'
    )

    open_end = schema.Bool(
        title=_(
            u'label_event_open_end',
            default=u'Open End'
        ),
        description=_(
            u'help_event_open_end',
            default=u"This event is open ended."
        ),
        required=False,
        default=False
    )
    directives.widget(
        'open_end',
        SingleCheckBoxFieldWidget,
        klass=u'event_open_end'
    )
```

Note how it uses `defaultFactory` to set an initial value.
````

### Summary

- You reused a existing behavior to add new fields
- You reused existing indexes to display the time of a talk
- You did not have to write your own datetime fields and indexers o/
