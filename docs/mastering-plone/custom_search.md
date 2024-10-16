---
myst:
  html_meta:
    "description": "Provide a customized search"
    "property=og:description": "Provide a customized search"
    "property=og:title": "Custom search"
    "keywords": "filter, faceted search"
---

(custom-search-label)=

# Custom Search

Volto has a search block that allows you to build custom searches without additional add-ons.

## Exercise

Show talks on the talks page with a search block.
The visitor should see a filter for the type of talk (Keynote, Talk, Lightning Talk).

You can add facets in the sidebar, but "type of talk" is not available.
What is necessary to implement?

Remember what we did to show featured content on the front page.

```{dropdown} Tips for a Solution
:animate: fade-in-slide-down
:icon: question

- The field `type_of_talk` needs to be indexed in catalog.
- `type_of_talk` needs to be a collection criterion.

After adding an index and a criterion, restarting the backend, and re-installing the add-on, the index is present in catalog but empty.

For populating the index you can go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes and reindex the new index.

In case you want to change something of the index, the index can be deleted.
A re-start of the backend, a re-install of the add-on and a new re-index of the index will populate the index.

Check the entries by switching to the "Browse" tab.
```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

{file}`catalog.xml`
```xml

  <index name="type_of_talk" meta_type="KeywordIndex">
    <indexed_attr value="type_of_talk"/>
  </index>
  <column value="type_of_talk"/>
```

{file}`querystring.xml`
```xml

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.type_of_talk">
      <value key="title" i18n:translate="">Type of Talk</value>
      <value key="enabled">True</value>
      <value key="sortable">False</value>
      <value key="operations">
        <element>plone.app.querystring.operation.selection.any</element>
        <element>plone.app.querystring.operation.selection.all</element>
        <element>plone.app.querystring.operation.selection.none</element>
      </value>
     <value key="group" i18n:translate="">Metadata</value>
     <value key="vocabulary">ploneconf.types_of_talk</value>
  </records>
```

Checkout `ploneconf.site` at tag "search" to see the updated code.
````
