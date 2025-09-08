---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# More Features

Next we will cover some more advanced topics which need configuration on Plone and Solr side.
Features like autocomplete and suggest ("did you mean ...") are often requested when it comes to search.
They are perfectly doable with the Plone / Solr combination.

At the end of this chapter we will build a full search page with autocomplete, suggest, term highlighting and faceting turned on.

Let's see how and start with autocomplete:

## Autocomplete

For autocomplete we need a special Solr handler because we don't search full terms but only part of terms.

With the additional Solr configuration, autocomplete can be called via URL directly:

```
http://localhost:8080/Plone/@@solr-autocomplete?term=Pl
```

Which gives the response

```
[
    {
        "value": "Willkommen bei Plone",
        "label": "Willkommen bei Plone"
    }
]
```

{file}`solr.cfg`

```ini
[solr-instance]
recipe = collective.recipe.solrinstance
...
name:title_autocomplete type:text_auto indexed:true stored:true
name:description_autocomplete type:text_desc indexed:true stored:true

additional-solrconfig =
  <!-- request handler to return typeahead suggestions -->
  <requestHandler name="/autocomplete" class="solr.SearchHandler">
    <lst name="defaults">
      <str name="echoParams">explicit</str>
      <str name="defType">edismax</str>
      <str name="rows">10</str>
      <str name="fl">description_autocomplete,title_autocomplete,score</str>
      <str name="qf">title_autocomplete^30 description_autocomplete^50.0</str>
      <str name="pf">title_autocomplete^30 description_autocomplete^50.0</str>
      <str name="group">true</str>
      <str name="group.field">title_autocomplete</str>
      <str name="group.field">description_autocomplete</str>
      <str name="sort">score desc</str>
      <str name="group.sort">score desc</str>
    </lst>
  </requestHandler>

extra-field-types =
  <fieldType class="solr.TextField" name="text_auto">
    <analyzer>
      <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.ShingleFilterFactory" maxShingleSize="4" outputUnigrams="true"/>
      <filter class="solr.EdgeNGramFilterFactory" maxGramSize="20" minGramSize="1"/>
     </analyzer>
  </fieldType>
  <fieldType class="solr.TextField" name="text_desc">
    <analyzer>
      <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.ShingleFilterFactory" maxShingleSize="4" outputUnigrams="true"/>
      <filter class="solr.EdgeNGramFilterFactory" maxGramSize="20" minGramSize="1"/>
     </analyzer>
   </fieldType>

additional-schema-config =
  <copyField source="Title" dest="title_autocomplete" />
  <copyField source="Description" dest="description_autocomplete" />
```

For the search template we utilize the HTML5 datalist element to populate the search input field.

{file}`search.pt`:

```html
<html lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="plone">
<body>
  <metal:content-core fill-slot="content-core">
    <input type="text" list="searchresults"
           id="acsearch" placeholder="Search site ..." />
    <datalist id="searchresults" />

    <script>
      $(document).ready(function() {
        $("#acsearch").on("input", function(e) {
          var val = $(this).val();
          if(val.length < 2) return;
          $.get("solr-autocomplete", {term:val}, function(res) {
            var dataList = $("#searchresults");
            dataList.empty();
            if(res.length) {
              for(var i=0, len=res.length; i<len; i++) {
                var opt = $("<option></option>").attr("value", res[i].label);
                dataList.append(opt);
              }
            }
          }, "json");
        });
      })
    </script>
  </metal:content-core>
</body>
</html>
```

## Suggest

The suggest (did you mean ...) feature is well known from popular search engines.
It is integrated into Solr as a component which needs to be enabled and configured.
Here is an example configuration which works with {py:mod}`collective.solr`.
If you change it, stick to the names of the parameters and handlers.

The JSON view of Plone can be called with this URL:
`http://localhost:8080/Plone/@@search?format=json&SearchableText=Plane`

And from JavaScript

```http
GET http://localhost:8080/Plone/@@search?SearchableText=Plane HTTP/1.1
Accept: application/json
```

We get a response like this

```json
{
    "data": [],
    "suggestions": {
            "plane": {
                    "endOffset": 87,
                    "numFound": 1,
                    "startOffset": 82,
                    "suggestion": ["plone"]
            }
    }
}
```

The configuration in buildout is as follows:

