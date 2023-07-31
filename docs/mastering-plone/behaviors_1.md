---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(behaviors1-label)=

# Behaviors

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout talks
```

Code for the end of this chapter:

```shell
git checkout behaviors_1
```
````

Enhance content types to be selectable for presentation on the front page.

In this part you will:

- Add a field to talks and other content types by using a behavior
- Make the field values available via catalog search

Topics covered:

- Behaviors
- Catalog indexes and catalog metadata columns

```{only} not presentation
A first approach would be to extend the functionality of a content type by writing an adapter that adapts an object of this type to add an additional attribute or feature.
This would mean to write an adapter for an interface the respective content types provides.

But for which interface shall we write the adapter?
Do we want to write it for the general {py:class}`Products.CMFCore.interfaces.IContentish` which is implemented by all content types?
We want to be more specific and provide the behavior only for some selected content types.
```

(behaviors1-dexterity-label)=

## Dexterity Approach

Dexterity has special adapters that are called and registered by the name behavior.

A behavior can be enabled for any content type through the web UI and at runtime.

All default views (e.g. the add and edit forms) know about the concept of behaviors.
When rendering forms, the views check whether there are behaviors referenced with the current context and if these behaviors have a schema of their own, these fields get shown in addition.


(behaviors1-names-label)=

## Names and Theory

```{only} not presentation
The name behavior is not a standard term in software development.
But it is a good idea to think of a behavior as an aspect.
You are adding an aspect to your content type and you want to write your aspect in such a way that it works independently of the content type on which the aspect is applied.
You should not have dependencies to specific fields of your type or to other behaviors.

