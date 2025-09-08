---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-registry-label)=

# Manage Settings with Registry, Control Panels and Vocabularies

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout dexterity_3
```

Code for the end of this chapter:

```shell
git checkout registry
```

{doc}`code`
````

In this part you will:

- Store a custom setting in a registry
- Create a control panel using z3c.form to allow setting that value

Topics covered:

- plone.app.registry
- control panels

## The Registry

The registry is used to get and set values stored in records. Each record contains the actual value, as well as a field that describes the record in more detail. It has a nice dict-like API.

All global settings in Plone 5 are stored in the registry.

The registry itself is provided by [plone.registry](https://pypi.org/project/plone.registry) and the UI to interact with it by [plone.app.registry](https://pypi.org/project/plone.app.registry)

Almost all settings in `/plone_control_panel` are actually stored in the registry and can be modified using its UI directly.

Open <http://localhost:8080/Plone/portal_registry> and filter for `displayed_types`. You see can modify the content types that should be shown in the navigation and site map. The values are the same as in <http://localhost:8080/Plone/@@navigation-controlpanel> but the later form is customized for usability.

## A setting

Let's store two values in the registry:

- The date of the conference
- Is talk submission open or closed

You cannot create values through the web; instead, you need to register them using Generic Setup.

Open the file {file}`profiles/default/registry.xml`. You already registered several new settings in there:

- You enabled self registration
- You stored a site logo
- You registered additional criteria usable for Collections

Adding the following code to {file}`registry.xml`. This creates a new value in the registry upon installation of the package.

```xml
<record name="ploneconf.talk_submission_open">
  <field type="plone.registry.field.Bool">
    <title>Allow talk submission</title>
    <description>Allow the submission of talks for anonymous users</description>
    <required>False</required>
  </field>
  <value>False</value>
</record>
```

When creating a new site a lot of settings are created in the same way. See <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml> to see how {py:mod}`Products.CMFPlone` registers values.

```xml
<record name="ploneconf.date_of_conference">
  <field type="plone.registry.field.Date">
    <title>First day of the conference</title>
    <required>False</required>
  </field>
  <value>2016-10-17</value>
</record>
```

## Accessing and modifying values in the registry

In Python you can access the registry like this:

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)
start = registry.get('ploneconf.date_of_conference')
```

{py:mod}`plone.api` holds methods to make this even easier:

```python
from plone import api
api.portal.get_registry_record('ploneconf.date_of_conference')
api.portal.set_registry_record('ploneconf.talk_submission_open', True)
```

## Add a custom control panel

When you want to add a custom control panel it is usually more convenient to register the fields, not manually as above, but as fields in a schema, similar to that of a content type schema.

For this you define an interface for the schema and a view that auto-generates a form from the schema. In {file}`browser/configure.zcml` add:

```xml
<browser:page
    name="ploneconf-controlpanel"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    class=".controlpanel.PloneconfControlPanelView"
    permission="cmf.ManagePortal"
    />
```

Add a file {file}`browser/controlpanel.py`:

```python
# -*- coding: utf-8 -*-
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IPloneconfControlPanel(Interface):

    date_of_conference = schema.Date(
        title=u'First day of the conference',
        required=False,
        default=date(2016, 10, 17),
    )

    talk_submission_open = schema.Bool(
        title=u'Allow talk submission',
        description=u'Allow the submission of talks for anonymous user',
        default=False,
        required=False,
    )


class PloneconfControlPanelForm(RegistryEditForm):
    schema = IPloneconfControlPanel
    schema_prefix = "ploneconf"
    label = u'Ploneconf Settings'


PloneconfControlPanelView = layout.wrap_form(
    PloneconfControlPanelForm, ControlPanelFormWrapper)
```

With this way of using fields you don't have to register the values in {file}`registry.xml`. Instead, you have to register the interface:

```xml
<records interface="ploneconf.site.browser.controlpanel.IPloneconfControlPanel"
         prefix="ploneconf" />
```

After reinstalling the package (to load the registry entry) you can access the control panel at <http://localhost:8080/Plone/@@ploneconf-controlpanel>.

To make it show up in the general control panel at <http://localhost:8080/Plone/@@overview-controlpanel> you have to register it with GenericSetup.
Add a file {file}`profiles/default/controlpanel.xml`:

```xml
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

Again, after applying the profile (reinstall the package or write a upgrade-step) your control panel shows up in <http://localhost:8080/Plone/@@overview-controlpanel>.

## Vocabularies

Do you remember the field `rooms`? We provided several options to chose from.
But who says that the next conference will have the same rooms?
These values should be configurable by the admin.
The admin could go to the Dexterity control panel and change the values but we will use a different approach.
We will allow the rooms to be added in the control panel and use these values in the talk-schema by registering a vocabulary.

Add a new field to {py:class}`IPloneconfControlPanel`:

```{code-block} python
:linenos:

rooms = schema.Tuple(
    title=u'Available Rooms for the conference',
    default=(u'101', u'201', u'Auditorium'),
    missing_value=None,
    required=False,
    value_type=schema.TextLine(),
)
```

Create a file {file}`vocabularies.py` and write the vocabulary:

```{code-block} python
:linenos:

# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory

@provider(IVocabularyFactory)
def RoomsVocabularyFactory(context):
    values = api.portal.get_registry_record('ploneconf.rooms')
    return safe_simplevocabulary_from_values(values)
```

You can now register this vocabulary as a named utility in {file}`configure.zcml` as `ploneconf.site.vocabularies.Rooms`:

```xml
<utility
    name="ploneconf.site.vocabularies.Rooms"
    component="ploneconf.site.vocabularies.RoomsVocabularyFactory" />
```

From now on you can use this vocabulary by only referring to its name `ploneconf.site.vocabularies.Rooms`.

Note:

- Plone comes with many useful vocabularies that you can use in your own projects. See <https://github.com/plone/plone.app.vocabularies/> for a list of them.

- We turn the values from the registry into a dynamic `SimpleVocabulary` that can be used in the schema.

- You could use the context with which the vocabulary is called or the request (using `getRequest` from `from zope.globalrequest import getRequest`) to constrain the values in the vocabulary.

- We use the handy helper method `safe_simplevocabulary_from_values` to create the vocabulary since the `token` of a `SimpleTerm` in a `SimpleVocabulary` needs to be bytes, not unicode.

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

Use the new vocabulary in the talk schema. Edit {file}`content/talk.xml`

```{code-block} xml
:emphasize-lines: 7
:linenos:

<field name="room"
       type="zope.schema.Choice"
       form:widget="z3c.form.browser.radio.RadioFieldWidget"
       security:write-permission="cmf.ReviewPortalContent">
  <description></description>
  <title>Room</title>
  <vocabulary>ploneconf.site.vocabularies.Rooms</vocabulary>
</field>
```

In a Python schema, that would look like this:

```python
directives.widget(room=RadioFieldWidget)
room = schema.Choice(
    title=_(u'Room'),
    vocabulary='ploneconf.site.vocabularies.Rooms',
    required=False,
)
```

An admin can now configure the rooms available for the conference.

We could use the same pattern for the fields `type_of_talk` and `audience`.

```{seealso}
<https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html>
```
