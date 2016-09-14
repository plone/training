collective.solr JSON API
------------------------------------------------------------------------------

JSON Search API
***************

URL::

  http://localhost:8080/Plone/@@search?format=json&SearchableText=Plone

Javascript::

  GET http://localhost:8080/Plone/@@search?SearchableText=Plone
  Accept: application/json

Response::

    {
        "data":
    [
            {
                "description": "",
                "id": "front-page",
                "portal_type": "Document",
                "title": "Willkommen bei Plone",
                "url": "http://localhost:8080/Plone/front-page"
            }
        ],
        "suggestions": [ ]
    }


JSON Suggest API
****************

Solr Configuration (solr.cfg)::

    [solr-instance]
    recipe = collective.recipe.solrinstance
    ...
    additional-solrconfig =

      <!-- =================================================================== -->
      <!-- SUGGEST (INCLUDED IN THE DEFAULT SOLR SELECT REQUEST HANDLER)       -->
      <!-- =================================================================== -->

      <searchComponent name="spellcheck" class="solr.SpellCheckComponent">
        <str name="queryAnalyzerFieldType">title</str>
        <lst name="spellchecker">

          <!-- The DirectSolrSpellChecker is a spell checker that doesn't require building a separate, parallel index in order.
          https://wiki.apache.org/solr/DirectSolrSpellChecker -->

          <!--
              Optional, it is required when more than one spellchecker is configured.
              Select non-default name with spellcheck.dictionary in request handler.
          -->
          <str name="name">direct</str>

          <!--
              Load tokens from the following field for spell checking,
              analyzer for the field's type as defined in schema.xml are used
          -->
          <str name="field">Title</str>
          <str name="classname">solr.DirectSolrSpellChecker</str>

          <!-- the spellcheck distance measure used, the default is the internal levenshtein -->
          <str name="distanceMeasure">internal</str>

          <!-- minimum accuracy needed to be considered a valid spellcheck suggestion -->
          <float name="accuracy">0.2</float>

          <!-- the maximum #edits we consider when enumerating terms: can be 1 or 2 -->
          <int name="maxEdits">2</int>

          <!-- the minimum shared prefix when enumerating terms -->
          <int name="minPrefix">1</int>

          <!-- maximum number of inspections per result. -->
          <int name="maxInspections">5</int>

          <!-- minimum length of a query term to be considered for correction -->
          <int name="minQueryLength">3</int>

          <!-- maximum threshold of documents a query term can appear to be considered for correction -->
          <!--<float name="maxQueryFrequency">0.01</float>-->

          <!-- uncomment this to require suggestions to occur in 1% of the documents
            <float name="thresholdTokenFrequency">.01</float>
          -->

        </lst>
      </searchComponent>

      <!-- Include the suggest search component into the default '/select' request
           handler.

           See https://wiki.apache.org/solr/SpellCheckComponent#Request_Parameters for all spellcheck component request parameters.
      -->

      <requestHandler name="/select" class="solr.SearchHandler"
      startup="lazy">
        <lst name="defaults">
          <!-- Solr Default Select Request Handler -->
          <str name="echoParams">explicit</str>
          <int name="rows">500</int>

          <!-- Suggest -->
          <str name="df">Title</str>

          <!-- The name of the spellchecker to use. -->
          <str name="spellcheck.dictionary">direct</str>

          <!-- Turn on or off spellcheck suggestions for this request. -->
          <str name="spellcheck">on</str>

          <!-- Provide additional information about the suggestion, such as the frequency in the index. -->
          <str name="spellcheck.extendedResults">false</str>

          <!-- The maximum number of suggestions to return. -->
          <str name="spellcheck.count">5</str>

          <!-- A collation is the original query string with the best suggestions for each term replaced in it. -->
          <str name="spellcheck.collate">false</str>

          <!-- If true, returns an expanded response format detailing collations found. -->
          <str name="spellcheck.collateExtendedResults">false</str>

        </lst>
        <arr name="last-components">
          <str>spellcheck</str>
        </arr>
      </requestHandler>

URL:

    http://localhost:8080/Plone/@@search?format=json&SearchableText=Plane

Javascript::

  GET http://localhost:8080/Plone/@@search?SearchableText=Plane
  Accept: application/json

Response::

    {
        "data": [ ],
        "suggestions":
        {
            "plane":
            {
                "endOffset": 87,
                "numFound": 1,
                "startOffset": 82,
                "suggestion":
                    [
                        "plone"
                    ]
                }
            }
        }
    }


JSON Autocomplete API
*********************

Solr Configuration (solr.cfg)::

    [solr-instance]
    recipe = collective.recipe.solrinstance
    ...
    name:title_autocomplete     type:text_autocomplete indexed:true stored:true

    additional-schema-config =
      <!-- Additional field for autocomplete -->
      <copyField source="Title" dest="title_autocomplete" />

    extra-field-types =
      <!-- Custom autocomplete filter for the autocomplete field -->
      <fieldType class="solr.TextField" name="text_autocomplete">
        <analyzer>

          <!-- Creates tokens of characters separated by splitting on whitespace. -->
          <tokenizer class="solr.WhitespaceTokenizerFactory"/>

          <!-- Creates tokens by lowercasing all letters and dropping non-letters. -->
          <filter class="solr.LowerCaseFilterFactory"/>

          <!-- A ShingleFilter constructs shingles (token n-grams) from a token stream. In other words, it creates combinations of tokens as a single token. For example, the sentence "please divide this sentence into shingles" might be tokenized into shingles "please divide", "divide this", "this sentence", "sentence into", and "into shingles". -->
          <filter class="solr.ShingleFilterFactory" maxShingleSize="4" outputUnigrams="true"/>

          <!-- Create n-grams from the beginning edge of a input token: e.g.
          Nigerian => "ni", "nig", "nige", "niger", "nigeri", "nigeria", "nigeria", "nigerian" -->
          <filter class="solr.EdgeNGramFilterFactory" maxGramSize="20" minGramSize="2"/>

         </analyzer>
      </fieldType>

URL::

  http://localhost:8080/Plone/@@solr-autocomplete?term=Pl

Response::

    [
        {
            "value": "Willkommen bei Plone",
            "label": "Willkommen bei Plone"
        }
    ]