Such an object allows you to apply the [open/closed principle](https://en.wikipedia.org/wiki/Open/closed_principle) to your dexterity objects.
```

(behaviors1-example-label)=

## Practical example

```{note}
We write the behavior code step by step, but you can also use the Plone Command Line Tool `plonecli` to initially create a behavior and edit it afterwards.
```

```{only} not presentation
So, let us write our own small behavior.

We want some selected talks, news items or other content to be presented on the front page.

So for now, our behavior just adds a new field to store the information if an object should be listed on the front page.
```

We want to keep a clean structure, so we create a {file}`behaviors` directory first, and include it into the zcml declarations of our {file}`configure.zcml`.

```xml
<include package=".behaviors" />
```

Then, we add an empty {file}`behaviors/__init__.py` and a {file}`behaviors/configure.zcml` containing

(featured-behavior-zcml-label)=

```{code-block} xml
:emphasize-lines: 6-11
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="ploneconf.site">

  <plone:behavior
      title="Featured"
      name="ploneconf.featured"
      description="Control if an item is shown on the frontpage"
      provides=".featured.IFeatured"
      />

</configure>
```

And a {file}`behaviors/featured.py` containing:

(featured-behavior-python-label)=

```{code-block} python
:linenos:

from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IFeatured(model.Schema):

    featured = schema.Bool(
        title='Show this item on the frontpage',
        required=False,
    )
    fieldset("Options", fields=["featured"])
```

This is exactly the same type of schema as the one in the talk content-type.
The only addition is `@provider(IFormFieldProvider)` that makes sure that the fields in the schema are displayed in the add- and edit-forms.

Let's go through this step by step.

1. We register a behavior in {ref}`behaviors/configure.zcml <featured-behavior-zcml-label>`.
   We do not say for which content type this behavior shall be enabled.
   You do this through the web or in the GenericSetup profile.
2. We create an interface in {ref}`behaviors/featured.py <featured-behavior-python-label>` for our behavior.
   We make it also a schema containing the fields we want to declare.
   We could just define schema fields on a zope.interface class, but we use an extended form from {py:mod}`plone.supermodel`, else we could not use the fieldset features.
3. We mark our schema as a class that also provides the {py:class}`IFormFieldProvider` interface using a decorator.
   The schema class itself provides the interface, not its instance!
4. We also add a `fieldset` so that our field is not mixed with the normal fields of the object.
5. We add a normal [Bool](https://zopeschema.readthedocs.io/en/latest/api.html#zope.schema.interfaces.IBool) schema field to control if an item should be displayed on the frontpage.

```{note}
For simplicity we do not use the so called `AnnotationStorage`.
The value of the field "featured" is saved on the object.
Imagine an add-on that unfortunately uses the same field name "featured" for another purpose than `ploneconf.site`.
Here the AnnotationStorage comes in.
The object is equipped by a storage where behaviors do store values with a key unique per behavior.

Furthermore a `marker interface` is needed as soon as we want to register components for objects that do adapt this behavior, e.g. REST API endpoints.

We will see `marker interfaces` and `AnnotationStorages` in chapter {doc}`behaviors_2`.
```

(behaviors1-adding-label)=

## Enabling the behavior on our talk

```{only} not presentation
We could add this behavior now via the plone control panel "content types".
But instead, we will do it directly and properly in a content types `GenericSetup` profile.
```

We add the behavior to {file}`profiles/default/types/talk.xml`:

```{code-block} xml
:emphasize-lines: 8
:linenos:

<?xml version="1.0"?>
<object name="talk" meta_type="Dexterity FTI" i18n:domain="plone"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n">
   ...
 <property name="behaviors">
  <element value="plone.dublincore"/>
  <element value="plone.namefromtitle"/>
  <element value="ploneconf.featured"/>
 </property>
 ...
</object>
```

After a restart and the reinstallation of the product we now have the new field we added through the behavior:

```{figure} _static/behaviors_frontend.png
:alt: Extended behavior field shown in Volto
```


(behaviors1-index-label)=

## Add an index for the new field

To use this new "featured" information in searches and listings, we have to add an index to the `plone_catalog`.
Indexing is the action to make object data searchable.
Plone stores available catalog indexes in the database.

```{note}
You can inspect existing indexes in `portal_catalog` on "Index" tab <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes>.
```

First of all we have to decide which kind of index we need for our new field.
Common index types are:

- FieldIndex stores values as is
- BooleanIndex stores boolean values as is
- KeywordIndex allows keyword-style look-ups (query term is matched against all the values of a stored list)
- DateIndex and DateRangeIndex store dates in searchable format.
  The latter provides ranged searches.

Because we have a boolean field for the featured information, it is obvious to use the BooleanIndex for this.

To add a new index we have to change the `catalog.xml` in the `profiles/default` folder of our product. Without changes the file does look like this:

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<object name="portal_catalog">
  <!--<column value="my_meta_column"/>-->
</object>
```

To add the new BooleanIndex to the file we have to change the file as following:

```{code-block} xml
:emphasize-lines: 3-5
:linenos:

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
</object>
```

To understand this snippet we have to understand the tags and information we are using:

- The `index` tag will tell the `plone_catalog` that we want to add a new index.
- `name` will be shown in the overview of `portal_catalog` and can be used in listings and searches later on.
- `meta_type` determines the type of index we want to use.
- The `indexed_attr` includes the field name of the information we are going to save in the index.

After a restart and reinstallation of the product, a new index is created in the `portal_catalog`.

```{note}
Instead of de-installing and installing in the `Add-Ons` control panel, we can import new or altered XML files in the `ZMI`. To do so go to `portal_setup`, switch to the `Import`-Tab and search for the profile to import like in this case: `ploneconf.site`.
```

To see if the adding was successful, we open the ZMI of our Plone site and navigate to the `portal_catalog` and click the `Indexes` tab.
The new index `featured` should now be listed.
As soon as you edit content, you can also see the values of "featured" listed on "Browse" tab.


(behaviors1-metadata-label)=

## Add a metadata column for the new field

The same rules and methods shown above for indexes apply for metadata columns.
The difference with metadata is that it is not used as criterions for searching the catalog, but is mandatory for displaying of search results returned from the catalog.

We will see that in fact every attribute of an object can be accessed in search results by explicitly requesting objects.
A way more performant search is requesting what is stored in the catalog.
And this is exactly the metadata.

To add a metadata column for "featured", we have to add one more line in the `catalog.xml` like this:

```{code-block} xml
:emphasize-lines: 6
:linenos:

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
  <column value="featured"/>
</object>
```

After another restart and another import of the xml-profile, the new metadata column can be found in the `portal_catalog` in your `ZMI` on the tab `Metadata`.


(behaviors1-exercise-label)=

## Exercise

Since you now know how to add indexes to the `portal_catalog`, it is time for an exercise.

Add a new index for the `speaker` field of our content type `Talk`

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} xml
:emphasize-lines: 6-8
:linenos:

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
  <index name="speaker" meta_type="FieldIndex">
    <indexed_attr value="speaker"/>
  </index>
</object>
```
````
