---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-customsearch-label)=

# Custom Search

If the chapters about views seem complex, the custom search add-ons shown below might be a great alternative
until you feel comfortable writing views and templates.

Here are two add-ons that allow you to add custom searches and content listings through the web ("TTW", requiring no programming: only the web browser) in Plone.

(plone5-customsearch-eea-label)=

## eea.facetednavigation

eea.facetednavigation is a full-featured and a very powerful add-on to improve search within large collections of items.
No programming skills are required to configure it since the configuration is done TTW.

It lets you gradually select and explore different facets (metadata/properties) of the site content and narrow down you search quickly
and dynamically.

- Install [eea.facetednavigation](https://pypi.org/project/eea.facetednavigation/)

- Enable it on a new folder "Discover talks" by clicking on {guilabel}`Actions > Enable faceted navigation`.

- Click on the {guilabel}`Faceted > Configure` to configure it TTW.

  > - Select 'Talk' for *Portal type*, hide *Results per page*
  > - Add a checkboxes widget to the left and use the catalog index *Audience* for it.
  > - Add a select widget for speaker
  > - Add a radio widget for type_of_talk

Examples:

- https://www.dipf.de/en/research/current-projects
- https://www.mountaineers.org/courses/courses-clinics-seminars
- https://www.dyna-jet.com/highpressurecleaner

```{seealso}
We use the new catalog indexes to provide the data for the widgets and search the results.
For other use cases we could also use either the built-in vocabularies (<https://pypi.org/project/plone.app.vocabularies>) or create custom vocabularies for this.

- Custom vocabularies TTW using [Products.ATVocabularyManager](https://pypi.org/project/Products.ATVocabularyManager)
- Programming using Vocabularies: <https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html>
```

## collective.collectionfilter

A more lightweight solution for custom searches and faceted navigation is [collective.collectionfilter](https://pypi.org/project/collective.collectionfilter).
By default it allows you to search among the results of a collection and/or filter the results by keywords, author or type.

It can also be extended quite easily to allow additional filters (like `audience`).
