---
myst:
  html_meta:
    "description": "How to make your Plone add-on configurable"
    "property=og:description": "How to make your Plone add-on configurable"
    "property=og:title": "Registry, control panels and vocabularies"
    "keywords": "registry, control panel, vocabulary, select, options, configuration, settings"
---

(registry-label)=

# Registry, control panels and vocabularies

```{card} 
In this part you will:

- Store custom settings in the registry
- Create a control panel to manage custom settings
- Create options in fields as vocabularies
- Training story: Assign talks to rooms

Topics covered:

- plone.app.registry
- Vocabularies
- Control panels
```

````{card} Backend chapter

Checkout `ploneconf.site` at tag "events":

```shell
git checkout events
```

The code at the end of the chapter:

```shell
git checkout vocabularies
```

More info in {doc}`code`
````


## Introduction

Do you remember the fields `audience` and `type_of_talk` in the talk content type?
The schema previously hard-coded several options for selection.

Next, you will add a field to assign talks to a room.
The room names change each year for the conference, so site administrators need to edit them.

Additionally, admins should be able to edit the options for `audience` and `type_of_talk`, making it possible to add options like _Lightning Talks_!

By combining the registry, a control panel and vocabularies you can make rooms configurable options.

To achieve this you first need to get to know the registry.


## The registry

The registry stores and retrieves values in records.
Each record consists of the actual value, along with a field that describes the record in more detail.
You can interact with the registry using Python dictionary-style operations to get and set values.

