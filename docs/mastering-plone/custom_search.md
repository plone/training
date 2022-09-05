---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(custom-search-label)=

# Custom Search

## Custom Search in Volto

Volto has (since Volto 14) a Search-Block that allows you to build custom searches without additional addons.


## Custom Search in Plone Classic

If the Plone Classic chapters about Views ({doc}`/mastering-plone/views_2`) and catalog-searches (({doc}`/mastering-plone/views_3`)) seem complex, the custom search add-ons shown below might be a great alternative until you feel comfortable writing views and templates.

Here are two add-ons that allow you to add custom searches and content listings through the web ("TTW", requiring no programming: only the web browser) in Plone.

(customsearch-eea-label)=

### eea.facetednavigation

eea.facetednavigation is a full-featured and a very powerful add-on to improve search within large collections of items.
No programming skills are required to configure it since the configuration is done TTW.

It lets you gradually select and explore different facets (metadata/properties) of the site content and narrow down you search quickly
and dynamically.

- Install [eea.facetednavigation](https://pypi.org/project/eea.facetednavigation/)

- Enable it on a new folder "Discover talks" by clicking on {guilabel}`Actions > Enable faceted navigation`.

- Click on the {guilabel}`Faceted > Configure` to configure it TTW.

  > - Select 'Talk' for _Portal type_, hide _Results per page_
  > - Add a checkboxes widget to the left and use the catalog index _Audience_ for it.
  > - Add a select widget for speaker
  > - Add a radio widget for type_of_talk

Examples:

- <https://www.dipf.de/en/research/current-projects>
- <https://www.mountaineers.org/courses/courses-clinics-seminars>
- <https://www.dyna-jet.com/highpressurecleaner>

```{seealso}
We use the new catalog indexes to provide the data for the widgets and search the results.
For other use cases we could also use either the built-in vocabularies (<https://pypi.org/project/plone.app.vocabularies>) or create custom vocabularies for this.

- Custom vocabularies TTW using [collective.taxonomy](https://pypi.org/project/collective.taxonomy)
- Programming using Vocabularies: <https://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html>
```

### collective.collectionfilter

A more lightweight solution for custom searches and faceted navigation is [collective.collectionfilter](https://pypi.org/project/collective.collectionfilter).
By default it allows you to search among the results of a collection and/or filter the results by keywords, author or type.

It can also be extended quite easily to allow additional filters (like `audience`).

