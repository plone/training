---
myst:
  html_meta:
    "description": "Content type basics"
    "property=og:description": "Content type basics"
    "property=og:title": "Content types I"
    "keywords": "data model, content type"
---

(dexterity1-label)=

# Content types I

In this part you will:

- Learn about content types
- Customize existing types
- Create a content type through the web


(dexterity1-what-label)=

## What is a content type?

A content type instance is a kind of object that can store information and is editable by users.
We have different content types to reflect the different kinds of information about which we need to collect and display information.

Pages, events, news items, files (binary) and images are all content types.

See "Features of Plone – {ref}`features-content-types-label`" for an overview.

It is common in developing a web site that you'll need customized versions of common content types, or perhaps even entirely new types.

Remember the requirements for our project? We wanted to be able to solicit and edit conference talks.
We _could_ use the **Page** content type for that purpose.
But we need to make sure we collect certain bits of information about a talk and we couldn't be sure to get that information if we just asked potential presenters to create a page.

Also, we'll want to be able to display talks featuring that special information, and we'll want to be able to show collections of talks.
A custom content type will be ideal.

(dexterity1-contains-label)=

## The makings of a Plone content type

Every Plone content type has the following parts:

Schema

: A definition of fields that comprise a content type, properties of an object.

FTI

: The "Factory Type Information" configures the content type in Plone, assigns it a name, additional features and available views to it.

Views

: A view is a representation of the object and the content of its fields that may be rendered in response to a request.
You may have _one or more_ views for an object.
Some may be _visual_ — intended for display as web pages — others may be intended to satisfy AJAX requests and render content in formats like JSON or XML.

## Schemas, Fields and Values

In a schema you can model fields that are used to store data.
Plone automatically creates forms bases on the schemata of a content type to add and edit content.

Values of these fields are attributes on content objects.

Here is a example that shows how to access and modify these values in python:

```pycon
>>> obj.title
'A Newsitem'
>>> obj.description
'Some description'
>>> obj.description = 'A new description'
>>> obj.description
'A new description'
>>> obj.image
<plone.namedfile.file.NamedBlobImage object at 0x11634c320>
>>> obj.image.data
b'\x89PNG\r\n\x1a\n\x00\x00\x00\...'
```

## Behaviors

Content types can have additional schemata. These are called behaviors.
They are meant to be used across content types to add shared functionality.

One example is the ability of most content types to allow them to be excluded from the navigation.
The field is available on all types even though it is not defined in their schema.
Instead it is provided by the behavior `plone.excludefromnavigation` that most content types use.

Each behavior schema can define fields. The values of these fields are again attributes on content objects.

The behavior `plone.excludefromnavigation` adds a attribute `exclude_from_nav` to each object. The value is either `True` or `False` because it is a boolean field.

(dexterity1-modify-label)=

## Modifying existing types

For now, we will not code anything.
We will only use the Plone web interface features.

- Go to the {guilabel}`Content Types` control panel at http://localhost:3000/controlpanel/dexterity-types.

- Inspect some of the existing default types.

- Select {guilabel}`Schema` of the context menu of content type `News Item`.

  ```{figure} _static/volto_dexterity_types.png

  ```

- Add a new field `Show this item on the frontpage` of type {guilabel}`Yes/No`

  ```{figure} _static/volto_edit_schema.png

  ```
  Save your changes.

- In another tab, add a `News Item` and you'll see the new field.

  ```{figure} _static/volto_add_news_item.png

  ```

- Note that the only field in the schema of the News Item is the one we just added.
  All others are provided by behaviors.

- So far the data in the new field `Show this item on the frontpage` is not displayed when rendering the News Item.
  We'll take care of this later.


(dexterity1-create-ttw-label)=

## Creating content types TTW

In this step we will create a content type called `Talk` and try it out. When it's ready we will move the code from the web to the file system and into our own add-on. Later we will extend that content type.

