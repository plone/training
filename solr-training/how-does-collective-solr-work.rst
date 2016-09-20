Collective Solr
------------------------------------------------------------------------------

Currently we depend on collective.indexing as a means to hook into the normal catalog machinery of Plone to detect content changes. c.indexing before version two had some persistent data structures that frequently caused problems when removing the add-on. These problems have been fixed in version two. Unfortunately c.indexing still has to hook the catalog machinery in various evil ways, as the machinery lacks the required hooks for its use-case. Going forward it is expected for c.indexing to be merged into the underlying ZCatalog implementation, at which point collective.solr can use those hooks directly.

TBD

Collective Solr Control Panel
*****************************

Basic Configuration:

- Active
- Host
- Port
- Base
- ...

Query Configuration::

    +(Title:{value}^5 OR
      Description:{value}^2 OR
      SearchableText:{value} OR
      SearchableText:({base_value}
    )
    OR searchwords:({base_value})^1000) +showinsearch:True


Base Functionality
******************

- Patches the ZCatalog
- Some queries are faster in Solr some are not
- Indexes and Metadata duplicated
- Full text search with SearchableText


Transactions
************

Solr is not transactional aware or supports any kind of rollback or undo. We therefor only sent data to Solr at the end of any successful request. This is done via collective.indexing, a transaction manager and an end request transaction hook. This means you won’t see any changes done to content inside a request when doing Solr searches later on in the same request.


Querying Solr with collective.solr
**********************************

ZCatalog Query::

    catalog(SearchableText='Foo', portal_type='Document')

Result is a Solr Object.

Direct Solr Queries::

    solr_search = solrSearchResults(
        SearchableText=SearchableText,
        spellcheck='true',
        use_solr='true',
    )

You can pass Solr query params directly to Solr and force a Solr response with "use_solr='true'".

Though, you have to make sure the response also contains


Mangler
*******

collective.solr has a mangleQuery function that translates / mangles ZCatalog query parameters to replace zope specifics with equivalent constructs for Solr.

https://github.com/collective/collective.solr/blob/master/src/collective/solr/mangler.py#L96