```ini
[solr-instance]
recipe = collective.recipe.solrinstance
...

additional-solrconfig =
  <!-- =================================================================== -->
  <!-- SUGGEST                                                             -->
  <!-- =================================================================== -->
   <!-- Spell Check

        The spell check component can return a list of alternative spelling
        suggestions.

        https://wiki.apache.org/solr/SpellCheckComponent
     -->
  <searchComponent name="spellcheck" class="solr.SpellCheckComponent">

    <str name="queryAnalyzerFieldType">SearchableText</str>

    <!-- Multiple "Spell Checkers" can be declared and used by this
         component
      -->

    <!-- a spellchecker built from a field of the main index -->
    <lst name="spellchecker">
      <str name="name">default</str>
      <str name="field">SearchableText</str>
      <str name="classname">solr.DirectSolrSpellChecker</str>
      <!-- the spellcheck distance measure used, the default is the internal levenshtein -->
      <str name="distanceMeasure">internal</str>
      <!-- minimum accuracy needed to be considered a valid spellcheck suggestion -->
      <float name="accuracy">0.5</float>
      <!-- the maximum #edits we consider when enumerating terms: can be 1 or 2 -->
      <int name="maxEdits">2</int>
      <!-- the minimum shared prefix when enumerating terms -->
      <int name="minPrefix">1</int>
      <!-- maximum number of inspections per result. -->
      <int name="maxInspections">5</int>
      <!-- minimum length of a query term to be considered for correction -->
      <int name="minQueryLength">4</int>
      <!-- maximum threshold of documents a query term can appear to be considered for correction -->
      <float name="maxQueryFrequency">0.01</float>
      <!-- uncomment this to require suggestions to occur in 1% of the documents
        <float name="thresholdTokenFrequency">.01</float>
      -->
    </lst>

    <!-- a spellchecker that can break or combine words.  See "/spell" handler below for usage -->
    <lst name="spellchecker">
      <str name="name">wordbreak</str>
      <str name="classname">solr.WordBreakSolrSpellChecker</str>
      <str name="field">SearchableText</str>
      <str name="combineWords">true</str>
      <str name="breakWords">true</str>
      <int name="maxChanges">10</int>
    </lst>

    <!-- Custom Spellchecker -->
    <lst name="spellchecker">
      <str name="name">suggest</str>
      <str name="classname">org.apache.solr.spelling.suggest.Suggester</str>
      <str name="lookupImpl">org.apache.solr.spelling.suggest.fst.WFSTLookupFactory</str>
      <str name="field">SearchableText</str>
      <float name="threshold">0.0005</float>
      <str name="buildOnCommit">true</str>
    </lst>

  </searchComponent>

  <!-- A request handler for demonstrating the spellcheck component.

       NOTE: This is purely as an example.  The whole purpose of the
       SpellCheckComponent is to hook it into the request handler that
       handles your normal user queries so that a separate request is
       not needed to get suggestions.

       IN OTHER WORDS, THERE IS REALLY GOOD CHANCE THE SETUP BELOW IS
       NOT WHAT YOU WANT FOR YOUR PRODUCTION SYSTEM!

       See https://wiki.apache.org/solr/SpellCheckComponent for details
       on the request parameters.
    -->
  <requestHandler name="/spell" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <!-- Solr will use suggestions from both the 'default' spellchecker
           and from the 'wordbreak' spellchecker and combine them.
           collations (re-written queries) can include a combination of
           corrections from both spellcheckers -->
      <str name="spellcheck.dictionary">default</str>
      <str name="spellcheck.dictionary">wordbreak</str>
      <str name="spellcheck.dictionary">suggest</str>
      <str name="spellcheck">on</str>
      <str name="spellcheck.extendedResults">true</str>
      <str name="spellcheck.count">10</str>
      <str name="spellcheck.alternativeTermCount">5</str>
      <str name="spellcheck.maxResultsForSuggest">5</str>
      <str name="spellcheck.collate">true</str>
      <str name="spellcheck.collateExtendedResults">true</str>
      <str name="spellcheck.maxCollationTries">10</str>
      <str name="spellcheck.maxCollations">5</str>
    </lst>
    <arr name="last-components">
      <str>spellcheck</str>
    </arr>
  </requestHandler>
```

A simple integration in our training-search is here:

