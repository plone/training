---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Alternative Indexing/Search Solutions

## alm.solrindex

`alm.solrindex` is another add-on for connecting Plone search to Solr.

It takes a different approach:

- `collective.solr` *wraps* the Zope catalog.
  Each item is indexed both in the ZCatalog and in Solr, typically including many indexes in both.
  When a search is performed, based on the indexes used,
  it decides to query either ZCatalog or solr but not both.
- `alm.solrindex` operates as an index *within* the Zope catalog,
  replacing the standard SearchableText index.
  Solr only needs to index the fulltext,
  and the ZCatalog no longer needs to do so.
  When a search is performed that includes a SearchableText criterion,
  first alm.solrindex will query solr for results,
  then those results will be further filtered by other ZCatalog indexes.

Pros:

- Solr is more efficient than ZCTextIndex at indexing and querying fulltext.
- Avoids duplication of index storage.
- Less data needs to be sent between Plone and solr when indexing.
- Don't need to add new indexes to Solr and reindex.

Cons:

- No admin UI in Plone control panel.
- Customizations can require monkey patching.
- Potential for missing some results. (see below)

### Setup

We set up Solr in our buildout in a similar way,
using the [hexagonit.recipe.download](https://pypi.org/project/hexagonit.recipe.download) and `collective.recipe.solr` buildout recipes.

The `solr-instance` buildout part looks a bit different.

```ini
[solr-instance]
recipe = collective.recipe.solrinstance
solr-location = ${solr-download:location}
host = ${settings:solr-host}
port = ${settings:solr-port}
basepath = /solr
max-num-results = 500
default-search-field = SearchableText
unique-key = docid
index =
    name:docid          type:integer  stored:true     required:true
    name:SearchableText type:text     stored:false
    name:Title          type:text     stored:false
    name:Description    type:text     stored:false
```

- We set the `unique-key` identifying the record to `docid`.
  `alm.solrindex` will pass the ZCatalog's internal integer record id
  (`rid`) in this field.
- We set the `default-search-field` to SearchableText,
  so that Solr queries which don't specify a field will use SearchableText.
- We configure fields for docid and each of the standard Plone fulltext indexes,
  but not any other fields.
- We set `stored: false` on the indexes so that Solr will only store the docid.

We also need to reference the Solr URI in an environment variable for the Plone instance part,
so that `alm.solrindex` knows where to connect

```ini
[instance]
environment-vars =
SOLR_URI http://${settings:solr-host}:${settings:solr-port}/solr
```

After running buildout,
we can start Plone and activate `alm.solrindex` in the Add-ons control panel.

```{note}
The default installation profile removes the existing SearchableText,
Title, and Description indexes, but does not automatically reindex existing content.

If you have existing content in the site,
you'll need to do a full reindex of the ZCatalog to get them indexed in Solr.
```

### Why Are Results Missing?

There is a limitation to this approach.

Solr is configured with a maximum limit on the number of results it will return
(`max-num-results` in the buildout configuration).
This is done because it hurts performance if there are thousands and thousands of results,
and Solr has to serialize all of them and Plone has to deserialize all of them.

For queries that only use indexes that are in Solr (i.e. the fulltext indexes),
this is not a big problem.

Solr ranks the results so the limited set it returns should be the most relevant results,
and most users are not going to navigate past more than a few pages of results anyway.

It can be a problem when the search term is very generic
(so there are many results and its hard for Solr to determine the most relevant ones)
and the results are also going to be filtered by other indexes
(such as in a faceted search solution).

In this case the limited result set from Solr is fairly arbitrary,
the other filters only get to operate on this limited set,
and we might end up missing results that should be there.

Example: Consider a site where there are 10,000 items with the term 'pdf',
including one in a folder "/annual-reports/2015".
If a search is performed for 'pdf' within the path '/annual-reports/2015':

1. First Solr finds all documents matching 'pdf', and ranks them.
2. Next it returns the top 500 results to Plone.
3. Next Plone filters those results by path. There is a good chance that
   our target document was not included in the 500 that Solr returned,
   so this filters down to no results.

There are a couple workarounds for this problem, both of which have their own tradeoff:

1. Increase `max-num-results` above the total number of documents
   (but this will hurt performance for queries that return many results).
2. Make sure that other indexes that are likely to narrow down the results a lot
   are also included in Solr
   (but this detracts from the main advantages of using `alm.solrindex` over `collective.solr`).

### Customization

Each type of field has its own *handler* which takes care of translating between ZCatalog and Solr queries.
These can be overridden to handle advanced customization:

Example: monkey patch the `TextFieldHandler` to use an `edismax` query that allows boosting some fields

```python
from Products.PluginIndexes.common.util import parseIndexRequest
from alm.solrindex.handlers import TextFieldHandler
from alm.solrindex.quotequery import quote_query

def parse_query(self, field, field_query):
    name = field.name
    request = {name: field_query}
    record = parseIndexRequest(request, name, ('query',))
    if not record.keys:
        return None

        query_str = ' '.join(record.keys)
        if not query_str:
            return None

        if name == 'SearchableText':
            q = quote_query(query_str)
        else:
            q = u'+%s:%s' % (name, quote_query(query_str))

        return {
            'q': q,
            'defType': 'edismax',
            'qf': 'Title^10 Description^2 SearchableText^0.2',  # boost fields
            'pf': 'Title~2^20 Description~5^5 SearchableText~10^2',  # boost phrases
        }
        TextFieldHandler.parse_query = parse_query
```

Example: Add a `path` index that works like Zope's `ExtendedPathIndex`
(i.e. it'll find anything whose path begins with the query value):

`solr.cfg`

```ini
[solr-instance]
...
index =
    ...
    name:path           type:descendent_path stored:false
```

`handlers.py`

```python
from alm.solrindex.handlers import DefaultFieldHandler

class PathFieldHandler(DefaultFieldHandler):

    def parse_query(self, field, field_query):
        query = super(PathFieldHandler, self).parse_query(field, field_query)
        if query == {'fq': 'path:""'}:
            return {}
        return query

    def convert_one(self, value):
        # avoid including the site path in the index data
        if value.startswith('/Plone'):
            value = value[6:]
        return super(PathFieldHandler, self).convert_one(value)
```

ZCML:

```
<utility component=".handlers.PathFieldHandler"
         provides="alm.solrindex.interfaces.ISolrFieldHandler"
         name="path" />
```

## DIY Solr

If both *collective.solr* and *alm.solrindex* are too much for you or you have special needs,
you can access Solr by custom code.
This might be, if you:

> - need to access a Solr server with a newer version / multicore setup and you don't have access to the configuration of Solr
> - Only want a fulltext search page of a small site with no need for full realtime support

You can find a full-featured example of a full-fledged custom Solr integration at the Ploneintranet (**advanced!**):

<https://github.com/ploneintranet/ploneintranet/pull/299>

## collective.elasticsearch

Another option for an advanced search integration is the younger project [Elasticsearch](https://www.elastic.co/elasticsearch/).
Like for Solr, the technical foundation is the Lucene index, written in Java.

Pros of Elasticsearch

- It uses JSON instead of an XML schema for (field) configuration,
  which might be easier to configure.
- Clustering and replication is built in from the beginning.
  It is easier to configure.
  Especially ad-hoc cluster which can (re)configure automatically.
- The project and community is agile and active.

Cons of Elasticsearch

- JSON is abused as Query DSL.
  It can lead to queries with up to 10 layers.
  This can be annoying especially if you write them programatically.

The integration of Elasticsearch with Plone is done with
<https://pypi.org/project/collective.elasticsearch/>

## Google Custom Search

Google provides a couple related tools for using Google as a
site-specific search engine embedded in your site:
Google Custom Search (free, ad-supported) and Google Site Search (paid).

```{note}
don't confuse these solutions with Google Search Appliance,
which was a rack-mounted device which has been discontinued.
```

Pros:

- Better ranking of results compared to ZCTextIndex.
- Fairly straightforward to integrate.
- GUI control panel for basic configuration.
- Don't have to run and maintain a separate Java service.
- Can easily be configured to search multiple websites.

Cons:

- Free version includes Google branding and ads in results.
- Cannot index private items.
- Changes are not indexed immediately (usually within a week).
- Only returns top 100 results for a query.
- Only useful for fulltext search, not searching specific fields.
- Limited control over result ranking and formatting.
- Google has a habit of discontinuing free services.
