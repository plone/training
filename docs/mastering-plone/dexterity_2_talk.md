---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(dexterity-2-talk-label)=

# Dexterity II: Talks

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout volto
```

Code for the end of this chapter:

```shell
git checkout talks
```
````

In this part you will solve the following task:

- Create a contenttype 'talk' to store all the data required for a talk

Topics covered:

- Registration and configuration of content types
- Schema
- Fields
- Widgets

## The type registration

Add a new file {file}`types.xml` to your add-on package in {file}`profiles/default/`.
That is {file}`backend/src/ploneconf.site/sources/ploneconf/site/profiles/default/types.xml`

The following lines will tell Plone that there is a new content type defined.

```xml
<?xml version="1.0"?>
<object name="portal_types" meta_type="Plone Types Tool">
  <object name="talk" meta_type="Dexterity FTI"/>
</object>
```

Plone will now expect a file {file}`profiles/default/types/talk.xml` and will register that as a new content type.

## The FTI

Add the file `ploneconf/site/profiles/default/types/talk.xml`.
Note that there is a file _types_ and a folder _types_.

This is the **Factory Type Information** that holds the configuration for the content type **talk**.

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<object name="talk" meta_type="Dexterity FTI" i18n:domain="plone"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n">
 <property name="title" i18n:translate="">Talk</property>
 <property name="description" i18n:translate=""></property>
 <property name="icon_expr">string:${portal_url}/document_icon.png</property>
 <property name="factory">talk</property>
 <property name="add_view_expr">string:${folder_url}/++add++talk</property>
 <property name="link_target"></property>
 <property name="immediate_view">view</property>
 <property name="global_allow">True</property>
 <property name="filter_content_types">True</property>
 <property name="allowed_content_types"/>
 <property name="allow_discussion">False</property>
 <property name="default_view">view</property>
 <property name="view_methods">
  <element value="view"/>
 </property>
 <property name="default_view_fallback">False</property>
 <property name="add_permission">cmf.AddPortalContent</property>
 <property name="klass">ploneconf.site.content.talk.Talk</property>
 <property name="schema">ploneconf.site.content.talk.ITalk</property>
 <property name="behaviors">
  <element value="plone.dublincore"/>
  <element value="plone.namefromtitle"/>
  <element value="plone.versioning" />
 </property>
 <property name="model_source"></property>
 <property name="model_file"></property>
 <property name="schema_policy">dexterity</property>
 <alias from="(Default)" to="(dynamic view)"/>
 <alias from="edit" to="@@edit"/>
 <alias from="sharing" to="@@sharing"/>
 <alias from="view" to="(selected layout)"/>
 <action title="View" action_id="view" category="object" condition_expr=""
    description="" icon_expr="" link_target="" url_expr="string:${object_url}"
    visible="True">
  <permission value="View"/>
 </action>
 <action title="Edit" action_id="edit" category="object" condition_expr=""
    description="" icon_expr="" link_target=""
    url_expr="string:${object_url}/edit" visible="True">
  <permission value="Modify portal content"/>
 </action>
</object>
```

Now our package has a new configuration for Generic Setup.
Generic Setup loads a lot of different types of configuration for the site from folder {file}`profiles/`.
This configuration is applied to your site upon installing the package.
This also means that you will need to re-install the package once we are finished with the talk.

But the type is not yet complete since the schema (`ploneconf.site.content.talk.ITalk`) and the class (`ploneconf.site.content.talk.Talk`) that are referenced in the FTI are not yet there.

## The schema

The schema holds the definition of the fields that the content type will offer to store data.

It is also the place where you would add widget options per field to control the display of fields.

In the FTI we referenced the Python path `ploneconf.site.content.talk.ITalk`.

The module {py:mod}`content` does not exist. Create a folder {file}`content` and add an empty {file}`__init__.py` in it.
From the training root that is {file}`backend/src/ploneconf.site/src/ploneconf/site/content/__init__.py`.

In this new folder add a file {file}`talk.py` with the following content:

