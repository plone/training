---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(extending-label)=

# Extending Plone

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Extending Volto frontend:

- {ref}`volto-richtexteditor-label`
- {ref}`volto-addon-label`
- {ref}`volto-custom-addon-label`
````

In this part you will:

- Get an overview over the technologies used to extend Plone

Topics covered:

- Overriding python or react components
- Component Architecture
- ZCML
- GenericSetup

Topic of the following chapter:

- Extending Plone with existing add-ons

As a developer you want to go further than simply configuring Plone, you want to extend and customize it.
Plone is built to be extended.
Extendability is not an afterthought but is the core of Plone and the systems it is based on.
Instead it is the core of its architecture.

```{note}
Plone itself even started out as an extension for CMF, which is an extension for Zope. Now Plone is the basis for many applications that extend it.
```

Plone consists of a Python backend and a React frontend. They are connected via the REST API. Thus you have two different layers that you can customize.

Therefore we create two different extension-packages to customize and extend Plone:

1. One is a python package that holds e.g. content types, dexterity-behaviors and configuration.
2. The other is a javascript package that hold views, styling and customization of the frontend.

Sometimes it is easy to know, which layer needs to be customized to achieve a certain result.

- All styling and javascript-based interaction is customized on the Volto-layer of Plone
- Content types and other persistent data should be customized or created in a python-package

For more complex use-cases you will need to add code to both parts of our customization-story. For example a content type will be defined in the python-package and its visualization will be defined in the javascript-package.

(extending-technologies-label)=

## Extension technologies

How do you extend Plone?

This depends on what type of extension you want to create.

```{only} not presentation
- You can create extensions with new types of objects to add to your Plone site. Usually these are content types.
- You can create an extension that changes or extends functionality. For example to change the way Plone displays search results, or to make pictures searchable by adding a converter from jpg to text.
```

For most projects you mix all kinds of methods to extend Plone.

### Component Architecture

```{only} presentation
- State of the art
- verbose
- cryptic
- Powerful and flexible
```

```{only} not presentation
The best way to extend Plone is via *Components*.

A bit of history is in order.

When Zope started, object-oriented design was **the** silver bullet.

Object-oriented design is good at modeling inheritance, but breaks down when an object has multiple aspects that are part of multiple taxonomies.

Some object-oriented programming languages like Python handle this through multiple inheritance. But it's not a good way to do it. Zope objects have more than 10 base classes. Too many namespaces makes code that's hard to maintain. Where did that method/attribute come from?

After a while, XML and Components became the next silver bullet (Does anybody remember J2EE?).

Based on their experiences with Zope in the past, Zope developers thought that a component system configured via XML might be the way to go to keep the code more maintainable.

Before Zope Components functionality was often extended by a practice called Monkey Patching: Changing code in other modules by importing and then modifying it at runtime.

Monkey Patching, like subclassing via multiple inheritance, does not scale. Multiple plugins might overwrite each other, you would explain to people that they have to reorder the imports, and then, suddenly, you will be forced to import feature A before B, B before C and C before A, or else your application won't work.

As the new concepts were radically different from the old Zope concepts, the Zope developers renamed the new project to Zope 3.
But it did not gain traction, was eventually renamed to Bluebream and then died out.

But the component architecture itself is quite successful and the Zope developers extracted it into the Zope Toolkit. The Zope toolkit is part of Zope, and Plone developers use it extensively.

This is what you want to use.
```

(extending-components-label)=

### Configuring Zope Components with ZCML

```{only} presentation
- zcml (Zope Component Markup Language) is used to register components
- components are distingushed by interfaces (contracts) that they require or provide
```

```{only} not presentation
ZCML, the Zope Configuration Mark-up Language is an XML based language used to configure Zope Components. With ZCML you declare utilities, adapters and browser views.

Components are distinguished from one another by the interfaces (formal definitions of functionality) that they require or provide.

During startup, Zope reads all these ZCML statements, validates that there are not two declarations trying to register the same components and registers everything. All components are registered by interfaces required and provided. Components with the same interfaces may optionally also be named.

It may seem a little cumbersome that you have to register all components. But thanks to ZCML, you hardly ever have a hard time to find what and where extensions or customizations are defined. ZCML files are like a phone book.
```

```{eval-rst}
.. epigraph::

    Explicit is better than implicit

    -- The Zen of Python

```

### GenericSetup

```{only} presentation
- Old style
- Does not cover 100% of use cases
```

```{only} not presentation
The next thing is {py:mod}`Products.GenericSetup`.

*GenericSetup* lets you define persistent configuration in XML files. *GenericSetup* parses the XML files and updates the persistent configuration according to the configuration. This is a step you have to run on your own!

You will see many objects in Zope or the ZMI that you can customize through the web. If they are well behaving, they can export their configuration via *GenericSetup* and import it again.

Typically you use *GenericSetup* to change workflows or add new content type definitions.

GenericSetup profiles may also be built into Python packages. Every package that is listed on the add-on package list inside a Plone installation has a GS profile that details how it fits into Plone. Packages that are part of Plone itself may have GS profiles, but are excluded from the active/inactive listing.
```

Example:

{file}`metadata.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>
    <dependency>profile-pas.plugins.ldap:default</dependency>
    <dependency>profile-collective.geolocationbehavior:default</dependency>
    <dependency>profile-collective.behavior.banner:default</dependency>
  </dependencies>
</metadata>
```

Most settings are stored in a tool called `portal_registry`. Since it has great import/export handlers for GenericSetup it can be configures with {file}`registry.xml`:

{file}`registry.xml`:

```xml
<?xml version="1.0"?>
<registry>
  <record name="plone.site_title" >
    <value>Mastering Plone Development</value>
  </record>
</registry>
```