```html
<html lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="plone">
<body>
  <metal:content-core fill-slot="content-core">
    <input type="text" list="searchresults"
           id="acsearch" placeholder="Search site ..." />
    <datalist id="searchresults" />

    <script>
      $(document).ready(function() {
        $("#acsearch").on("input", function(e) {
          var val = $(this).val();
          if(val.length < 2) return;
          $.get("suggest-terms", {term:val}, function(res) {
            var dataList = $("#searchresults");
            dataList.empty();
            if(res.length) {
              for(var i=0, len=res.length; i<len; i++) {
                var opt = $("<option></option>").attr("value", res[i].label);
                dataList.append(opt);
              }
            }
          }, "json");
        });
      })
    </script>
  </metal:content-core>
</body>
</html>
```

## Facetting

Facetting is tightly integrated in :py:mod::`collective.solr` and works out of the box.
We will now create a full search page with faceting, autocomplete, search term highlighting and suggest enabled.
The HTML of the page is mainly taken from the standard page.
To reduce complexity some of the standard features like syndication,  i18n and view actions have been removed:

```html
<html metal:use-macro="here/main_template/macros/master">
<head>
  <metal:block fill-slot="top_slot"
               tal:define="dummy python:request.set('disable_border',1);
                   disable_column_one python:request.set('disable_plone.leftcolumn',1);
                   enable_column_two python:request.set('disable_plone.rightcolumn',0);"/>
  <metal:block fill-slot="column_one_slot"/>

  <metal:js fill-slot="javascript_head_slot">
    <script type="text/javascript" src=""
            tal:attributes="src string:${portal_url}/++resource++collective.showmore.js">
    </script>
    <script type="text/javascript">

  $(document).ready(function() {
    $("#acsearch").on("input", function(e) {
      var val = $(this).val();
      if(val.length < 2) return;
      $.get("solr-autocomplete", {term:val}, function(res) {
        var dataList = $("#searchresults");
        dataList.empty();
        if(res.length) {
          for(var i=0, len=res.length; i<len; i++) {
            var opt = $("<option></option>").attr("value", res[i].label);
            dataList.append(opt);
          }
        }
      },"json");
    });
  })


    </script>
  </metal:js>
</head>

<body>
<div metal:fill-slot="main"
     tal:define="results view/search">
  <form name="searchform"
        action="search"
        class="searchPage"
        tal:attributes="action request/getURL">
    <input class="searchPage" name="SearchableText" id="acsearch" type="text"
           size="25" list="searchresults" title="Search Site"
           placeholder="Search Site ..."
           tal:attributes="value request/SearchableText|nothing;"/>
    <datalist id="searchresults"/>
    <input class="searchPage searchButton" type="submit" value="Search"/>
    <div tal:define="view nocall: context/@@search-facets | nothing"
         tal:condition="python: view"
         tal:replace="structure view/hiddenfields"/>
  </form>
  <h1 class="documentFirstHeading">
    Search results
    <span class="discreet">
        &mdash;
      <span tal:content="python:len(results)">234</span>
      items matching your search terms
    </span>
  </h1>

  <div tal:condition="not: view/has_results">
    <p tal:define="suggest view/suggest">
      <tal:noresuls>No results were found.</tal:noresuls>
      <tal:suggest condition="suggest">Did you mean:
        <strong>
          <a href="" tal:attributes="href suggest/url"
             tal:content="suggest/word">Plone</a>
        </strong>
      </tal:suggest>
    </p>
  </div>
  <div tal:condition="results" id="content-core">
    <dl class="searchResults">
      <tal:results repeat="result results">
        <dt tal:attributes="class result/ContentTypeClass">
          <a href="#"
             tal:attributes="href result/getURL;
                             class string:state-${result/review_state}"
             tal:content="result/Title"/>
        </dt>
        <dd>
          <span tal:replace="result/CroppedDescription">Cropped description</span>
          <br/>
        </dd>
      </tal:results>
    </dl>
    <div metal:use-macro="here/batch_macros/macros/navigation"/>
  </div>

</div>
<div metal:fill-slot="portlets_two_slot">
  <div tal:define="facet_view nocall: context/@@search-facets;
                     results view/search;"
       tal:condition="view/has_results"
       tal:replace="structure python:facet_view(results=results._sequence._basesequence)"/>
</div>
</body>
</html>
```

