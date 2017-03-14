*****************************
How does collective.solr work 
*****************************

Currently we depend on collective.indexing as a means to hook into the normal catalog machinery of Plone to detect content changes.
collective.indexing before version two had some persistent data structures that frequently caused problems when removing the add-on.
These problems have been fixed in version two.
Unfortunately collective.indexing still has to hook the catalog machinery in various evil ways,
as the machinery lacks the required hooks for its use-case.
Going forward it is expected for collective.indexing to be merged into the underlying ZCatalog implementation,
at which point collective.solr can use those hooks directly.

Base Functionality
==================

- Patches the ZCatalog
- Some queries are faster in Solr some are not
- Indexes and Metadata duplicated
- Full text search with SearchableText

Transactions
============

Solr is not transaction-aware and does not support any kind of rollback or undo.
We therefore only send data to Solr at the end of any successful request.
This is done via collective.indexing,
a transaction manager and an end request transaction hook.
This means you won’t see any changes done to content inside a request when doing Solr searches later on in the same request.

Querying Solr with collective.solr
==================================

ZCatalog Query::

    catalog(SearchableText='Foo', portal_type='Document')

Result is a Solr Object.

Direct Solr Queries::

    solr_search = solrSearchResults(
        SearchableText=SearchableText,
        spellcheck='true',
        use_solr='true',
    )

You can pass Solr query params directly to Solr and force a Solr response
with ::

  use_solr='true'


Mangler
=======

collective.solr has a mangleQuery function that translates / mangles ZCatalog query parameters to replace zope specifics with equivalent constructs for Solr.

.. seealso:: https://github.com/collective/collective.solr/blob/master/src/collective/solr/mangler.py#L96


