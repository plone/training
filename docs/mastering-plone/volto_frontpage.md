---
myst:
  html_meta:
    "description": "How to use the listing block with custom criterion"
    "property=og:description": "How to use the listing block with custom criterion"
    "property=og:title": "Creating a dynamic frontpage with Volto blocks"
    "keywords": "catalog, index, listing, criteria"
---

(volto-frontpage-label)=

# Creating a dynamic frontpage with Volto blocks

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend
:class: logo
```

Solve a simlar tasks in Plone Classic in chapter {doc}`frontpage`

---

Get the code! ({doc}`More info <code>`)

```{note}
The code you modify is from the backend, i.e. ploneconf.site!
```

Code for the beginning of this chapter:

```shell
git checkout behaviors_1
```

Code for the end of this chapter:

```shell
git checkout frontpage
```
````

In this part you will:

- Use a listing block to show content marked as featured
- Configure additional criterion for listing block

## Add Index as collection criteria

To understand why we need a collection criteria for a dynamic frontpage in Volto and what a collection criterion is, we have to look at the listing block of Volto.

```{figure} _static/volto_frontpage.png
:alt: Listing Block sidebar
:align: left
```

In the sidebar we see the `criteria` selection and if we click there, it'll show some of the choosable criterias ordered in categories like the following:

- `Metadata` contains indexes that are counting as metadata like Type (means Portal Types) and Review State
- `Text` contains indexes that are counting as text-data like Description and Searchable Text
- `Dates` contains indexes which are working with date-data like Effective Date and Creation Date

To get all talks we marked as `featured` we have to get the listing block to recognize our newly created index.
This means we have to add our index to the collection criterias, so we can choose it.

To add our new index as a criterion to be appliable in a listing block or a collection, we have to switch to our `backend`. There we have to create a plone.app.registry record for our index. This can be achieved by adding a new file {file}`profiles/default/registry/querystring.xml`:

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<registry xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          i18n:domain="plone">

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.featured">
      <value key="title" i18n:translate="">Featured</value>
      <value key="enabled">True</value>
      <value key="sortable">False</value>
      <value key="operations">
          <element>plone.app.querystring.operation.boolean.isTrue</element>
          <element>plone.app.querystring.operation.boolean.isFalse</element>
      </value>
     <value key="group" i18n:translate="">Metadata</value>
  </records>

</registry>
```

To understand this code snippet, we have to know the information and tags we are using:

- The prefix refers to the featured index we just created.
- The operations elements define the provided criterion values to filter the listing.
- The group value defines the group under which the entry shows up in the selection widget, in our case `Metadata`.

```{note}
For a full list of all existing QueryField declarations see <https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L245>
```

```{note}
For a full list of all existing operations see <https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L1>
```

Like explained in the last chapter we can now restart the instance and import the newly added profile by using the `portal_setup` in our ZMI.


## Add a listing block to show the featured content

Now we will go back to our frontend and open localhost:3000.
To create a new listing block on the front-page we have to click on `edit` and then create one new block.
Now you choose the block `Listing` from the menu:

```{figure} _static/volto_frontpage_1.png
:alt: Most used blocks in Volto
:align: left
```

You will gain a new block and sidebar looking like this:

```{figure} _static/volto_frontpage_3.png
:alt: listing block with featured content
:align: left
```

## Outlook: block variations

The listing block comes with default variations for the display. The editor can choose from these vaiations to change the template for the listing: with thumbnail image or without, etc.. Your project maybe needs a custom template. The way to go would be to create an additional variation of the listing block. See {ref}`plone6docs:extensions-block-variations` for more information.
