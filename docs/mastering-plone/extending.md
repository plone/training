---
myst:
  html_meta:
    "description": "Plone architecture and concepts"
    "property=og:description": "Plone architecture and concepts"
    "property=og:title": "Extend and customize Plone"
    "keywords": "Plone, architecture, zcml, Generic Setup"
---

(extending-label)=

# Extend and customize Plone

```{card} Backend chapter

In this part you will get an overview over the technologies used to extend the Plone backend.

Topics covered:

- Extension packages
- Component architecture
- ZCML
- Generic Setup
```

As a developer you want to go further than simply configuring Plone.
You want to extend and customize it.
Plone is built to be extended.
Extendability is not an afterthought but is the core of Plone and the systems it is based on.

How do you extend Plone?

This depends on what type of extension you want to create.

```{only} not presentation
- You can create extensions with new types of objects to add to your Plone site. Usually these are content types.
- You can create an extension that changes or extends functionality. For example to change the way Plone displays search results, or to make pictures searchable by adding a transformer from image to text.
```

For most projects you combine multiple kinds of methods to extend Plone.


(extending-packages-label)=

## Extension packages

Plone consists of a Python backend and a React frontend.
They are connected via the REST API.
Thus you have two different layers that you can customize.

Therefore we create two different extension packages to customize and extend Plone.
(These are similar to add-ons, but they are located in the project repository.)

1. One is a Python package that holds for example content types, behaviors and configuration.
   (For the training project, this is located in {file}`backend/src/ploneconf/site`.)
2. The other is a JavaScript package that hold views, styling and customization of the frontend.
   (For the training project, this is located in {file}`frontend/packages/volto-ploneconf-site`.)

Sometimes it is easy to know which layer needs to be customized to achieve a certain result.

- All styling and JavaScript-based interaction is customized on the frontend side of Plone.
- Content types and other persistent data are customized or created in a Python package.

For more complex use cases you will need to add code to both parts of our customization story.
For example a content type is defined in the Python package and its visualization is defined in the JavaScript package.



(extending-technologies-component-architecture-label)=

## Component Architecture

```{only} presentation
- State of the art
- verbose
- cryptic
- Powerful and flexible
```

````{only} not presentation

Plone uses a component architecture to provide loose coupling between different parts of the system.

What does that mean?
There is a central registry of components that can fulfill predefined contracts, called interfaces.
If some code wants to make a call to another part of Plone, it should not do so directly.
Instead, it should ask the registry for a component that can provide the interface it is designed to use.

There are several kinds of components:

* *Utilities* provide a standalone service.
* *Adapters* provide a new way to access an existing object.
* *Subscribers* execute actions in response to events triggered on a different object.

For example, there is an interface `INameFromTitle` which defines how to get the title for a content item.
(Get an adapter which is registered for the `INameFromTitle` interface, and get its `title` attribute.)
If you as a developer want to change how the title is calculated for a specific content type, you can register an `INameFromTitle` adapter for that content type.

This is the basis for Plone's extensibility.
Add-on packages can easily change core Plone functionality by adding or replacing components in the registry, without needing to directly change the code that uses those components.

```{tip}
Many of the interfaces used by Plone core are defined in the `plone.base` package.
You can explore them here: https://github.com/plone/plone.base/tree/main/src/plone/base/interfaces

However, Plone is made up of many packages, so there are also a lot of interfaces defined elsewhere.
```

```{note}
Earlier versions of Zope and Plone relied more on other ways of composing software, such as object-oriented inheritance.
But this led to very complicated objects that were difficult to reason about and override.

Over time, many parts have been updated to use the component architecture.
But there are still some inner parts which use inheritance.
Sometimes it is necessary to use more invasive techniques like monkey-patching to override core Plone functionality.
```

````


(extending-components-label)=

## Configure Zope Components with ZCML

```{only} presentation
- zcml (Zope Component Markup Language) is used to register components
- components are distingushed by interfaces (contracts) that they require or provide
```

````{only} not presentation
The Zope Configuration Markup Language (ZCML) is an XML-based language used to configure Zope components.
With ZCML you register utilities, adapters and browser views using ZCML.

Components are distinguished from one another by the interfaces (formal definitions of functionality) that they require or provide.

During startup, Zope reads all these ZCML statements, validates that there are not two declarations trying to register the same components, and registers everything.
All components are registered by interfaces required and provided.
Components with the same interfaces may optionally also be named.

```{tip}
ZCML is only processed at startup time.
If you make changes to a `.zcml` file, you have to restart the backend in order for the changes to take effect.
```

It may seem a little cumbersome that you have to register all components.
But thanks to ZCML, you hardly ever have a hard time to find what and where extensions or customizations are defined.
ZCML files are like a phone book.
````

```{epigraph}
   Explicit is better than implicit
   
   -- The Zen of Python
```

(extending-technologies-generic-setup-label)=

## Generic Setup

```{only} presentation
- Old style
- Does not cover 100% of use cases
```

```{only} not presentation
Another tool for configuring Plone using XML files is {term}`Generic Setup`.

Generic Setup organizes XML configuration files in a _profile_.
When the profile is applied, it will update persistent settings stored in the database.

Unlike ZCML, Generic Setup profiles are not read automatically.
You have to apply the profile on your own, usually by installing or upgrading an add-on.
When you do this, Generic Setup reads the XML files and updates the persistent configuration accordingly.

Generic Setup profiles are a useful way to programmatically configure the same things that can be changed through the web in a control panel.
You will see many objects in Zope or the ZMI that you can customize through the web.
If they are well behaving, they can export their configuration via Generic Setup and import it again.

For example, you can use Generic Setup to change workflows or add new content type definitions.

Generic Setup profiles may also be built into Python packages.
Every package that is listed in the Add-ons control panel in Site Setup has a Generic Setup profile that defines how it fits into Plone.
(Packages that are part of Plone itself may also have Generic Setup profiles, but are not shown in the Add-ons control panel unless they are optional.)
```

Examples of a profile of an add-on in `profile/default/`

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

Most settings are stored in a tool called `portal_registry`.
Since it has great import/export handlers for Generic Setup, it can be configured with {file}`registry/main.xml`:

{file}`registry/main.xml`:

```xml
<?xml version="1.0"?>
<registry>
  <record name="plone.site_title" >
    <value>Mastering Plone Development</value>
  </record>
</registry>
```
