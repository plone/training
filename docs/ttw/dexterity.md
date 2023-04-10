---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(dexterity1-label-ttw)=

# Dexterity

In this part you will:

- Create a new content type called _Talk_.

Topics covered:

- Content types
- Archetypes and Dexterity
- Fields
- Widgets

(dexterity1-what-label-ttw)=

## What Is A Content Type?

A content type is a kind of object that can store information and is editable by users.
We have different content types to reflect the different kinds of information about which we need to collect and display information.
Pages, folders, events, news items, files (binary) and images are all content types.

It is common in developing a web site that you'll need customized versions of common content types, or perhaps even entirely new types.

Remember the requirements for our project? We wanted to be able to solicit and edit conference talks.
We _could_ use the **Page** content type for that purpose.

But we need to make sure we collect certain bits of information about a talk and we couldn't be sure to get that information if we asked potential
presenters to create a page.

Also, we'll want to be able to display talks featuring that special information, and we'll want to be able to show collections of talks.

A custom content type will be ideal.

(dexterity1-contains-label-ttw)=

## The Makings Of A Plone Content Type

Every Plone content type has the following parts:

Schema

: A definition of fields that comprise a content type;
properties of an object.

FTI

: The "Factory Type Information" configures the content type in Plone,
assigns it a name, an icon, additional features and possible views to it.

Views

: A view is a representation of the object and the content of its fields that may be rendered in response to a request.
You may have _one or more_ views for an object.
Some may be _visual_ — intended for display as web pages — others may be intended to satisfy AJAX requests and render content in formats like JSON or XML.

(dexterity1-comparison-label-ttw)=

## Dexterity And Archetypes

There are two content frameworks in Plone:

- _Dexterity_: new and the coming default.
- _Archetypes_: old, tried and tested. Widespread, used in many add-ons.
- Plone 4.x: Archetypes is the default, with Dexterity available.
- Plone 5.x: Dexterity is the default, with Archetypes available.
- For both, add and edit forms are created automatically from a schema.

What are the differences?

- Dexterity: New, faster, modular, no dark magic for getters and setters.
- Archetypes had magic setter/getter - use {py:meth}`talk.getAudience()` for the field {py:attr}`audience`.
- Dexterity: fields are attributes: {py:attr}`talk.audience` instead of {py:meth}`talk.getAudience()`.

"Through The Web" or TTW, i.e. in the browser, without programming:

