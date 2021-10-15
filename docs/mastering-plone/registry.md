---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": "Vocabularies, Registry-Settings and Control Panels"
  "keywords": "vocabulary, registry, controlpanel, select, options"
---

(registry-label)=

# Vocabularies, Registry-Settings and Control Panels


````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
# frontend
git checkout event
```

```shell
# backend
git checkout event
```

Code for the end of this chapter:

```shell
# frontend
git checkout registry
```

```shell
# backend
git checkout registry
```

{doc}`code`
````

In this part you will:

- Store custom settings in the registry
- Create a controlpanel to manage custom settings
- Create options in fields as vocabularies
- Training story: Assign talks to rooms

Topics covered:

- plone.app.registry
- Vocabularies
- Control panels

## Introduction

Do you remember the fields `audience` and `type_of_talk` of talk content type?
We provided several options to choose from that were hard-coded in the schema.

Next we want to add a field to assign talks to a room.
Since the conference next year will have different room names, these values need to be editable.

And while we're at it: It would be much better to have the options for `audience` and `type_of_talk` editable by admins as well, e.g. to be able to add *Lightning Talks*!

By combining the registry, a controlpanel and vocabularies you can allow rooms to be editable options.

To be able to to so you first need to get to know the registry.

## The Registry

The registry is used to get and set values stored in records. Each record consists of the actual value, as well as a field that describes the record in more detail. It has a nice dict-like API.

From Plone 5 on all global settings are stored in the registry.

The registry itself is provided by [plone.registry](https://pypi.org/project/plone.registry) and the UI to interact with it by [plone.app.registry](https://pypi.org/project/plone.app.registry)

Almost all settings in `/plone_control_panel` are actually stored in the registry and can be modified using its UI directly.

Open <http://localhost:8080/Plone/portal_registry> and filter for `displayed_types`.
You see that you can modify the content types that should be shown in the navigation and site map. The values are the same as in <http://localhost:8080/Plone/@@navigation-controlpanel>, but the later form is customized for usability.

```{note}
This UI for the registry is not yet available in frontend.
```

## Registry Records

You already added in {doc}`volto_frontpage` an additional criterion usable for Collections in {file}`profiles/default/registry/querystring.xml`.
This setting is stored in the registry.

Let's look at existing values in the registry.

Go to <http://localhost:3000/controlpanel/navigation> and add `talk` to the field **Displayed content types**.
Talks in the root will now show up in the navigation.
This setting is stored in registry record `plone.displayed_types`.

## Accessing and modifying records in the registry

In Python you can access the registry record with key `plone.displayed_types` via {py:mod}`plone.api`. It holds convenience methods to make the get and set of a record easy:

```{code-block} python

from plone import api

api.portal.get_registry_record('plone.displayed_types')
api.portal.set_registry_record('plone.smtp_host', 'my.mail.server')
```

Often seen in code from before the time of plone.api, is the access of the registry by `zope.component.getUtility`.

```{code-block} python

from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)
displayed_types = registry.get('plone.displayed_types')
```

The value of the record `displayed_types` is the tuple `('Image', 'File', 'Link', 'News Item', 'Folder', 'Document', 'Event', 'talk')`


## A UI for custom registry records

Now let's add our own custom settings:

- Is talk submission open or closed?
- Which rooms are available for talks?

While we're at it we can also add new settings `types_of_talk` and `audiences` that we will use later for the fields `type_of_talk` and `audience`.

To define custom records you write the same type of schema as you already did for content types or for behaviors:

Add a file {file}`browser/controlpanel.py`:

```{code-block} python
:linenos:

from zope import schema
from zope.interface import Interface

import json

VOCABULARY_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "titles": {
                            "type": "object",
                            "properties": {
                                "lang": {"type": "string"},
                                "title": {"type": "string"},
                            }
                        },
                    }
                }
            }
        },
    }
)