Let's analyze the important parts.
The head includes a reference to the {file}`showmore.js` JavaScript,
which is included in :py:mod::`collective.solr` and used to reduce long lists of facets.

Additionally the left column is removed on the search page.
The right column is kept.
No portlets will be displayed, it is used for the facets.

The first thing we do in our search is getting the results for the search query, if there is one:

```python
def search(self):
    if not self.request.get('SearchableText'):
        return []
    catalog = api.portal.get_tool('portal_catalog')
    results = IContentListing(catalog(hl='true', **self.request.form))
    self.has_results = bool(len(results))
    b_start = self.request.get('b_start', 0)
    batch = Batch(results, size=20, start=b_start)
    return batch
```

We can use the standard Plone catalog API for getting the results.

```{note}
Don't use {py:meth}`plone.api.content.find` because it "fixes" the query to match the indexes defined in ZCatalog and will strip all Solr-related query parameters.
We don't want that.
```

After we have the results, we wrap it with `IContentListing` to have unified access to them.
Finally we create a Batch, to make sure long result sets are batched on our search view.

The next thing we have in our search view is the form itself

```python
<form name="searchform"
      action="search"
      class="searchPage"
      tal:attributes="action request/getURL">
  <input class="searchPage" name="SearchableText" id="acsearch" type="text"
         size="25" list="searchresults" title="Search Site"
         placeholder="Search Site ..."
         tal:attributes="value request/SearchableText|nothing;"/>
  <datalist id="searchresults"/>
  <input class="searchPage searchButton" type="submit" value="Search"/>
  <div tal:define="view nocall: context/@@search-facets | nothing"
       tal:condition="python: view"
       tal:replace="structure view/hiddenfields"/>
</form>
```

We have a input field for used input.
For the autocompletion we reference the datalist with the `list` attribute.
For the facets we need to render the `hiddenfields` snippet,
which is constructed by the `search-facets` view of `collective.solr`.
This snippet will add the necessary query parameters like **facet=true&facet.field=portal_type&facet.field=review_state**.

We use the `h1` element for displaying the number of elements.

The next section is reserved for the *suggest* snippet:

```html
<div tal:condition="not: view/has_results">
  <p tal:define="suggest view/suggest">
    <tal:noresuls>No results were found.</tal:noresuls>
    <tal:suggest condition="suggest">Did you mean:
      <strong>
        <a href="" tal:attributes="href suggest/url"
           tal:content="suggest/word">Plone</a>
      </strong>
    </tal:suggest>
  </p>
</div>
```

If no results are found with the query, a term is suggested.
This term is fetched from the `collective.solr` AJAX view **suggest-terms**.

The code in our view class is here

```python
def suggest(self):
    self.request.form['term'] = self.request.get('SearchableText')
    suggest_view = getMultiAdapter((self.context, self.request),
                                   name='suggest-terms')
    suggestions = json.loads(suggest_view())
    if suggestions:
        word = suggestions[0]['value']['word']
        query = self.request.form.copy()
        query['SearchableText'] = word
        return {'word': word,
                'url': '{0}?{1}'.format(self.request.getURL(),
                                        urlencode(query, doseq=1))}
    return ''
```

We get suggestions from the Solr handler and construct an URL for a new search with query parameters preserved.

The next thing we have is the result list.
There is nothing fancy in it.

We show the title, which is linked to the article found and the cropped description.

Finally we have the snippet for the facets in the right slot:

```
<div metal:fill-slot="portlets_two_slot">
    <div tal:define="facet_view nocall: context/@@search-facets;
                       results view/search;"
         tal:condition="view/has_results"
         tal:replace="structure python:facet_view(results=results._sequence._basesequence)"/>
  </div>
```

We call the facet view of :py:mod::`collective.solr` with our resultset and get the facets fully rendered as HTML.

```{note}
We need to pass the `real` Solr response to the facet view.
That's why we have to escape the batch (\_sequence) and the contentlisting (\_basesequence)
```

Now we have a fully functional Plone search with faceting, autocompletion, suggestion and term highlighting.
You can find the complete example on [GitHub](https://github.com/collective/plonetraining.solr_example).

## Exercise

Have a custom search page with autocomplete, suggest, highlighting and faceting working.
