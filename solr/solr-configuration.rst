***************************
Solr Buildout Configuration
***************************

Solr Multi Core
===============

solr.cfg::

    [solr-instance]
    recipe = collective.recipe.solrinstance:mc
    cores =
      collection1
      collection2
      collection3
      testing
    default-core-name = collection1

.. note:: collective.solr does not support multicore setups currently.
   It always uses the default core for indexing and searching. 

Stopwords
=========

For indexes with lot of text,
common uninteresting words like *"the"*, *"a"*, and so on, make the index large and slow down phrase queries.
To deal with this problem, it is best to remove them from fields where they show up often.

We need to add the **StopFilterFactory** with a reference to a text file with one stopword per line to the Solr configuration:

solr.cfg::

    [solr-instance]
    recipe = collective.recipe.solrinstance
    filter =
        text solr.StopFilterFactory ignoreCase="true" words="${buildout:directory}/etc/stopwords.txt"
    java_opts +=
        -Dsolr.allow.unsafe.resourceloading=true

Since we don't copy over the stopwords file to the *parts/solr-instance* directory we need
to allow Solr reading resource files outside its home directory.

stopwords.txt::

   a
   the
   i

For some common language secific examples see the Solr git repository:

.. seealso:: https://github.com/apache/lucene-solr/tree/master/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball


Stemming
========

Stemming is a language specific operation which try to reduce terms to a base form.

Here is an example::

  "riding", "rides", "horses" ==> "ride", "ride", "hors". 

This can help in some situations but may hurt in others.

For example,
if you run an intranet and people usally know exactly what they are looking for it is probably not a good idea,
but if you provide a Google-like search where you browse more than search then stemming is probably for you.

If you are interested in this feature look at the Solr documentation here:

.. seealso:: https://wiki.apache.org/solr/LanguageAnalysis

A short example to include a german stemming factory into the buildout is here:

solr.cfg::

    [solr-instance]
    recipe = collective.recipe.solrinstance
    ...
    filter =
    #    text solr.GermanMinimalStemFilterFactory  # Less aggressive
    #    text solr.GermanLightStemFilterFactory  # Moderately aggressiv
    #    text solr.SnowballPorterFilterFactory language="German2"  # More aggressive
        text solr.StemmerOverrideFilterFactory dictionary="${buildout:directory}/etc/stemdict.txt" ignoreCase="false"
    java_opts +=
        -Dsolr.allow.unsafe.resourceloading=true

stemdict.txt::

    # english stemming
    monkeys monkey
    otters  otter

    # some crazy ones that a stemmer would never do
    dogs    cat

    # german stemming
    gelaufen    lauf
    lief        lauf
    risiken     risiko


Synonyms
========

Solr can deal with synonyms.
Maybe you run a shop for selling smartphones and you want people typing "iphone",
"i-phone" or even "ephone", "ifone", or "iphnoe" to get the latest "iPhone" offers.

A simple synonym like solution is to use the *searchwords* extension which is provided by collective.solr.
It is a schemaextender for all types and allows to specify terms which are boosted by factor 1000 in the default search query.
For "real" synonyms implemented in Solr you can use the *SynonymFilterFactory*:

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    ...
    filter-index =
    # The recommended approach for dealing with synonyms is to expand the synonym
    # when indexing. See: http://wiki.apache.org/solr/AnalyzersTokenizersTokenFilters#solr.SynonymFilterFactory
        text solr.SynonymFilterFactory synonyms="${buildout:directory}/etc/synonyms.txt" ignoreCase="true" expand="true"

Note that the SynonymFilterFactory is an index filter and not a query filter.

synonyms.txt::

    #Explicit mappings match any token sequence on the LHS of "=>"
    #and replace with all alternatives on the RHS.  These types of mappings #ignore the expand parameter in the schema.
    #Examples:
    ipod => i-pod, i pod => ipod,

    #Equivalent synonyms may be separated with commas and give no explicit mapping.
    # In this case the mapping behavior will be taken from the expand parameter in the schema.
    # This allows the same synonym file to be used in different synonym handling strategies.
    #Examples:
    ipod, i-pod, i pod
    foozball , foosball
    universe , cosmos

    # expand: (optional; default: true) If true, a synonym will be expanded to all
    # equivalent synonyms. If false, all equivalent synonyms will be reduced
    # to the first in the list.

    #multiple synonym mapping entries are merged.
    foo => foo bar
    foo => baz
    #is equivalent to
    foo => foo bar, baz

For a full list of index and query filter factories consult the Solr documentation:

.. seealso:: https://cwiki.apache.org/confluence/display/solr/Understanding+Analyzers%2C+Tokenizers%2C+and+Filters

Exercise
========

Experiment with stemming, stopwords and synonyms.
Add your own values and see how Solr behaves.
