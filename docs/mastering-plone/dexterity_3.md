---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(dexterity-3-label)=

# Content types III: Sponsors

````{card} Backend chapter

Get the code! ({doc}`More info <code>`)


```shell
git checkout dexterity_upgrade_steps
```

````

Without sponsors, a conference would be hard to finance! Plus it is a good opportunity for Plone companies to advertise their services.

```{card}
In this part we will:

- Create a sponsor contenttype to manage sponsors
- Store non-visible information about the sponsor in the sponsor-type

Topics covered:

- Schema hint and directives
- Field permissions
- Vocabularies
```


## The Python schema

First we create the schema for the new content type.

Add a new file {file}`content/sponsor.py`.

```{code-block} python
:linenos:

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implementer


class ISponsor(model.Schema):
    """Dexterity Schema for Sponsors
    """

    level = schema.Choice(
        title='Sponsoring Level',
        vocabulary='ploneconf.sponsor_levels',
        required=True
    )

    text = RichText(
        title='Text',
        required=False
    )

    url = schema.URI(
        title='Link',
        required=False
    )

    fieldset('Images', fields=['logo', 'advertisement'])
    logo = namedfile.NamedBlobImage(
        title='Logo',
        required=False,
    )

    advertisement = namedfile.NamedBlobImage(
        title='Advertisement (Gold-sponsors and above)',
        required=False,
    )

    directives.read_permission(notes='cmf.ManagePortal')
    directives.write_permission(notes='cmf.ManagePortal')
    notes = RichText(
        title='Secret Notes (only for site-admins)',
        required=False
    )


@implementer(ISponsor)
class Sponsor(Container):
    """Sponsor instance class"""
```

Some things are notable here:

- {samp}`fieldset('Images', fields=['logo', 'advertisement'])` moves the two image fields to another tab.
- {samp}`directives.read_permission(...)` sets the read and write permission for the field `notes` to users who can add new members. Usually this permission is only granted to Site Administrators and Managers. We use it to store information that should not be publicly visible. Please note that {py:attr}`obj.notes` is still accessible in templates and Python.

```{seealso}
See the {ref}`plone6docs:backend-fields-reference-label` for a reference of all field-types and directives you can use in dexterity.
```

## The Factory Type Information, or FTI

Next, we create the factory type information ("FTI") for the new type in {file}`profiles/default/types/sponsor.xml`

```{code-block} xml
:emphasize-lines: 21
:linenos:

<?xml version="1.0"?>
<object name="sponsor" meta_type="Dexterity FTI" i18n:domain="plone"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n">
 <property name="title" i18n:translate="">Sponsor</property>
 <property name="description" i18n:translate=""></property>
 <property name="icon_expr">string:${portal_url}/document_icon.png</property>
 <property name="factory">sponsor</property>
 <property name="add_view_expr">string:${folder_url}/++add++sponsor</property>
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
 <property name="schema">ploneconf.site.content.sponsor.ISponsor</property>
 <property name="klass">ploneconf.site.content.sponsor.Sponsor</property>
 <property name="behaviors">
  <element value="plone.dublincore"/>
  <element value="plone.namefromtitle"/>
  <element value="plone.versioning"/>
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

Then we register the FTI in {file}`profiles/default/types.xml`

```{code-block} xml
:emphasize-lines: 4
:linenos:

<?xml version="1.0"?>
<object name="portal_types" meta_type="Plone Types Tool">
 <object name="talk" meta_type="Dexterity FTI"/>
 <object name="sponsor" meta_type="Dexterity FTI"/>
</object>
```

After reinstalling our package we can create the new type.

In production you will want to manage and document such changes in code with upgrade steps.
See the next chapter.


## Summary

- You created a new content type to store information on sponsors
- You learned how to protect individual fields from being edited with permissions
- Next you will learn how to display the sponsors at the bottom of every page