Since Plone 5 the registry stores all global settings.
Plone provides the registry through [plone.registry](https://pypi.org/project/plone.registry) and offers a user interface for interaction via [plone.app.registry](https://pypi.org/project/plone.app.registry).

Most settings in {guilabel}`Site Setup` reside in the registry.
You can modify them directly through its UI.

Open http://localhost:8080/Plone/portal_registry and filter for `displayed_types`.
Modify the content types shown in the navigation and site map directly.
These values match those in http://localhost:8080/Plone/@@navigation-controlpanel, where the form is customized for better usability.

```{note}
This UI for the registry is not yet available in the frontend.
```

## Registry records

In {doc}`volto_frontpage` you already added a criterion usable for listing blocks in {file}`profiles/default/registry/querystring.xml`.
This setting is stored in the registry.

Examine the existing values in the registry.

Go to http://localhost:3000/controlpanel/navigation and add `talk` to the field {guilabel}`Displayed content types`.
Talks in the root will now show up in the navigation.
This setting is stored in the registry record `plone.displayed_types`.


## Accessing and modifying records in the registry

In Python you can access the registry record with the key `plone.displayed_types` via `plone.api.portal`.
It holds convenience functions to get and set a record:

```{code-block} python

from plone import api

api.portal.get_registry_record('plone.displayed_types')
api.portal.set_registry_record('plone.smtp_host', 'my.mail.server')
```

For more information see `plone.api.portal` documentation: {ref}`plone6docs:portal-get-registry-record-example`.

The access of the registry by `zope.component.getUtility` is often seen in code from before the time of `plone.api`.

```{code-block} python

from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)
displayed_types = registry.get('plone.displayed_types')
```

The value of the record `displayed_types` is the tuple `('Image', 'File', 'Link', 'News Item', 'Folder', 'Document', 'Event', 'talk')`.

## Custom registry records

Now add custom settings:

- Is talk submission open or closed?
- Which rooms are available for talks?

Additionally, new settings `types_of_talk` and `audiences` can be added for use later in the fields `type_of_talk` and `audience`.

To define custom records, you write the same type of schema as you already did for content types or for behaviors:

Add a file {file}`controlpanel/controlpanel.py`:

```{code-block} python
:linenos:

from plone import schema
from plone.autoform import directives
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
                            },
                        },
                    },
                },
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
        default={
            "items": [
                {
                    "token": "talk",
                    "titles": {
                        "en": "Talk",
                        "de": "Vortrag",
                    },
                },
                {
                    "token": "lightning-talk",
                    "titles": {
                        "en": "Lightning-Talk",
                        "de": "Lightning-Talk",
                    },
                },
            ]
        },
        missing_value={"items": []},
    )
    directives.widget(
        "types_of_talk",
        frontendOptions={
            "widget": "vocabularyterms",
        },
    )

    audiences = schema.JSONField(
        title="Audience",
        description="Available audiences of a talk",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={
            "items": [
                {
                    "token": "beginner",
                    "titles": {
                        "en": "Beginner",
                        "de": "Anfänger",
                    },
                },
                {
                    "token": "advanced",
                    "titles": {
                        "en": "Advanced",
                        "de": "Fortgeschrittene",
                    },
                },
                {
                    "token": "professional",
                    "titles": {
                        "en": "Professional",
                        "de": "Profi",
                    },
                },
            ]
        },
        missing_value={"items": []},
    )
    directives.widget(
        "audiences",
        frontendOptions={
            "widget": "vocabularyterms",
        },
    )

    rooms = schema.JSONField(
        title="Rooms",
        description="Available rooms of the conference",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={
            "items": [
                {
                    "token": "101",
                    "titles": {
                        "en": "101",
                        "de": "101",
                    },
                },
                {
                    "token": "201",
                    "titles": {
                        "en": "201",
                        "de": "201",
                    },
                },
                {
                    "token": "auditorium",
                    "titles": {
                        "en": "Auditorium",
                        "de": "Auditorium",
                    },
                },
            ]
        },
        missing_value={"items": []},
    )
    directives.widget(
        "rooms",
        frontendOptions={
            "widget": "vocabularyterms",
        },
    )

```

The motivation to use `schema.JSONField` instead of `schema.List` is described as follows.

The options for the types of a talk, the room and the audience may change.
A modification of the feeding vocabulary would mean that already used options are no longer available, which would corrupt the data of the concerned talks.
We can "future-proof" this vocabulary with JSONFields that store a vocabulary source in the registry.
This vocabulary is a list of dictionaries, with keys that never change, and values that may be modified when necessary.
See the default values to understand what is stored in the registry:
Example `types_of_talk`:

```{code-block} python
[
    {
        "token": "talk",
        "titles": {
            "en": "Talk",
            "de": "Vortrag",
        },
    },
    {
        "token": "lightning-talk",
        "titles": {
            "en": "Lightning-Talk",
            "de": "Lightning-Talk",
        },
    },
]
```

If the name `Lightning-Talk` needs to be updated to `Short talks`, the talks categorized as lightning talks will still display correctly.
This is because the value stored in the talks is the token `lightning-talk`, which remains unchanged.

A new field `JSONField` has been introduced.
This field is used to store JSON data for the content.
A schema defines the valid structure of the field values.

```python
    directives.widget(
        "audiences",
        frontendOptions={
            "widget": "vocabularyterms",
        },
    )
```

The `frontendOptions` forces Volto to display on editing the field with a widget prepared for vocabulary terms.
More correct, it forces Volto to lookup the widget in `Volto's` widget mapping to find the corresponding widget.


The schema `IPloneconfSettings` is now registered for the registry.
Add the following to {file}`profiles/default/registry/main.xml`.
Each field in the `IPloneconfSettings` schema adds a corresponding record to the registry.

```xml
<?xml version="1.0"?>
<registry
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="ploneconf.site">

  <records
      interface="ploneconf.site.controlpanel.controlpanel.IPloneconfSettings"
      prefix="ploneconf" />

</registry>
```

```{note}
The `prefix` allows you to access these records with a shortcut:
You can use `ploneconf.rooms` instead of `ploneconf.site.controlpanel.controlpanel.IPloneconfSettings.rooms`.
```

After reinstalling the package to apply the registry changes, you can access and modify these registry records as described before.
Either use http://localhost:8080/Plone/portal_registry or Python:

```python
from plone import api

api.portal.get_registry_record('ploneconf.rooms')
```

`````{note}
In training code `ploneconf.site`, we use Python to define the registry records.
Alternatively you could add these registry entries with Generic Setup.

The following creates a new entry `ploneconf.talk_submission_open` with Generic Setup:

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

When creating a new vanilla Plone instance, a lot of default settings are created that way.
See https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml to see how {py:mod}`Products.CMFPlone` registers values.
`````


(controlpanel-label)=

## Add a custom control panel

Now you'll add a custom control panel to edit all settings related to the package with a user-friendly interface.

To register a control panel for the frontend, add the following `RegistryConfigletPanel` to {file}`controlpanel/controlpanel.py`.
The `RegistryConfigletPanel` uses the schema and will serve as a factory for a control panel configlet.

```{code-block} python
:emphasize-lines: 1-2, 16-25
:linenos:

from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter

# …

class IPloneconfSettings(Interface):
    talk_submission_open = schema.Bool(
        title="Allow talk submission",
        description="Allow the submission of talks for anonymous user",
        default=False,
        required=False,
    )

# …

@adapter(Interface, Interface)
class PloneConfRegistryConfigletPanel(RegistryConfigletPanel):
    """Volto control panel"""

    schema = IPloneconfSettings
    schema_prefix = "ploneconf"
    configlet_id = "ploneconf-controlpanel"
    configlet_category_id = "Products"
    title = "Ploneconf Settings"
    group = "Products"
```


If you want to use this control panel in Classic UI as well, see https://2022.training.plone.org/mastering-plone/registry.html#add-a-custom-control-panel, which also handles the Classic UI version.

The factory is used in {file}`controlpanel/configure.zcml` for a named adapter:

```{code-block} xml
:linenos:

  <adapter
    factory="ploneconf.site.controlpanel.controlpanel.PloneConfRegistryConfigletPanel"
    name="ploneconf-controlpanel" />
```

Finally register in {file}`profiles/default/controlpanel.xml` the configlet with Generic Setup so that it gets listed in the {guilabel}`Site Setups` panels list (often called 'control panel').
Therefore the named adapter "ploneconf-controlpanel" provides the schema for the form of the control panel configlet.

```{code-block} xml
:linenos:
:emphasize-lines: 9

<?xml version="1.0" encoding="utf-8"?>
<object name="portal_controlpanel">
  <configlet action_id="ploneconf-controlpanel"
             appId="ploneconf-controlpanel"
             category="Products"
             title="Ploneconf Settings"
             visible="True"
  >
    <permission>Manage portal</permission>
  </configlet>
</object>

```

After applying the profile (for example, by reinstalling the package), your control panel configlet shows up on http://localhost:3000/controlpanel/controlpanel

```{figure} _static/volto_ploneconf_controlpanel_overview.png
```


```{figure} _static/volto_ploneconf_controlpanel.png
```

As you can see in the control panel configlet for the `ploneconf.site` package, the entries can be modified and reordered.
Changes are reflected in the registry because the configlet is registered with the schema of the registry fields.

````{note}
**Frontend widgets**

A short remark on the frontend widget.
We want the `VocabularyTermsWidget` to be applied.
Thus we specify a hint, using a so-called "tagged value", the name of the frontend widget to be applied for the three control panel fields in our backend schema.
Thus no widget registration in the frontend app is needed.

```python
directives.widget(
    "types_of_talk",
    frontendOptions={
        "widget": "vocabularyterms",
    },
)
```

This is also the way you would configure a content type schema, where you may want to override the default widget.

A widget component in your frontend package would be mapped to a key "mywidget".
In your content type schema you would add a widget directive with
`frontendOptions={"widget": "mywidget"}`
````

(vocabularies-label)=

## Vocabularies

Now the custom settings are stored in the registry and can be modified conveniently by site administrators.
These options still need to be used in talks.

To achieve this, turn them into vocabularies.

Vocabularies are often used for selection fields.
They have many benefits:

- They enable you to separate the select option values from the content type schema.
  Users can edit vocabularies through the UI.
- Developers can set vocabularies dynamically.
  The available options may vary based on existing content, the user's role, or even the time of day.

Create a file {file}`vocabularies/talk.py` and write code that generates vocabularies from these settings:

```{code-block} python
:linenos:
:emphasize-lines: 13-15

from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def TalkTypesVocabulary(context):
    name = "ploneconf.types_of_talk"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get("items", [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems(
        [[item["token"], item["token"], item["titles"][lang]] for item in items]
    )


@provider(IVocabularyFactory)
def AudiencesVocabulary(context):
    name = "ploneconf.audiences"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get("items", [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems(
        [[item["token"], item["token"], item["titles"][lang]] for item in items]
    )


@provider(IVocabularyFactory)
def RoomsVocabularyFactory(context):
    name = "ploneconf.rooms"
    registry_record_value = api.portal.get_registry_record(name)
    items = registry_record_value.get("items", [])
    lang = api.portal.get_current_language()
    return SimpleVocabulary.fromItems(
        [[item["token"], item["token"], item["titles"][lang]] for item in items]
    )
```

The `SimpleVocabulary.fromItems()` is a method that takes the list of dictionaries of vocabulary terms

```python
[
    {
        "token": "talk",
        "titles": {
            "en": "Talk",
            "de": "Vortrag",
        },
    },
    {
        "token": "lightning-talk",
        "titles": {
            "en": "Lightning-Talk",
            "de": "Lightning-Talk",
        },
    },
]
```

and creates a Zope vocabulary.
This `SimpleVocabulary` instance has methods that Plone uses to display select widgets, display the rendered content type instance according the user language, etc..

You can now register these vocabularies as named utilities in {file}`vocabularies/configure.zcml`:

```xml

<utility
    name="ploneconf.types_of_talk"
    component="ploneconf.site.vocabularies.talk.TalkTypesVocabulary" />
<utility
    name="ploneconf.audiences"
    component="ploneconf.site.vocabularies.talk.AudiencesVocabulary" />
<utility
    name="ploneconf.rooms"
    component="ploneconf.site.vocabularies.talk.RoomsVocabularyFactory" />
```

From now on you can use these vocabulary by referring to their name, for example, `ploneconf.rooms`.

```{note}
- Plone comes with many useful named vocabularies that you can use in your own projects, for example `plone.app.vocabularies.Users` or `plone.app.vocabularies.PortalTypes`.

- See <https://github.com/plone/plone.app.vocabularies/> for a list of vocabularies.

- We turn the values from the registry into a dynamic `SimpleVocabulary` that can be used in the schema.

- You could use the context with which the vocabulary is called or the request (using `getRequest` from `zope.globalrequest`) to constrain the values in the vocabulary.
```

```{seealso}
Plone documentation [Vocabularies](https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html).
```

## Using vocabularies in a schema

To use a vocabulary in a schema field, replace the attribute `values` with `vocabulary`, and point to a vocabulary by its name:

```{code-block} python
:emphasize-lines: 3
:linenos:

type_of_talk = schema.Choice(
    title='Type of talk',
    vocabulary='ploneconf.types_of_talk',
    required=True,
)
```

Don't forget to add the new field `room`.

Edit {file}`content/talk.py`:

```{code-block} python
:emphasize-lines: 19, 33, 81-85
:linenos:

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


class ITalk(model.Schema):
    """Dexterity-Schema for Talks"""

    directives.widget(type_of_talk=RadioFieldWidget)
    type_of_talk = schema.Choice(
        title="Type of talk",
        vocabulary="ploneconf.types_of_talk",
        required=True,
    )

    details = RichText(
        title="Details",
        description="Description of the talk (max. 2000 characters)",
        max_length=2000,
        required=True,
    )

    directives.widget(audience=CheckBoxFieldWidget)
    audience = schema.Set(
        title="Audience",
        value_type=schema.Choice(
            vocabulary="ploneconf.audiences",
        ),
        required=False,
    )

    speaker = schema.TextLine(
        title="Speaker",
        description="Name (or names) of the speaker",
        required=False,
    )

    company = schema.TextLine(
        title="Company",
        required=False,
    )

    email = Email(
        title="Email",
        description="Email address of the speaker",
        required=False,
    )

    website = schema.TextLine(
        title="Website",
        required=False,
    )

    twitter = schema.TextLine(
        title="Twitter name",
        required=False,
    )

    github = schema.TextLine(
        title="Github username",
        required=False,
    )

    image = NamedBlobImage(
        title="Image",
        description="Portrait of the speaker",
        required=False,
    )

    speaker_biography = RichText(
        title="Speaker Biography (max. 1000 characters)",
        max_length=1000,
        required=False,
    )

    room = schema.Choice(
        title="Room",
        vocabulary="ploneconf.rooms",
        required=False,
    )


@implementer(ITalk)
class Talk(Container):
    """Talk instance class"""
```

## Adjust frontend according schema changes

With the new key value pairs (token/title) we adjust the component accordingly:

```jsx
      {content.audience?.map((item) => {
        let color = color_mapping[item.token] || 'green';
        return (
          <Label key={item.token} color={color}>
            {item.title}
          </Label>
        );
      })}
```

One tiny thing is still missing: We should display the room.

Modify {file}`frontend/src/components/Views/Talk.jsx` an add this after the `When` component:

```{code-block}
:emphasize-lines: 6

    {content.room && (
      <>
        <Header dividing sub>
          Where
        </Header>
        <p>{content.room.title}</p>
      </>
    )}
```

````{dropdown} The complete TalkView
:animate: fade-in-slide-down
:icon: question

```jsx
import {
  Container as SemanticContainer,
  Header,
  Image,
  Label,
  Segment,
} from 'semantic-ui-react';
import { flattenToAppURL } from '@plone/volto/helpers';
import { When } from '@plone/volto/components/theme/View/EventDatesInfo';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const color_mapping = {
    beginner: 'green',
    advanced: 'yellow',
    professional: 'purple',
  };
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.title}: </span>
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
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
          <>
            <Header dividing sub>
              Audience
            </Header>
            {content.audience?.map((item) => {
              let color = color_mapping[item.token] || 'green';
              return (
                <Label key={item.token} color={color}>
                  {item.title}
                </Label>
              );
            })}
          </>
        )}
      </Segment>
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        {content.website ? (
          <p>
            <a href={content.website}>{content.company || content.website}</a>
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
            X:{' '}
            <a href={`https://x.com/${content.twitter}`}>
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
        <Image
          src={flattenToAppURL(content.image?.scales?.preview?.download)}
          size="small"
          floated="right"
          alt={content.speaker}
          avatar
        />
        {content.speaker_biography && (
          <div
            dangerouslySetInnerHTML={{
              __html: content.speaker_biography.data,
            }}
          />
        )}
      </Segment>
    </Container>
  );
};
export default TalkView;
```

````

## Summary

- You successfully combined the registry, a control panel, and vocabularies to enable site administrators to manage field options.
- It seems like a lot, but you will certainly use dynamic vocabularies, control panels, and the registry in many of your Plone projects in one way or another.