- Dexterity has a good TTW story.
- Archetypes has no TTW story.
- UML-modeling: [ArchGenXML](https://4.docs.plone.org/old-reference-manuals/archgenxml/index.html) for Archetypes, [agx](https://github.com/bluedynamics/agx.dev) for Dexterity

Approaches for Developers:

- Schema in Dexterity: TTW, XML, Python. Interface = schema, often no class needed.
- Schema in Archetypes: Schema only in Python.
- Dexterity: Easy permissions per field, easy custom forms.
- Archetypes: Permissions per field are hard, custom forms even harder.
- If you have to program for old sites you need to know Archetypes!
- If starting fresh, go with Dexterity.

Extending:

- Dexterity has _Behaviors_: easily extendable.
  Just activate a behavior TTW and your content type is e.g. translatable ({py:mod}`plone.app.multilingual`).
- Archetypes has {py:mod}`archetypes.schemaextender`. Powerful but not as flexible.

We have only used Dexterity for the last few years.
We teach Dexterity and not Archetypes because it's more accessible to beginners, has a great TTW story and is the future.

Views:

- Both Dexterity and Archetypes have a default view for content types.
- Browser Views provide custom views.
- You can generate views for content types in the browser without programming (using the {py:mod}`plone.app.mosaic` Add-on).
- Display Forms.

(dexterity1-modify-label-ttw)=

## Modifying Existing Types

- Go to the control panel <http://localhost:8080/Plone/@@dexterity-types>

- Inspect some of the existing default types.

- Select the type {guilabel}`News Item` and add a new field `Hot News` of type {guilabel}`Yes/No`

- In another tab, add a _News Item_ and you'll see the new field.

- Go back to the schema-editor and click on {guilabel}`Edit XML Field Model`.

- Note that the only field in the XML schema of the News Item is the one we just added. All others are provided by behaviors.

- Edit the form-widget-type so it says:

  ```xml
  <form:widget type="z3c.form.browser.checkbox.SingleCheckBoxFieldWidget"/>
  ```

- Edit the News Item again. The widget changed from a radio field to a check box.

- The new field `Hot News` is not displayed when rendering the News Item. We'll take care of this later.

```{seealso}
<https://5.docs.plone.org/external/plone.app.contenttypes/docs/README.html#extending-the-types>
```

(dexterity1-create-ttw-label-ttw)=

## Creating Content Types "Through-The-Web"

In this step we will create a content type called _Talk_ and try it out.
When it's ready, we will move the code from the web to the file system and into our own add-on.
Later we will extend that type, add behaviors and a viewlet for Talks.

- Add new content type "Talk" and some fields for it:

  - {guilabel}`Add new field` "Type of talk", type {guilabel}`Choice`.
    Go to {menuselection}`Settings` and add options: talk, keynote, training.
  - {guilabel}`Add new field` "Details", type {guilabel}`Rich Text` with a maximal length of 2000.
  - {guilabel}`Add new field` "Audience", type {guilabel}`Multiple Choice`. Add options: beginner, advanced, pro.
  - Check the behaviors that are enabled: _Dublin Core metadata_, _Name from title_. Do we need them all?

- Test the content type.

- Return to the control panel <http://localhost:8080/Plone/@@dexterity-types>

- Extend the new type: add the following fields:

  - "Speaker", type: {guilabel}`Text line`
  - "Email", type: {guilabel}`Email`
  - "Image", type: {guilabel}`Image`, not required
  - "Speaker Biography", type: {guilabel}`Rich Text`

- Test again.

Here is the complete XML schema created by our actions:

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

(dexterity1-ttw-to-code-label-ttw)=

## Moving Content Types Into Code

It's awesome that we can do so much through the web.
But it's also a dead end if we want to reuse this content type in other sites.

Also, for professional development,
we want to be able to use version control for our work,
and we'll want to be able to add the kind of business logic that will require programming.

So, we'll ultimately want to move our new content type into a Python package.
We're missing some skills to do that, and we'll cover those in the next couple of chapters.

```{seealso}
- [Dexterity Developer Manual](https://5.docs.plone.org/external/plone.app.dexterity/docs/index.html)
- [The standard behaviors](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html)
```

(dexterity1-excercises-label-ttw)=

## Exercises

### Exercise 1

Modify Pages to allow uploading an image as decoration (like _News Items_ do).

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

- Go to the dexterity control panel (<http://localhost:8080/Plone/@@dexterity-types>)
- Click on *Page* (<http://127.0.0.1:8080/Plone/dexterity-types/Document>)
- Select the tab *Behaviors* (<http://127.0.0.1:8080/Plone/dexterity-types/Document/@@behaviors>)
- Check the box next to {guilabel}`Lead Image` and save.

The images are displayed above the title.
```

### Exercise 2

Create a new content type called _Speaker_ and export the schema to a XML File.
It should contain the following fields:

- Title, type: {guilabel}`Text Line`
- Email, type: {guilabel}`Email`
- Homepage, type: {guilabel}`URL` (optional)
- Biography, type: {guilabel}`Rich Text` (optional)
- Company, type: {guilabel}`Text Line` (optional)
- Twitter Handle, type: {guilabel}`Text Line` (optional)
- IRC Handle, type: {guilabel}`Text Line` (optional)
- Image, type: {guilabel}`Image` (optional)

Do not use the {term}`Dublin Core` or the Basic behavior since a speaker should not have a description (unselect it in the Behaviors tab).

We could use this content type later to convert speakers into Plone users. We could then link them to their talks.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

The schema should look like this:

```xml
<model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns:users="http://namespaces.plone.org/supermodel/users"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="title" type="zope.schema.TextLine">
      <title>Name</title>
    </field>
    <field name="email" type="plone.schema.email.Email">
      <title>Email</title>
    </field>
    <field name="homepage" type="zope.schema.URI">
      <required>False</required>
      <title>Homepage</title>
    </field>
    <field name="biography" type="plone.app.textfield.RichText">
      <required>False</required>
      <title>Biography</title>
    </field>
    <field name="company" type="zope.schema.TextLine">
      <required>False</required>
      <title>Company</title>
    </field>
    <field name="twitter_handle" type="zope.schema.TextLine">
      <required>False</required>
      <title>Twitter Handle</title>
    </field>
    <field name="irc_name" type="zope.schema.TextLine">
      <required>False</required>
      <title>IRC Handle</title>
    </field>
    <field name="image" type="plone.namedfile.field.NamedBlobImage">
      <required>False</required>
      <title>Image</title>
    </field>
  </schema>
</model>
```
````

```{seealso}
- [Dexterity XML](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html)
- [Model-driven types](https://5.docs.plone.org/external/plone.app.dexterity/docs/model-driven-types.html#model-driven-types)
```
