---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Solr Buildout Configuration

## Solr Multi Core

Solr allows creating multiple cores which can be indexed and queried independently.
However, collective.solr does not currently support multicore setups.
It always uses the default core for indexing and searching.

A core is defined by creating a file called core.properties. In our example setup there
is exactly one of these files. It specifies the name of the core.

core.properties

```ini
name=plone
```

It could also contain other property definitions. To define more cores we could add more
files of the same name in other directories.

```{seealso}
https://solr.apache.org/guide/8_2/defining-core-properties.html
```

## Stopwords

For indexes with a lot of text,
common uninteresting words like *"the"*, *"a"*, and so on, make the index large and slow down phrase queries.
To deal with this problem, it is best to remove them from fields where they show up often.

We need to add the **StopFilterFactory** with a reference to a text file with one stop word per line to the Solr configuration:

schema.xml

```xml
<fieldType name="text" class="solr.TextField" positionIncrementGap="100">
    [...]
    <analyzer type="index">
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        [...]
```

`stopwords.txt`:

```
a
the
i
```

For some common language specific examples see the Solr git repository:

```{seealso}
https://github.com/apache/solr
```

## Stemming

Stemming is a language specific operation which tries to reduce terms to a base form.

Here is an example:

```
"riding", "rides", "horses" ==> "ride", "ride", "hors".
```

This can help in some situations but may hurt in others.

For example,
if you run an intranet and people usally know exactly what they are looking for it is probably not a good idea,
but if you provide a Google-like search where you browse more than search then stemming is probably for you.

If you are interested in this feature look at the Solr documentation here:

```{seealso}
https://solr.apache.org/guide/8_2/understanding-analyzers-tokenizers-and-filters.html
```

```{seealso}
https://cwiki.apache.org/confluence/display/solr/LanguageAnalysis
```

A short example to include a German stemming factory is here:

schema.xml

```xml
<fieldType name="text" class="solr.TextField" positionIncrementGap="100">
    [...]
    <analyzer type="index">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <!-- <filter class="solr.GermanMinimalStemFilterFactory"/>  # Less aggressive -->
        <!-- <filter class="solr.GermanLightStemFilterFactory"/>  # Moderately aggressiv -->
        <!-- <filter class="solr.SnowballPorterFilterFactory" language="German2"/>  More aggressive -->
        <filter class="solr.StemmerOverrideFilterFactory"
                dictionary="stemdict.txt" ignoreCase="false" />
```

`stemdict.txt`:

```
# english stemming
monkeys monkey
otters  otter

# some crazy ones that a stemmer would never do
dogs    cat

# German stemming
gelaufen    lauf
lief        lauf
risiken     risiko
```

## Synonyms

Solr can deal with synonyms.
Maybe you run a shop for selling smartphones and you want people typing "iphone",
"i-phone" or even "ephone", "ifone", or "iphnoe" to get the latest "iPhone" offers.

A simple synonym like solution is to use the *searchwords* extension which is provided by collective.solr.
It is a schemaextender for all types and allows to specify terms which are boosted by factor 1000 in the default search query.
For "real" synonyms implemented in Solr you can use the *SynonymGraphFilterFactory*:

schema.xml

```xml
<fieldType name="text" class="solr.TextField" positionIncrementGap="100">
    [...]
    <analyzer type="index">
        <filter class="solr.SynonymGraphFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
        [...]
```

Note that the SynonymFilterFactory is an index filter and not a query filter.

`synonyms.txt`:

```
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
```

For a full list of index and query filter factories consult the Solr documentation:

```{seealso}
https://solr.apache.org/guide/6_6/understanding-analyzers-tokenizers-and-filters.html
```

## Exercise

Experiment with stemming, stop words and synonyms.
Add your own values and see how Solr behaves.