class IPloneconfSettings(Interface):

    talk_submission_open = schema.Bool(
        title="Allow talk submission",
        description="Allow the submission of talks for anonymous user",
        default=False,
        required=False,
    )

    types_of_talk = schema.JSONField(
        title="Types of Talk",
        description="Available types of a talk",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "talk",
                "titles": {
                    "en": "Talk",
                    "de": "Vortrag",
                }
            },
            {
                "token": "lightning-talk",
                "titles": {
                    "en": "Lightning-Talk",
                    "de": "Lightning-Talk",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'types_of_talk',
        frontendOptions={
            "widget": 'vocabularyterms',
        })

    audiences = schema.JSONField(
        title="Audience",
        description="Available audiences of a talk",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "beginner",
                "titles": {
                    "en": "Beginner",
                    "de": "Anfänger",
                }
            },
            {
                "token": "advanced",
                "titles": {
                    "en": "Advanced",
                    "de": "Fortgeschrittene",
                }
            },
            {
                "token": "professional",
                "titles": {
                    "en": "Professional",
                    "de": "Profi",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'audiences',
        frontendOptions={
            "widget": 'vocabularyterms',
        })

    rooms = schema.JSONField(
        title="Rooms",
        description="Available rooms of the conference",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "101",
                "titles": {
                    "en": "101",
                    "de": "101",
                }
            },
            {
                "token": "201",
                "titles": {
                    "en": "201",
                    "de": "201",
                }
            },
            {
                "token": "auditorium",
                "titles": {
                    "en": "Auditorium",
                    "de": "Auditorium",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'rooms',
        frontendOptions={
            "widget": 'vocabularyterms',
        })
```

Motivation for the use of schema.JSONField instead of schema.List:

The options for the types of a talk, the room and the audience may change. A modification of the feeding vocabulary would mean that already used options are no longer available which would corrupt the data of the concerned talks. So we care for a futureproof vocabulary with JSONFields that mean to store a vocabulary source in registry that is a list of dictionaries with keys that never change and values that are free to modify if necessary.


We now register this schema `IPloneconfSettings` for the registry.
Add the following to {file}`profiles/default/registry/main.xml`.
With this statement the registry is extended by one record per `IPloneconfSettings` schema field.

```xml
<records interface="ploneconf.site.browser.controlpanel.IPloneconfControlPanel"
         prefix="ploneconf" />
```

```{note}
The `prefix` allows you to access these records with a shortcut:
You can use `ploneconf.rooms` instead of `ploneconf.site.browser.controlpanel.IPloneconfControlPanel.room`.
```

After reinstalling the package (to apply the registry changes) you can access and modify these registry records as described above:

Either use <http://localhost:8080/Plone/portal_registry> or python:

```python
from plone import api

api.portal.get_registry_record('ploneconf.rooms')
```

````{note}
In training code `ploneconf.site` we use `Python` to define the registry records.
Alternatively you could also add these registry entries with Generic Setup.

The following creates a new entrie `ploneconf.talk_submission_open` with Generic Setup:

```{code-block} xml
:linenos:

<record name="ploneconf.talk_submission_open">
  <field type="plone.registry.field.Bool">
    <title>Allow talk submission</title>
    <description>Allow the submission of talks for anonymous users</description>
    <required>False</required>
  </field>
  <value>False</value>
</record>
```

When creating a new vanilla Plone instance, a lot of default settings are created that way. See <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml> to see how {py:mod}`Products.CMFPlone` registers values.
````

## Add a custom control panel

Now you will add a custom control panel to edit all setting related to our package with a nice UI.

To register a controlpanel for the frontend and Plone Classic you need quite a bit of boiler-plate:

```{code-block} python
:emphasize-lines: 1-2, 4, 147-165
:linenos:

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone import schema
from zope.component import adapter
from zope.interface import Interface

import json

VOCABULARY_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "titles": {
                            "type": "object",
                            "properties": {
                                "lang": {"type": "string"},
                                "title": {"type": "string"},
                            }
                        },
                    }
                }
            }
        },
    }
)


