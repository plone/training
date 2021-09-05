(registry-label)=

# Vocabularies, Registry-Settings and Control Panels


````{sidebar}
```{figure} _static/plone.svg
:alt: Plone Logo
```
```{figure} _static/volto.svg
:alt: Volto Logo
```

This chapter is about both the React frontend Volto and Plone Classic.

---

**Get the code! ({doc}`More info <code>`)**
Code for the beginning of this chapter:

```
# frontend
git checkout event

# backend
git checkout event
```

Code for the end of this chapter:

```
# frontend
git checkout registry

# backend
git checkout registry
```
````

In this part you will:

- Store custom settings in the registry
- Create a controlpanel to manage custom settings
- Create options in fields as vocabularies
- Assign talks to rooms

Topics covered:

- plone.app.registry
- Vocabularies
- Control panels

## Introduction

Do you remember the fields `audience` and `type_of_talk` from the talk content-type?
We provided several options to chose from that were hard-coded in the schema.

Next we want to add a field to assign talks to a room.
Since the conference next year will have different room numbers or names these values need to to be editable.

And while we're at it: It would be much better to have the options for `audience` and `type_of_talk` editable by admins as well, e.g. to be able to add *Lightning Talks*!

By combining the registry, a controlpanel and vocabularies you can allow rooms to be editable options.

To be able to to so you first need to get to know the registry.

## The Registry

The registry is used to get and set values stored in records. Each record contains the actual value, as well as a field that describes the record in more detail. It has a nice dict-like API.

All global settings since Plone 5 are stored in the registry.

