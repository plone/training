More Features...
=====================

Next we will cover some more advanced topics which need configuration
on Plone and Solr side. Features like autocomplete and suggest
(did you mean ...) are often requested when it comes to search.
They are perfectly doable with the Plone / Solr combination.

Let's see how and start with autocomplete: 

Autocomplete
--------------

For autocomplete we need a special Solr handler because we don't search
full terms but only part of terms.

solr.cfg::

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

For the search template we utilize the HTML5 datalist element to populate 
the search input field.

search.pt::

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


Suggest
--------

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    ...

    additional-solrconfig =
      <!-- =================================================================== -->
      <!-- SUGGEST                                                             -->
      <!-- =================================================================== -->
       <!-- Spell Check

            The spell check component can return a list of alternative spelling
            suggestions.

            http://wiki.apache.org/solr/SpellCheckComponent
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

           See http://wiki.apache.org/solr/SpellCheckComponent for details
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

search.pt::

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

