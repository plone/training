---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# How Does collective.solr Work

We used to depend on `collective.indexing` as a means to hook into the normal catalog machinery of Plone to detect content changes.
Now the support for alternative indexes is part of `Products.CMFCore` (since version 2.2.12).
However, to return results from solr via a catalog query a monkey patch is still required.

## Base Functionality

- Patches the ZCatalog
- Some queries are faster in Solr, some are not
- Indexes and Metadata are duplicated
- Full text search with SearchableText is handled by solr

## Transactions

Solr is not transaction-aware and does not support any kind of rollback or undo.
We therefore only send data to Solr at the end of any successful request.
This is done via `Products.CMFCore.indexing`, a transaction manager and an end request transaction hook.

This means you won’t see any changes done to content inside a request when doing Solr searches later on in the same request.

## Querying Solr With collective.solr

ZCatalog Query:

```
catalog(SearchableText='Foo', portal_type='Document')
```

Result is a Solr response object.

Direct Solr Queries:

```
from collective.solr.dispatcher import solrSearchResults

solr_search = solrSearchResults(
    SearchableText=SearchableText,
    spellcheck='true',
    use_solr='true',
)
```

You can pass Solr query params directly to Solr and force a Solr response
with

```
use_solr='true'
```

## Mangler

`collective.solr` has a mangleQuery function that translates / mangles ZCatalog query parameters to replace Zope specifics with equivalent constructs for Solr.

```{seealso}
<https://github.com/collective/collective.solr/blob/main/src/collective/solr/mangler.py#L96>
```
