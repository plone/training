---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Advanced Pipeline Tips

One of the most difficult things about Transmogrifier is being aware of everything that is possible in the pipeline.
There is a lot of manipulation that can be done in the pipleline,
but it means you have to know what blueprints are available, and how to use them all.
When starting out, you may find yourself writing a lot more blueprints than is really necessary.
As you learn more about what is possible with the pipeline,
you may end up writing less custom code.

In this section, we'll cover some advanced tips of what is possible in the pipeline.

## Multiple pipelines

If you know you will run an import multiple times,
there are steps that will only need to be run the first time.
Any imports run after that can use less steps.
Additional pipelines can still point to your same custom blueprints file.

The pipelines will need to be set up as separate profiles.

## Dates Updater

plone.app.transmogrifier.datesupdater

```console
[datesupdate]
blueprint = plone.app.transmogrifier.datesupdater
modification-key = modified
effective-key = show_date
expiration-key = hide_date
```

## Conditions

Add a condition section that does the same thing as the blueprint we created that excludes older items.

See <https://5.docs.plone.org/external/collective.transmogrifier/docs/source/sections.html>

## Changing Types

Reducing the number of types used in your site?
You can map old types to what you want it to be in the new site.

```console
[map-types]
blueprint = collective.transmogrifier.sections.inserter
key = string:_type
value = python:{
    'HTML Document': 'Document',
    'Event Manager': 'Folder',
    'Folder (Ordered)': 'Folder',
    }.get(item['_type'], item['_type'])
```

## Others

Take data from a field called `document_src`, and put it into `text`,
which will be used as the body text for the object:

```console
[doctext]
blueprint = collective.transmogrifier.sections.manipulator
keys =
    document_src
destination = string:text
```

If the item is of type `history_item`, change the path where it will be imported:

```console
[history-item-path]
blueprint = collective.transmogrifier.sections.inserter
key = string:_path
condition = python:item['_type'] == 'history_item'
value = python:item['_path'].replace('/Images', '')
```