```{code-block} python
:linenos:

from plone import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ITalk(model.Schema):
    """Dexterity-Schema for Talks"""

    directives.widget(type_of_talk=RadioFieldWidget)
    type_of_talk = schema.Choice(
        title='Type of talk',
        values=['Talk', 'Training', 'Keynote'],
        required=True,
    )

    details = RichText(
        title='Details',
        description='Description of the talk (max. 2000 characters)',
        max_length=2000,
        required=True,
    )

    directives.widget(audience=CheckBoxFieldWidget)
    audience = schema.Set(
        title='Audience',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
    )

    speaker = schema.TextLine(
        title='Speaker',
        description='Name (or names) of the speaker',
        required=False,
    )

    company = schema.TextLine(
        title='Company',
        required=False,
    )

    email = Email(
        title='Email',
        description='Email adress of the speaker',
        required=False,
    )

    website = schema.TextLine(
        title='Website',
        required=False,
    )

    twitter = schema.TextLine(
        title='Twitter name',
        required=False,
    )

    github = schema.TextLine(
        title='Github username',
        required=False,
    )

    image = NamedBlobImage(
        title='Image',
        description='Portrait of the speaker',
        required=False,
    )

    speaker_biography = RichText(
        title='Speaker Biography (max. 1000 characters)',
        max_length=1000,
        required=False,
    )


@implementer(ITalk)
class Talk(Container):
    """Talk instance class"""
```

The first class {py:class}`ITalk` is the schema for talks and defines quite a lot of different fields for different kinds of data.

- The fields in the schema are mostly from {py:mod}`zope.schema`.
- The most basic field is `schema.TextLine` which can store text.
- In the next chapter you will find a reference of all field-types available in Plone.
- The widget directives can be ignored by now, as we are implementing for a frontend app.
    The widget directives like above do control the rendering of the fields in Plone Classic.
    In the rare case that you need to tweak the rendering of a field in frontend, this can be done like described in {doc}`plone6docs:volto/recipes/widget`


```{eval-rst}
.. todo::

    * As a first step use a simplified schema without directives or vocabularies
    * Then add some simple widget-directives
    * In the sponsors-chapter discuss all fields, directives, permissions, defaults.
    * Extend to the final version like https://github.com/collective/ploneconf.site/pull/1/files in a later chapter

```

## The instance class

The second class {py:class}`Talk` in {file}`talk.py` will be the class of instances for each talk.
It inherits from {py:class}`Container` which is one of the default classes of dexterity.
{py:class}`Container` is used for items that can contain other items.
It does nothing so far but it can be useful later when we want to add methods or properties to it that can be used directly from a talk instance.

## Try the new type

Now all pieces should be in place and you can enable the new type `Talk`.

- Restart Plone (to load the new Python code and the changed zcml)
- You do not need to restart the Volto frontend since we did not do any changes there.
- Re-install the package ploneconf.site (deactivate and activate) to load the type registration and type configuration:
    Follow the link "SITE SETUP" in the bottom of the toolbar and switch to "Add-Ons".

Now instances of the new type can be added.
Please check that you can add a talk to your site.

```{figure} _static/dexterity_add_talk_frontend.png
Adding a talk in the frontend
```

- Test the type by adding a talk. Add some values in the fields, save it, look at the view and edit it again.
- Compare all the fields you see to the code in the schema.
- You can also make changes in the schema. After restarting the backend these changes are effective immediately.
- Find the tool `portal_types` in the ZMI http://localhost:8080/manage.
  Look at the FTI for type `talk` and inspect the configuration taken from the FTI.
  
  You can make changes to the FTI here. 
- A part of the configuration is also available in Plone control panels (SITE SETUP).
  For example the content types control panel `http://localhost:3000/controlpanel/dexterity-types` allows to add behaviors to content types.
  Please be aware that these changes are done on your site instance.
  You can use the browser UI, but it's the add-on package where you configure your content types.

The field values of your talk instance are listed.
In one of the next chapters we will create a custom view for the new type.


## Summary

- You created a custom content type.
- You can now control the data that will be stored for talks.
- You can reuse and adapt these examples to model data for your own use-cases.
- Next up: After looking at even more fields that are available in Plone, you will learn to change how talks are displayed.