The registry itself is provided by [plone.registry](https://pypi.org/project/plone.registry) and the UI to interact with it by [plone.app.registry](https://pypi.org/project/plone.app.registry)

Almost all settings in `/plone_control_panel` are actually stored in the registry and can be modified using its UI directly.

Open <http://localhost:8080/Plone/portal_registry> and filter for `displayed_types`.
You see that you can modify the content types that should be shown in the navigation and site map. The values are the same as in <http://localhost:8080/Plone/@@navigation-controlpanel> but the later form is customized for usability.

```{note}
This UI for the registry is not yet available in Volto.
```

## Registry-records

You already added an additional criterion usable for Collections in {file}`profiles/default/registry/querystring.xml`.
This setting is stored in the registry.

Let's look at existing values in the registry

Go to <http://localhost:3000/controlpanel/navigation> and add `talk` to the field **Displayed content types**.
After saving talks that are in the root-folder will show up in the navigation.

This setting is stored in `plone.displayed_types`.

## Accessing and modifying records in the registry

In Python you can access the registry with this value like this:

```{code-block} python
:linenos: true

from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)
displayed_types = registry.get('plone.displayed_types')
```

`displayed_types` is then the tuple `('Image', 'File', 'Link', 'News Item', 'Folder', 'Document', 'Event', 'talk')`

{py:mod}`plone.api` holds convenience methods to make this even easier:

```{code-block} python
:linenos: true

from plone import api

api.portal.get_registry_record('plone.displayed_types')
api.portal.set_registry_record('plone.smtp_host', 'my.mail.server')
```

## Managing custom registry records

Now let's add our own custom settings:

- Is talk submission open or closed?
- Which rooms are available for talks?

While we're at it we can also add new settings `types_of_talk` and `audiences` that we will use later for the fields `type_of_talk` and `audience`.

To define custom records you write the same type of schema as you already did for dexterity types or for behaviors:

Add a file {file}`browser/controlpanel.py`:

```{code-block} python
:linenos: true

from zope import schema
from zope.interface import Interface


class IPloneconfControlPanel(Interface):

    talk_submission_open = schema.Bool(
        title='Allow talk submission',
        description='Allow the submission of talks for anonymous user',
        default=False,
        required=False,
    )

    types_of_talk = schema.List(
        title=u'Available types for talks',
        default=['Talk', 'Training', 'Keynote'],
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )

    audiences = schema.List(
        title='Available audiences for talks',
        default=['Beginner', 'Advanced', 'Professional'],
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )

    rooms = schema.Tuple(
        title='Available Rooms for the conference',
        default=('101', '201', 'Auditorium'),
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )
```

You now have to register this schema for the registry.
Add the following to {file}`profiles/default/registry/main.xml`

```xml
<records interface="ploneconf.site.browser.controlpanel.IPloneconfControlPanel"
         prefix="ploneconf" />
```

```{note}
The `prefix` allows you access these records with a shortcut:
You can use `ploneconf.rooms` instead of having to use `ploneconf.site.browser.controlpanel.IPloneconfControlPanel.room`.
```

After reinstalling the package (to load the registry entry) you can access and modify these values in the registry as described above:

Either use <http://localhost:8080/Plone/portal_registry> or python:

```python
from plone import api

api.portal.get_registry_record('ploneconf.rooms')
```

````{note}
We use python to define the values.

Alternatively you could also add these values only using Generic Setup.

You could even create new records through the web using <http://localhost:8080/Plone/portal_registry>.

The following creates a new value `ploneconf.talk_submission_open` using Generic Setup:

```{code-block} xml
:linenos: true

<record name="ploneconf.talk_submission_open">
  <field type="plone.registry.field.Bool">
    <title>Allow talk submission</title>
    <description>Allow the submission of talks for anonymous users</description>
    <required>False</required>
  </field>
  <value>False</value>
</record>
```

When creating a new site a lot of default settings are created that way. See <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml> to see how {py:mod}`Products.CMFPlone` registers values.
````

## Add a custom control panel

Now you will add a custom control panel to edit all setting related to our package with a nice UI.

To register a controlpanel in Volto and Plone Classic you need quite a bit of boiler-plate:

```{code-block} python
:emphasize-lines: 1-4, 6, 44-61
:linenos: true

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IPloneconfControlPanel(Interface):

    talk_submission_open = schema.Bool(
        title=u'Allow talk submission',
        description=u'Allow the submission of talks for anonymous user',
        default=False,
        required=False,
    )

    types_of_talk = schema.List(
        title=u'Available types for talks',
        default=[u'Talk', u'Training', u'Keynote', u'Lightning Talk'],
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )

    audiences = schema.List(
        title=u'Available audiences for talks',
        default=[u'Beginner', u'Advanced', u'Professional'],
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )

    rooms = schema.Tuple(
        title=u'Available Rooms for the conference',
        default=(u'101', u'201', u'Auditorium'),
        missing_value=None,
        required=False,
        value_type=schema.TextLine(),
    )


@adapter(Interface, Interface)
class PloneconfControlPanel(RegistryConfigletPanel):
    schema = IPloneconfControlPanel
    schema_prefix = 'ploneconf'
    configlet_id = 'ploneconf-controlpanel'
    configlet_category_id = 'General'
    title = 'Ploneconf Settings'
    group = 'Products'


class PloneconfControlPanelForm(RegistryEditForm):
    schema = IPloneconfControlPanel
    schema_prefix = 'ploneconf'
    label = u'Ploneconf Settings'


PloneconfControlPanelView = layout.wrap_form(
    PloneconfControlPanelForm, ControlPanelFormWrapper)
```

You also need to register these in {file}`browser/configure.zcml`:

```{code-block} xml
:linenos: true

<browser:page
    name="ploneconf-controlpanel"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    class=".controlpanel.PloneconfControlPanelView"
    permission="cmf.ManagePortal"
    />

<adapter
    factory="ploneconf.site.browser.controlpanel.PloneconfControlPanel"
    name="ploneconf-controlpanel" />
```

Finally you also need to register it in Generic Setup.
Add a file {file}`profiles/default/controlpanel.xml`:

```{code-block} xml
:linenos: true

<?xml version="1.0"?>
<object name="portal_controlpanel">
  <configlet
      title="Ploneconf Settings"
      action_id="ploneconf-controlpanel"
      appId="ploneconf-controlpanel"
      category="Products"
      condition_expr=""
      icon_expr=""
      url_expr="string:${portal_url}/@@ploneconf-controlpanel"
      visible="True">
    <permission>Manage portal</permission>
  </configlet>
</object>
```

After applying the profile (e.g. by reinstall the package) your control panel shows up.

In Volto it is at <http://localhost:3000/controlpanel/ploneconf-controlpanel>

```{figure} _static/volto_ploneconf_controlpanel.png
```

In Plone Classic at <http://localhost:8080/Plone/ploneconf-controlpanel>

```{figure} _static/classic_ploneconf_controlpanel.png
```

## Vocabularies

Now the custom settings are stored in the registry that we can modify then in a nice way as admins.
We still need to use these options in talks.

To do so we turn them into vocabularies.

Vocabularies are often used for selection fields. They have many benefits:

- They allow you to separate the displayed option and the stored value for a field. This allows translating titles while using the same values.
- They can be created dynamically, so the available options can change depending on existing content, the role of the user or even the time of day.

Create a file {file}`vocabularies.py` and write code that generates vocabularies from these settings:

```{code-block} python
:linenos: true

from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


@provider(IVocabularyFactory)
def RoomsVocabularyFactory(context):
    name = 'ploneconf.rooms'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def TalkTypesVocabulary(context):
    name = 'ploneconf.types_of_talk'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def AudiencesVocabulary(context):
    name = 'ploneconf.audiences'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)
```

You can now register these vocabularies as named utilities in {file}`configure.zcml`:

```xml
<utility
    name="ploneconf.types_of_talk"
    component="ploneconf.site.vocabularies.TalkTypesVocabulary" />

<utility
    name="ploneconf.audiences"
    component="ploneconf.site.vocabularies.AudiencesVocabulary" />

<utility
    name="ploneconf.rooms"
    component="ploneconf.site.vocabularies.RoomsVocabularyFactory" />
```

From now on you can use these vocabulary by referring to their name, e.g. `ploneconf.rooms`.

````{note}
- Plone comes with many useful named vocabularies that you can use in your own projects, for example `plone.app.vocabularies.Users` or `plone.app.vocabularies.PortalTypes`.

- See <https://github.com/plone/plone.app.vocabularies/> for a list of vocabularies.

- We turn the values from the registry into a dynamic `SimpleVocabulary` that can be used in the schema.

- You could use the context with which the vocabulary is called or the request (using `getRequest` from `from zope.globalrequest import getRequest`) to constrain the values in the vocabulary.

- We use the handy helper method `safe_simplevocabulary_from_values` to create the vocabulary since the `token` of a `SimpleTerm` in a `SimpleVocabulary` needs to be ASCII.

- `binascii.b2a_qp` (which is used by `safe_simplevocabulary_from_values`) has the annoying habit of adding line-breaks every 80 characters. Make sure your values are shorter than that or use something else to create the vocabulary-terms!

- You can write your own helper to further control the creation of the vocabulary terms. The `value` is stored on the object, the `token` used to communicate with the widget during editing and `title` is what is displayed in the widget.
  This example allows you to translate the displayed title while keeping the value stored on the object the same in all languages:

  ```python
  from binascii import b2a_qp
  from ploneconf.site import _
  from zope.schema.vocabulary import SimpleTerm
  from zope.schema.vocabulary import SimpleVocabulary

  def simplevoc(values):
      return SimpleVocabulary(
          [SimpleTerm(value=i, token=b2a_qp(i.encode('utf-8')), title=_(i)) for i in values],
      )
  ```
````

```{seealso}
Plone documentation **Vocabularies** <https://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html>
```

## Using vocabularies in a schema

To use a vocabulary in a schema replace `values` with `vocabulary` and point to the vocbulary by name:

```{code-block} python
:emphasize-lines: 3
:linenos: true

type_of_talk = schema.Choice(
    title=_(u'Type of talk'),
    vocabulary='ploneconf.types_of_talk',
    required=True,
)
```

Don't forget to add the new field `room` now.

Edit {file}`content/talk.py`:

```{code-block} python
:emphasize-lines: 23, 37, 85-90
:linenos: true

# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from ploneconf.site import _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ITalk(model.Schema):
    """Dexterity-Schema for Talks"""

    directives.widget(type_of_talk=RadioFieldWidget)
    type_of_talk = schema.Choice(
        title=_(u'Type of talk'),
        vocabulary='ploneconf.types_of_talk',
        required=True,
        )

    details = RichText(
        title=_(u'Details'),
        description=_(u'Description of the talk (max. 2000 characters)'),
        max_length=2000,
        required=True,
        )

    directives.widget(audience=CheckBoxFieldWidget)
    audience = schema.Set(
        title=_(u'Audience'),
        value_type=schema.Choice(vocabulary='ploneconf.audiences'),
        required=False,
        )

    speaker = schema.TextLine(
        title=_(u'Speaker'),
        description=_(u'Name (or names) of the speaker'),
        required=False,
        )

    company = schema.TextLine(
        title=_(u'Company'),
        required=False,
        )

    email = Email(
        title=_(u'Email'),
        description=_(u'Email adress of the speaker'),
        required=False,
        )

    website = schema.TextLine(
        title=_(u'Website'),
        required=False,
        )

    twitter = schema.TextLine(
        title=_(u'Twitter name'),
        required=False,
        )

    github = schema.TextLine(
        title=_(u'Github username'),
        required=False,
        )

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(u'Portrait of the speaker'),
        required=False,
        )

    speaker_biography = RichText(
        title=_(u'Speaker Biography (max. 1000 characters)'),
        max_length=1000,
        required=False,
        )

    directives.widget(room=CheckBoxFieldWidget)
    room = schema.Set(
        title=_(u'Room'),
        value_type=schema.Choice(vocabulary='ploneconf.rooms'),
        required=False,
        )


@implementer(ITalk)
class Talk(Container):
    """Talk instance class"""
```

One tiny thing is still missing: We should display the room.

Modify {file}`frontend/src/components/Views/Talk.jsx` an add this after the `When` component:

```{code-block}
:emphasize-lines: 6
:linenos: true

    {content.room && (
      <>
        <Header dividing sub>
          Where
        </Header>
        <p>{content.room.title}</p>
      </>
    )}
```

````{admonition} The complete TalkView
:class: toggle

```jsx
import React from 'react';
import { flattenToAppURL } from '@plone/volto/helpers';
import {
  Container,
  Header,
  Image,
  Icon,
  Label,
  Segment,
} from 'semantic-ui-react';
import { Helmet } from '@plone/volto/helpers';
import { When } from '@plone/volto/components/theme/View/EventDatesInfo';

const TalkView = (props) => {
  const { content } = props;
  const color_mapping = {
    Beginner: 'green',
    Advanced: 'yellow',
    Professional: 'red',
  };

  return (
    <Container id="page-talk">
      <Helmet title={content.title} />
      <h1 className="documentFirstHeading">
        {content.type_of_talk.title}: {content.title}
      </h1>
      <Segment floated="right">
        {content.start && !content.hide_date && (
          <>
            <Header dividing sub>
              When
            </Header>
            <When
              start={content.start}
              end={content.end}
              whole_day={content.whole_day}
              open_end={content.open_end}
            />
          </>
        )}
        {content.room && (
          <>
            <Header dividing sub>
              Where
            </Header>
            <p>{content.room.title}</p>
          </>
        )}
        {content.audience && (
          <Header dividing sub>
            Audience
          </Header>
        )}
        {content.audience.map((item) => {
          let audience = item.title;
          let color = color_mapping[audience] || 'green';
          return (
            <Label key={audience} color={color}>
              {audience}
            </Label>
          );
        })}
      </Segment>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.details && (
        <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      )}
      {content.speaker && (
        <Segment clearing>
          <Header dividing>{content.speaker}</Header>
          {content.website ? (
            <p>
              <a href={content.website}>{content.company}</a>
            </p>
          ) : (
            <p>{content.company}</p>
          )}
          {content.email && (
            <p>
              Email: <a href={`mailto:${content.email}`}>{content.email}</a>
            </p>
          )}
          {content.twitter && (
            <p>
              Twitter:{' '}
              <a href={`https://twitter.com/${content.twitter}`}>
                {content.twitter.startsWith('@')
                  ? content.twitter
                  : '@' + content.twitter}
              </a>
            </p>
          )}
          {content.github && (
            <p>
              Github:{' '}
              <a href={`https://github.com/${content.github}`}>
                {content.github}
              </a>
            </p>
          )}
          {content.image && (
            <Image
              src={flattenToAppURL(content.image.scales.preview.download)}
              size="small"
              floated="right"
              alt={content.image_caption}
              avatar
            />
          )}
          {content.speaker_biography && (
            <div
              dangerouslySetInnerHTML={{
                __html: content.speaker_biography.data,
              }}
            />
          )}
        </Segment>
      )}
    </Container>
  );
};
export default TalkView;
```

By the way: When using a vocabulary you can also drop the annoying `item.title || item.token` pattern.
````

```{note}
The approach to create options for fields from registry-records has one problem:
Existing talks are not updated when you change a value in the controlpanel.
Instead they will have invalid data and you will have to update them.

If the options in your fields tend to change often you should consider using [collective.taxonomy](https://github.com/collective/collective.taxonomy) to manage vocabularies.
Among many other things it allows you to translate terms and to change the text that is displayed while keeping the values the same.
Using {py:mod}`collective.taxonomy` for vocabularies works fine with Volto, but the UI where you create and edit vocabularies is so far only available in Plone Classic.

In this case study the approach used here works fine though because you will create a new site for next years conference anyway.
```

## Summary

- You successfully combined the registry, a controlpanel and vocabularies to allow managing field options by admins.
- It seems like a lot but you will certainly use dynamic vocabularies, controlpanels and the registry in all of your future Plone projects in one way or another.