class IPloneconfSettings(Interface):

    talk_submission_open = schema.Bool(
        title="Allow talk submission",
        description="Allow the submission of talks for anonymous user",
        default=False,
        required=False,
    )

    types_of_talk = schema.JSONField(
        title="Types of Talk",
        description="Available types of a talk",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "talk",
                "titles": {
                    "en": "Talk",
                    "de": "Vortrag",
                }
            },
            {
                "token": "lightning-talk",
                "titles": {
                    "en": "Lightning-Talk",
                    "de": "Lightning-Talk",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'types_of_talk',
        frontendOptions={
            "widget": 'vocabularyterms',
        })

    audiences = schema.JSONField(
        title="Audience",
        description="Available audiences of a talk",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "beginner",
                "titles": {
                    "en": "Beginner",
                    "de": "Anfänger",
                }
            },
            {
                "token": "advanced",
                "titles": {
                    "en": "Advanced",
                    "de": "Fortgeschrittene",
                }
            },
            {
                "token": "professional",
                "titles": {
                    "en": "Professional",
                    "de": "Profi",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'audiences',
        frontendOptions={
            "widget": 'vocabularyterms',
        })

    rooms = schema.JSONField(
        title="Rooms",
        description="Available rooms of the conference",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={"items": [
            {
                "token": "101",
                "titles": {
                    "en": "101",
                    "de": "101",
                }
            },
            {
                "token": "201",
                "titles": {
                    "en": "201",
                    "de": "201",
                }
            },
            {
                "token": "auditorium",
                "titles": {
                    "en": "Auditorium",
                    "de": "Auditorium",
                }
            },
        ]},
        missing_value={"items": []},
    )
    directives.widget(
        'rooms',
        frontendOptions={
            "widget": 'vocabularyterms',
        })


class PloneconfRegistryEditForm(RegistryEditForm):
    schema = IPloneconfSettings
    schema_prefix = 'ploneconf'
    label = 'Ploneconf Settings'


class PloneConfControlPanelFormWrapper(ControlPanelFormWrapper):
    form = PloneconfRegistryEditForm


@adapter(Interface, Interface)
class PloneConfRegistryConfigletPanel(RegistryConfigletPanel):
    """frontend control panel configlet"""
    schema = IPloneconfSettings
    schema_prefix = 'ploneconf'
    configlet_id = 'ploneconf-controlpanel'
    configlet_category_id = 'Products'
    title = 'Ploneconf Settings'
    group = 'Products'

```

You also need to register these in {file}`browser/configure.zcml`:

```{code-block} xml
:linenos:

<browser:page
    name="ploneconf-controlpanel"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    class=".controlpanel.PloneConfControlPanelFormWrapper"
    permission="cmf.ManagePortal"
    layer="ploneconf.site.interfaces.IPloneconfSiteLayer"
    />

<adapter
    factory="ploneconf.site.browser.controlpanel.PloneConfRegistryConfigletPanel"
    name="ploneconf-controlpanel" />
```

Finally you also need to register it with Generic Setup to let the configlet get listed in `Site Setups` panels list.
Add a file {file}`profiles/default/controlpanel.xml`:

```{code-block} xml
:linenos:

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

In frontend it is at <http://localhost:3000/controlpanel/ploneconf-controlpanel>

```{figure} _static/volto_ploneconf_controlpanel.png
```


````{note}
A short remark on the frontend widget. As we want the `VocabularyTermsWidget` to be applied, we give already in our backend schema of the control panel the hint with a so called tagged value which frontend widget we want to be applied for the three control panel fields. So no widget registration in frontend app needed.

```python
directives.widget(
    'types_of_talk',
    frontendOptions={
        "widget": 'vocabularyterms',
    })
```
````

As you see in the opened control panel configlet for the ploneconf.site package, the registry records can be modified and their order can be changed.

## Vocabularies

Now the custom settings are stored in the registry and we can modify them in a nice way as admins.
We still need to use these options in talks.

To do so we turn them into vocabularies.

Vocabularies are often used for selection fields. They have many benefits:

- They allow you to separate the select options values from the content type schema. Which means that they can be edited via UI like seen before.
- A vocabulary can even be dynamically, the available options can change depending on existing content, the role of the user or even the time of day.

Create a file {file}`vocabularies.py` and write code that generates vocabularies from these settings:

```{code-block} python
:linenos:

from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def TalkTypesVocabulary(context):
    name = "ploneconf.types_of_talk"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get('items', [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems([[item['token'], item['token'], item['titles'][lang]] for item in items])


@provider(IVocabularyFactory)
def AudiencesVocabulary(context):
    name = "ploneconf.audiences"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get('items', [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems([[item['token'], item['token'], item['titles'][lang]] for item in items])


@provider(IVocabularyFactory)
def RoomsVocabularyFactory(context):
    name = "ploneconf.rooms"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get('items', [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems([[item['token'], item['token'], item['titles'][lang]] for item in items])
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
````

```{seealso}
Plone documentation **Vocabularies** <https://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html>
```


## Using vocabularies in a schema

To use a vocabulary in a schema replace `values` with `vocabulary` and point to the vocbulary by name:

```{code-block} python
:emphasize-lines: 3
:linenos:

type_of_talk = schema.Choice(
    title=_(u'Type of talk'),
    vocabulary='ploneconf.types_of_talk',
    required=True,
)
```

Don't forget to add the new field `room` now.

Edit {file}`content/talk.py`:

```{code-block} python
:emphasize-lines: 21, 35, 83-87
:linenos:

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
from plone import schema
from zope.interface import implementer


class ITalk(model.Schema):
    """Define a content type schema for Talks"""

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

    room = schema.Choice(
        title=_(u'Room'),
        vocabulary='ploneconf.rooms',
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
:linenos:

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


## Summary

- You successfully combined the registry, a controlpanel and vocabularies to allow managing field options by admins.
- It seems like a lot but you will certainly use dynamic vocabularies, controlpanels and the registry in all of your future Plone projects in one way or another.