- Add new content type "Talk" and some fields for it:

  - {guilabel}`Add new field` "Type of talk", type "Choice". Add options: talk, keynote, training.
  - {guilabel}`Add new field` "Details", type "Rich Text" with a maximal length of 2000.
  - {guilabel}`Add new field` "Audience", type "Multiple Choice". Add options: beginner, advanced, pro.
  - Check the behaviors that are enabled: _Dublin Core metadata_, _Name from title_. Do we need them all?

- Test the content type.

- Return to the control panel <http://localhost:8080/Plone/@@dexterity-types>

- Extend the new type: add the following fields:

  - "Speaker", type: "Text line"
  - "Email", type: "Email"
  - "Image", type: "Image", not required
  - "Speaker Biography", type: "Rich Text"

- Test again.

````{note}
The schema you created through the web is stored as XML in the database. Here is the complete XML schema created by our actions:

```{code-block} xml
:linenos:

<model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
     xmlns:users="http://namespaces.plone.org/supermodel/users"
     xmlns:security="http://namespaces.plone.org/supermodel/security"
     xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
     xmlns:form="http://namespaces.plone.org/supermodel/form"
     xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="type_of_talk" type="zope.schema.Choice">
      <description/>
      <title>Type of talk</title>
      <values>
        <element>Talk</element>
        <element>Training</element>
        <element>Keynote</element>
      </values>
    </field>
    <field name="details" type="plone.app.textfield.RichText">
      <description>Add a short description of the talk (max. 2000 characters)</description>
      <max_length>2000</max_length>
      <title>Details</title>
    </field>
    <field name="audience" type="zope.schema.Set">
      <description/>
      <title>Audience</title>
      <value_type type="zope.schema.Choice">
        <values>
          <element>Beginner</element>
          <element>Advanced</element>
          <element>Professional</element>
        </values>
      </value_type>
    </field>
    <field name="speaker" type="zope.schema.TextLine">
      <description>Name (or names) of the speaker</description>
      <title>Speaker</title>
    </field>
    <field name="email" type="plone.schema.email.Email">
      <description>Adress of the speaker</description>
      <title>Email</title>
    </field>
    <field name="image" type="plone.namedfile.field.NamedBlobImage">
      <description/>
      <required>False</required>
      <title>Image</title>
    </field>
    <field name="speaker_biography" type="plone.app.textfield.RichText">
      <description/>
      <max_length>1000</max_length>
      <required>False</required>
      <title>Speaker Biography</title>
    </field>
  </schema>
</model>
```
````

It's awesome that we can do so much through the web and great for prototyping or small projects. But it's also a dead end if we want to reuse this content type in other sites.

Also, for professional development, we want to be able to use version control for our work, and we'll want to be able to add the kind of business logic that will require programming.

Instead, you'll create your new content type in your Python package.
Using Python to define the schema gives us much more control (e.g. for validation and default-values).

(dexterity1-excercises-label)=

## Exercises

### Exercise 1

Modify Pages to allow uploading an image as decoration (like News Items do).

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

- Go to the dexterity control panel (<http://localhost:8080/Plone/@@dexterity-types>)
- Click on *Page* (<http://127.0.0.1:8080/Plone/dexterity-types/Document>)
- Select the tab *Behaviors* (<http://127.0.0.1:8080/Plone/dexterity-types/Document/@@behaviors>)
- Check the box next to {guilabel}`Lead Image` and save.

The images are displayed above the title.
```

## Further reading
- Documentation {doc}`plone6docs:backend/fields`
- [Example content type](https://github.com/collective/example.contenttype) A Plone content type with all available fields

Plone 5 documentation
- [Dexterity Developer Manual](https://5.docs.plone.org/external/plone.app.dexterity/docs/index.html)
- [The standard behaviors](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html)
- [Dexterity XML](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html)
- [Model-driven types](https://5.docs.plone.org/external/plone.app.dexterity/docs/model-driven-types.html#model-driven-types)
