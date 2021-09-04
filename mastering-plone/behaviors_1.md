(behaviors1-label)=

# Behaviors

````{sidebar} Classic chapter
```{figure} _static/plone.svg
:alt: Plone Logo
```

This chapter is about Plone Classic.

---

**Get the code! ({doc}`More info <code>`)**

Code for the beginning of this chapter:

```
git checkout talks
```

Code for the end of this chapter:

```
git checkout behaviors_1
```
````

In this part you will:

- Add another field to talks by using a behavior
- Add a custom index for the field
- Add a metadata column for the field

Topics covered:

- Behaviors
- Indexes
- Metacolumns

```{only} not presentation
You can extend the functionality of your Dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

But if you want to use this adapter, you must somehow know that an object implements that.
Also, adding more fields to an object would not be easy with such an approach.
```

(behaviors1-dexterity-label)=

## Dexterity Approach

```{only} not presentation
Dexterity has a solution for it, with special adapters that are called and registered by the name behavior.

A behavior can be added to any content type through the web and at runtime.

All default views (e.g. the add- and edit-forms) know about the concept of behaviors.
When rendering forms, the views also check whether there are behaviors referenced with the current context and if these behaviors have a schema of their own, these fields get shown in addition.
```

(behaviors1-names-label)=

## Names and Theory

```{only} not presentation
The name behavior is not a standard term in software development.
But it is a good idea to think of a behavior as an aspect.
You are adding an aspect to your content type and you want to write your aspect in such a way that it works independently of the content type on which the aspect is applied.
You should not have dependencies to specific fields of your object or to other behaviors.

Such an object allows you to apply the [open/closed principle](https://en.wikipedia.org/wiki/Open/closed_principle) to your dexterity objects.
```

(behaviors1-example-label)=

## Practical example

```{note}
You can also use the Plone Command Line Tool `plonecli` to initially create a behavior and edit it afterwards
```

```{only} not presentation
So, let us write our own small behavior.

We want some talks, news items or other content to be represented on the frontpage similar to what we did with the "hot news" field early on.

So for now, our behavior just adds a new field to store this information.
```

We want to keep a clean structure, so we create a {file}`behaviors` directory first, and include it into the zcml declarations of our {file}`configure.zcml`.

```xml
<include package=".behaviors" />
```

Then, we add an empty {file}`behaviors/__init__.py` and a {file}`behaviors/configure.zcml` containing

(featured-behavior-zcml-label)=

```{code-block} xml
:emphasize-lines: 6-10
:linenos: true

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="ploneconf.site">

  <plone:behavior
      title="Featured"
      name="ploneconf.featured"
      description="Control if a item is shown on the frontpage"
      provides=".featured.IFeatured"
      />

</configure>
```

And a {file}`behaviors/featured.py` containing:

(featured-behavior-python-label)=

```{code-block} python
:linenos: true

# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IFeatured(model.Schema):

    featured = schema.Bool(
        title=u'Show this item on the frontpage',
        required=False,
    )
```

````{only} not presentation
```{sidebar} Advanced reference
It can be a bit confusing when to use factories or marker interfaces and when not to.

If you do not define a factory, your attributes will be stored directly on the object.
This can result in clashes with other behaviors.

You can avoid this by using the {py:class}`plone.behavior.AnnotationStorage` factory.
This stores your attributes in an [Annotation](https://docs.plone.org/develop/plone/misc/annotations.html).
But then you *must* use a marker interface if you want to have custom viewlets, browser views or portlets.

Without it, you would have no interface against which you could register your views.
```
````

This is exactly the same type of schema as the one in the talk content-type.
The only addition is `@provider(IFormFieldProvider)` that makes sure that the fields in the schema are displayed in the add- and edit-forms.

Let's go through this step by step.

1. We register a behavior in {ref}`behaviors/configure.zcml <featured-behavior-zcml-label>`.
   We do not say for which content type this behavior is valid.
   You do this through the web or in the GenericSetup profile.
2. We create a interface in {ref}`behaviors/featured.py <featured-behavior-python-label>` for our behavior.
   We make it also a schema containing the fields we want to declare.
   We could just define schema fields on a zope.interface class, but we use an extended form from {py:mod}`plone.supermodel`, else we could not use the fieldset features.
