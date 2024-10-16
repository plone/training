---
myst:
  html_meta:
    "description": "Organize and protect fields of content types"
    "property=og:description": "Organize and protect fields of content types"
    "property=og:title": "Content types III: Sponsors"
    "keywords": "schema, permission"
---

(dexterity-3-label)=

# Content types III: Sponsors

Without sponsors, a conference would be hard to finance! Plus it is a good opportunity for Plone companies to advertise their services.

```{card}
In this part we will:

- Create a sponsor contenttype to manage sponsors
- Store non-visible information about the sponsor in the sponsor-type

Tools and techniques covered:

- Schema hint and directives
- Field permissions
```

````{card} Backend chapter

Checkout `ploneconf.site` at tag "search":

```shell
git checkout search
```

The code at the end of the chapter:

```shell
git checkout schema
```

More info in {doc}`code`
````


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
    """Dexterity Schema for Sponsors"""

    level = schema.Choice(
        title="Sponsoring Level", values=["bronze", "silver", "gold"], required=True
    )

    text = RichText(title="Text", required=False)

    url = schema.URI(title="Link", required=False)

    fieldset("Images", fields=["logo", "advertisement"])
    logo = namedfile.NamedBlobImage(
        title="Logo",
        required=False,
    )

    advertisement = namedfile.NamedBlobImage(
        title="Advertisement (Gold-sponsors and above)",
        required=False,
    )

    directives.read_permission(notes="plone.app.controlpanel.Site")
    directives.write_permission(notes="plone.app.controlpanel.Site")
    notes = RichText(
        title="Secret Notes (only for site-administrators and managers)", required=False
    )


@implementer(ISponsor)
class Sponsor(Container):
    """Sponsor instance class"""
```

Some things are notable here:

- {samp}`fieldset('Images', fields=['logo', 'advertisement'])` moves the two image fields to another tab.
- {samp}`directives.read_permission(...)` sets the read and write permission for the field `notes` to users who can make changes on the control panel 'Site'. Usually this permission is only granted to Site Administrators and Managers. We use it to store information that should not be publicly visible.

```{seealso}
See the {doc}`dexterity_reference` for a reference of all field-types and directives you can use in dexterity.
```

## The Factory Type Information, or FTI

Next, we create the factory type information ("FTI") for the new type in {file}`profiles/default/types/sponsor.xml`

```{code-block} xml
:emphasize-lines: 21
:linenos:

<?xml version="1.0" encoding="utf-8"?>
<object xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        meta_type="Dexterity FTI"
        name="sponsor"
        i18n:domain="plone"
>
  <property name="title"
            i18n:translate=""
  >Sponsor</property>
  <property name="description"
            i18n:translate=""
  />
  <property name="icon_expr">string:${portal_url}/document_icon.png</property>
  <property name="factory">sponsor</property>
  <property name="add_view_expr">string:${folder_url}/++add++sponsor</property>
  <property name="link_target" />
  <property name="immediate_view">view</property>
  <property name="global_allow">True</property>
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types" />
  <property name="allow_discussion">False</property>
  <property name="default_view">view</property>
  <property name="view_methods">
    <element value="view" />
  </property>
  <property name="default_view_fallback">False</property>
  <property name="add_permission">cmf.AddPortalContent</property>
  <property name="schema">ploneconf.site.content.sponsor.ISponsor</property>
  <property name="klass">ploneconf.site.content.sponsor.Sponsor</property>
  <property name="behaviors">
    <element value="plone.dublincore" />
    <element value="plone.namefromtitle" />
    <element value="plone.versioning" />
  </property>
  <property name="model_source" />
  <property name="model_file" />
  <property name="schema_policy">dexterity</property>
  <alias from="(Default)"
         to="(dynamic view)"
  />
  <alias from="edit"
         to="@@edit"
  />
  <alias from="sharing"
         to="@@sharing"
  />
  <alias from="view"
         to="(selected layout)"
  />
  <action action_id="view"
          category="object"
          condition_expr=""
          description=""
          icon_expr=""
          link_target=""
          title="View"
          url_expr="string:${object_url}"
          visible="True"
  >
    <permission value="View" />
  </action>
  <action action_id="edit"
          category="object"
          condition_expr=""
          description=""
          icon_expr=""
          link_target=""
          title="Edit"
          url_expr="string:${object_url}/edit"
          visible="True"
  >
    <permission value="Modify portal content" />
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
