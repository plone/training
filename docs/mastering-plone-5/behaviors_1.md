---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-behaviors1-label)=

# Behaviors

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout testing
```

Code for the end of this chapter:

```shell
git checkout behaviors_1
```

{doc}`code`
````

In this part you will:

- Add another field to talks by using a behavior

Topics covered:

- Behaviors

```{only} not presentation
You can extend the functionality of your Dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

But if you want to use this adapter, you must somehow know that an object implements that.
Also, adding more fields to an object would not be easy with such an approach.
```

(plone5-behaviors1-dexterity-label)=

## Dexterity Approach

```{only} not presentation
Dexterity has a solution for it, with special adapters that are called and registered by the name behavior.

A behavior can be added to any content type through the web and at runtime.

All default views (e.g. the add- and edit-forms) know about the concept of behaviors.
When rendering forms, the views also check whether there are behaviors referenced with the current context and if these behaviors have a schema of their own, these fields get shown in addition.
```

(plone5-behaviors1-names-label)=

## Names and Theory

```{only} not presentation
The name behavior is not a standard term in software development.
But it is a good idea to think of a behavior as an aspect.
You are adding an aspect to your content type and you want to write your aspect in such a way that it works independently of the content type on which the aspect is applied.
You should not have dependencies to specific fields of your object or to other behaviors.

Such an object allows you to apply the [open/closed principle](https://en.wikipedia.org/wiki/Open/closed_principle) to your dexterity objects.
```

(plone5-behaviors1-example-label)=

## Practical example

```{only} not presentation
So, let us write our own small behavior.

In the future, we want some talks, news items or other content be represented on the frontpage similar to what we did with the "hot news" field early on.

So for now, our behavior just adds a new field to store this information.
```

We want to keep a clean structure, so we create a {file}`behaviors` directory first, and include it into the zcml declarations of our {file}`configure.zcml`.

```xml
<include package=".behaviors" />
```

Then, we add an empty {file}`behaviors/__init__.py` and a {file}`behaviors/configure.zcml` containing

(plone5-social-behavior-zcml-label)=

```{code-block} xml
:emphasize-lines: 6-10
:linenos:

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

(plone5-social-behavior-python-label)=

```{code-block} python
:linenos:

# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IFeatured(model.Schema):

    directives.fieldset(
        'featured',
        label=u'Featured',
        fields=('featured',),
    )

    featured = schema.Bool(
        title=u'Show this item on the frontpage',
        required=False,
    )
```

```{only} not presentation
Let's go through this step by step.

1. We register a behavior in {file}`behaviors/configure.zcml`.
   We do not say for which content type this behavior is valid.
   You do this through the web or in the GenericSetup profile.
2. We create a marker interface in {file}`behaviors/social.py` for our behavior.
   We make it also a schema containing the fields we want to declare.
   We could just define schema fields on a zope.interface class, but we use an extended form from {py:mod}`plone.supermodel`, else we could not use the fieldset features.
3. We mark our schema as a class that also provides the {py:mod}`IFormFieldProvider` interface using a decorator.
   The schema class itself provides the interface, not its instance!
4. We also add a `fieldset` so that our fields are not mixed with the normal fields of the object.
5. We add a normal [Bool](https://zopeschema.readthedocs.io/en/latest/api.html#zope.schema.interfaces.IBool) schema field to control if a item should be displayed on the frontpage.
```

````{only} not presentation
```{note}

It can be a bit confusing when to use factories or marker interfaces and when not to.

If you do not define a factory, your attributes will be stored directly on the object.
This can result in clashes with other behaviors.

You can avoid this by using the {py:class}`plone.behavior.AnnotationStorage` factory.
This stores your attributes in an [Annotation](https://5.docs.plone.org/develop/plone/misc/annotations.html).
But then you *must* use a marker interface if you want to have custom viewlets, browser views or portlets.

Without it, you would have no interface against which you could register your views.
```
````

(plone5-behaviors1-adding-label)=

## Adding it to our talk

```{only} not presentation
We could add this behavior now via the plone control panel.
But instead, we will do it directly and properly in our GenericSetup profile
```

We must add the behavior to {file}`profiles/default/types/talk.xml`:

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

[plone5_fieldset]: https://5.docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/fieldsets.html?highlight=fieldset
[plone5_iformfieldprovider]: https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/custom-add-and-edit-forms.html?highlight=iformfieldprovider#edit-forms
[plone5_plone.supermodel]: https://5.docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-interfaces-vs-other-interfaces