3. We mark our schema as a class that also provides the {py:class}`IFormFieldProvider` interface using a decorator.
   The schema class itself provides the interface, not its instance!
4. We also add a `fieldset` so that our fields are not mixed with the normal fields of the object.
5. We add a normal [Bool](https://zopeschema.readthedocs.io/en/latest/fields.html#bool) schema field to control if a item should be displayed on the frontpage.

(behaviors1-adding-label)=

## Adding it to our talk

```{only} not presentation
We could add this behavior now via the plone control panel.
But instead, we will do it directly and properly in our GenericSetup profile
```

We must add the behavior to {file}`profiles/default/types/talk.xml`:

```{code-block} xml
:emphasize-lines: 8
:linenos: true

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

## Add a index for the new field

To use these new information for example in searches or listings we have to add an index to the `plone_catalog` for it. Indexing is the action to make object data search-able. Plone stores available indexes in the database.

```{note}
You can create them through-the-web and inspect existing indexes in portal_catalog on Index tab. To have those indexes directly after the installation you have to add those indexes like we will show in this chapter.
```

First of all we have to decide which kind of Index we need to add for our new field. Often used index types are for example:

- FieldIndex stores values as is
- BooleanIndex stores boolean values as is
- KeywordIndex allows keyword-style look-ups (query term is matched against all the values of a stored list)
- DateIndex and DateRangeIndex store dates (Zope 2 DateTime objects) in searchable format. The latter provides ranged searches.

Therefore we have a boolean field for the featured information it would be obvious to use the BooleanIndex for this.

To add a new index we have to change the `catalog.xml` in the `profiles/default` folder of our product. Without changes the file should look like this:

```{code-block} xml
:linenos: true

<?xml version="1.0"?>
<object name="portal_catalog">
  <!--<column value="my_meta_column"/>-->
</object>
```

To add the new BooleanIndex to the file we have to change the file as following:

```{code-block} xml
:emphasize-lines: 3-5
:linenos: true

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
</object>
```

To understand this snippet we have to understand the tags and information we are using:

- The `index`-tag will tell the `plone_catalog` that we want to add a new index
- `name` will be shown in the overview of `portal_catalog` and can be used in listings and searches later on
- `meta_type` will determine the kind of index we want to use
- The `indexed_attr` will include the fieldname of the information we are going to save in the index

After a restart and reinstallation of the product, it should now create a new index in the `portal_catalog`.

```{note}
Instead of deinstall/install or reinstall the product over the `prtal_quickinstaller` or `Add-Ons` controlpanel, we can import new or altered XML files in the `ZMI`. To do so go to `portal_setup`, switch to the `Import`-Tab and search for the profile to import like in this case: `ploneconf.site`.
```

To see if the adding was successfully we will open the ZMI of our plone-site and navigate to the `portal_catalog` and click the `Indexes`-Tab. In the above list the new index `fetaured` should pop up.

## Add a metadata column for the new field

The same rules and methods shown above for indexes apply for metadata columns. The difference with metadata is that it is not used for searching, but for displaying the results.

To add a metadata column for featured we have to add one more line in the `catalog.xml` like this:

```{code-block} xml
:emphasize-lines: 6
:linenos: true

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
  <column value="featured"/>
</object>
```

After another restart and another import of the xml-profile the new metadata column can be found in the `portal_catalog` in your `ZMI` under the tab `Metadata`.

(behaviors-1-label)=

## Exercises

Since you now know how to add indexes to the `portal_catalog` it is time for some exercise.

### Exercise 1

Add a new index for the `speaker`-field of our content type `Talk`

````{admonition} Solution
:class: toggle

```{code-block} xml
:emphasize-lines: 6-8
:linenos: true

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

[fieldset]: https://docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/fieldsets.html?highlight=fieldset
[iformfieldprovider]: https://docs.plone.org/external/plone.app.dexterity/docs/advanced/custom-add-and-edit-forms.html?highlight=iformfieldprovider#edit-forms
[plone.supermodel]: https://docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-interfaces-vs-other-interfaces
