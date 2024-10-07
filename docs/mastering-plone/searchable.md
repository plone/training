---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(searchable-label)=

# Search for additional fields

```{card}
In this part you will:

- Ensure that the detailed description of a talk and its speaker are included in search.
```

````{card} Backend chapter

Checkout `ploneconf.site` at tag "upgrade_steps":

```shell
git checkout upgrade_steps
```

The code at the end of the chapter:

```shell
git checkout searchable
```

More info in {doc}`code`
````

In the previous chapter we prepared a search block to search for talks.
You may have noticed that a search for speaker names does not show the expected results.
We add the two fields of a talk "speaker" and "details" to the `SearchableText` index.
This is the index that's addressed when making a full text search.


The package `plone.app.dexterity.textindexer` allows to add fields to the `SearchableText`index.
The package is already installed with Plone.

Add the behavior `plone.textindexer` to the list of behaviors of your content type.

{file}`src/ploneconf/site/profiles/default/types/talk.xml`

```{code-block} xml
:emphasize-lines: 7

  <property name="behaviors">
    <element value="plone.dublincore" />
    <element value="plone.namefromtitle" />
    <element value="plone.versioning" />
    <element value="ploneconf.featured" />
    <element value="plone.eventbasic" />
    <element value="plone.textindexer" />
  </property>
```

Now you need to mark the fields you want to include in your `SearchableText` index.
This can be done with the `searchable` directive.

{file}`src/ploneconf/site/profiles/default/types/talk.xml`

```{code-block} python
:emphasize-lines: 1, 3, 11

from plone.app.dexterity import textindexer

    textindexer.searchable("details")
    details = RichText(
        title="Details",
        description="Description of the talk (max. 2000 characters)",
        max_length=2000,
        required=True,
    )

    textindexer.searchable("speaker")
    speaker = schema.TextLine(
        title="Speaker",
        description="Name (or names) of the speaker",
        required=False,
    )
```

The `SearchableText` index now includes your fields.

To be able to search for text in the detailed description of a talk and its speaker we need to restart Plone and update the catalog.
This can be done with an upgrade step.
Do you remember the earlier chapter {doc}`upgrade_steps`?
You can use the function `update_indexes` for a new upgrade step.


```{figure} _static/searchable.png
:alt: Make fields searchable

Make fields searchable
```
