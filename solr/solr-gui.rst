*************************
Solr GUI and Query Syntax
*************************

In the next part we will take a closer look the the search GUI of Solr and its query syntax.

Access Solr GUI
===============

Solr is a REST-based wrapper around the Java lucene index.
It comes with its own web GUI.
It is possible to access all of the SOLR API via REST and most of this functionality is exposed via its web GUI.
To test it out, do the following:

 - Go to: http://localhost:8983/solr/#/
 - Select Core "collection1"
 - Go to: "Schema Browser"
 - Select "fullname"
 - Click: "Load Term Info"
 - Click on term "<fullname>"

Solr Query Syntax
=================

Solr Query Parameters:

Query "q"::

    Title:"news"
    *:"news"

Solr response ::

  {
    "responseHeader":{
      "status":0,
      "QTime":0,
      "params":{
        "q":"*:*",
        "indent":"true",
        "wt":"json"}},
    "response":{"numFound":51,"start":0,"docs":[
        {
          "path_string":"/Plone/news",
          "Title":"News",
          "showinsearch":true,
          "path_depth":3,
          "exclude_from_nav":false,
          "Type":"Folder",
          "UID":"88411960ec3f4b1f86feae9094ba718e",
          "is_folderish":true,
          "getId":"news",
          "Date":"2015-12-25T16:46:24Z",
          "review_state":"published",
          "Language":"en",
          "portal_type":"Folder",
          "expires":"2499-12-30T22:00:00Z",
          "allowedRolesAndUsers":["Anonymous"],
          "path_parents":["/Plone",
            "/Plone/news"],
          "object_provides":["Products.ATContentTypes.interfaces.folder.IATFolder",
            "Products.CMFPlone.interfaces.syndication.ISyndicatable",
            "eea.facetednavigation.subtypes.interfaces.IPossibleFacetedNavigable",
            "Products.CMFCore.interfaces._content.IContentish",
            "webdav.interfaces.IWriteLock"],
          "Description":"Site News",
          "effective":"1000-01-05T22:00:00Z",
          "created":"2015-12-25T16:46:24.841Z",
          "getIcon":"",
          "Creator":"admin",
          "modified":"2015-12-25T16:46:24.841Z",
          "SearchableText":"news  News  Site News ",
          "_version_":1545835799688249344},


Filter Query "fq":

This parameter can be used to specify a query that can be used to restrict the super set of documents that can be returned,
without influencing the score.
It can be very useful for speeding up complex queries since the queries specified with fq are cached independently from the main query.
Caching means the same filter is used again for a later query (i.e. there's a cache hit).
See SolrCaching to learn about the caches Solr uses::

    is_folderish:true

Sorting "sort"::

    "Date asc"
    "Date desc"

Filter List "fl"::

    Title,Type

This parameter can be used to specify a set of fields to return,
limiting the amount of information in the response.

Response Writer "wt"::

  "json"

A Response Writer generates the formatted response of a search.

Solr Query via URL
==================

Copy query from Solr GUI, e.g.::

    http://localhost:8983/solr/collection1/select?q=Title%3A%22termine%22&wt=json&indent=true

You can use curl or the Python package `requests` (https://pypi.python.org/pypi/requests) to access the REST API of Solr.

Solr Query via API
==================

Another way of accessing Solr is to use a Python wrapper,
which exposes the Solr API in a Pythonic way.
Collective.solr has included such a wrapper (``solr.py``),
which is old but still works for our case.
Meanwhile there are other packages around.
Here are some examples:

 - ``mysolr``: https://pypi.python.org/pypi/mysolr/0.8.3
 - ``solrpy``: https://pypi.python.org/pypi/solrpy3/0.98
 - ``pysolr``: https://pypi.python.org/pypi/pysolr/3.5.0

Sometimes it is handy to have a separate virtualenv available for doing batch operations (delete, update, etc.)

I use the following script to delete all Plone Documents from Solr ::

 >>> from mysolr import Solr
 >>> solr = Solr(base_url='http://localhost:8983/solr')
 >>> solr.delete_by_query('portal_type:Document')
 

Advanced Solr Query Syntax
==========================

Simple Query::

    "fieldname:value"

A clause can be **mandatory** (finds only articles containing the word *Boston*)::

  +Boston

A clause can be **probibited** (finds all articles except those containing the word *Vienna*)::

  -Vienna

Operators::

    "Title:Foo AND Description:Bar"

"AND", "OR", "+", "-", "||", "NOT"

Be carefull with combining operators such as::

 New AND York OR Buenos AND Aires

which will probably lead to no results.
You will need to use sub-queries.

Sub-queries::

 (New AND York) OR (Buenos Aires)

Range Queries::

    "[* TO NOW]"

Boost Terms::

    "people^4"

Fuzzy Search::

 "house0.6"

Proximity Search::

 "apache solr"~

with treshold::

 "apache solr"~7

Wildcard queries:

Find all cities starting with *New* you can do::

 New*

Or a single character wildcard::

 M?ller

which will find *Müller*, *Miller*, etc.

Date math
=========

Solr provides some useful date units which are available for date queries.
The units you can choose of are:

*YEAR*, *MONTH*, *DAY*, *DATE* (synonymous with *DAY*), *HOUR*, *MINUTE*, *SECOND*, *MILLISECOND*, *MILLI* (synonymous with *MILLISECOND*) and *NOW*.
All of these units can be pluralized with an *S* as in *DAYS*. ::

 effective:[* TO NOW-3MONTHS]

*NOW* has a millisecond precision.
To round down by using the */* operator (it never rounds up)::

 effective:[* TO NOW/DAY-2YEAR]

Existing (and non-existing) queries
===================================

Assume we want to find all documents which have a value in a certain field
(whatever that value is, it doesn't matter).

Find all documents with a description::

 Description:[* TO *] 

The oposite (finding all documents with no description) is also possible::

 -Description:[* TO *] 

Faceting
========

Faceting is one of the killer features of Solr.
It allows the grouping nd filtering results for better findability.
To enable faceting you need o turn faceting on in the query and specify the fields you want tofacet upon:

For a simple facet query in Solr you activate the feature and specify the facet fields(s)::

 http://localhost:8983/solr/collection1/select?q=*%3A*&wt=json&indent=true&facet=true&facet.field=portal_type

Besides the matching documents this will give you an additional grouping of documents::

  {
   "responseHeader":{
    "status":0,
    "QTime":6,
    "params":{
      "q":"*:*",
      "facet.field":"portal_type",
      "indent":"true",
      "wt":"json",
      "facet":"true"}},
   "response":{"numFound":6,"start":0,"docs":[
     ...
   ]}
   "facet_counts":{
    "facet_queries":{},
    "facet_fields":{
      "portal_type":[
        "Folder",3,
        "Collection",2,
        "Document",1]},
    "facet_dates":{},
    "facet_ranges":{},
    "facet_intervals":{}}
  }

There are more complex scenarios possible. For a complete list
of options see the according Solr documentation.

.. seealso:: https://cwiki.apache.org/confluence/display/solr/Faceting

With collective.solr you don't have to worry about the faceting details too much.
There is a convenient method to configure the faceting fields in the control panel of collective.solr.
All the other magic is handled by the product.
We will see an example later.

Search GUIs
===========

 - collective.solr out of the box: collective.solr commes with its own search view. 
   For the new version 6.0 it is based on ReactJS and looks similar to the Plone search view with native facet support of Solr.

 - eea.facetednavigation: This addon allows faceting out of the box even without Solr.
   It is a product for integrators to setup search and filter GUIs TTW.
   It can be used for several use cases: Search pages, collection replacements, etc.  **DEMO**

 - custom: Another way is to create a custom search page. 
   This is easy to do and we will see later on in this training how.

Exercise
========

 Do some queries in Solr directly
