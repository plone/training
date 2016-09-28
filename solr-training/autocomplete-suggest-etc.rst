More Features...
=====================

Next we will cover some more advanced topics which need configuration
on Plone and Solr side. Features like autocomplete and suggest
(did you mean ...) are often requested when it comes to search.
They are perfectly doable with the Plone / Solr combination.

Let's see how and start with autocomplete: 

Autocomplete
--------------


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
        <!-- SUGGEST (INCLUDED IN THE DEFAULT SOLR SELECT REQUEST HANDLER)       -->
        <!-- =================================================================== -->

        <searchComponent name="spellcheck" class="solr.SpellCheckComponent">
        <str name="queryAnalyzerFieldType">title</str>
        <lst name="spellchecker">
          <str name="name">direct</str>
          <str name="field">title_suggest</str>
          <str name="classname">solr.DirectSolrSpellChecker</str>
          <str name="distanceMeasure">internal</str>
          <float name="accuracy">0.2</float>
          <int name="maxEdits">2</int>
          <int name="minPrefix">1</int>
          <int name="maxInspections">5</int>
          <int name="minQueryLength">3</int>
          <!--<float name="maxQueryFrequency">0.01</float>-->
        </lst>
        </searchComponent>

        <requestHandler name="/select" class="solr.SearchHandler"
        startup="lazy">
        <lst name="defaults">
          <!-- Solr Default Select Request Handler -->
          <str name="echoParams">explicit</str>
          <int name="rows">500</int>
          <!-- Suggest -->
          <str name="df">title_suggest</str>
          <str name="spellcheck.dictionary">direct</str>
          <str name="spellcheck">on</str>
          <str name="spellcheck.extendedResults">true</str>
          <str name="spellcheck.count">5</str>
          <str name="spellcheck.collate">true</str>
          <str name="spellcheck.collateExtendedResults">true</str>
        </lst>
        <arr name="last-components">
          <str>spellcheck</str>
        </arr>
        </requestHandler>


Solr Import Handler
*******************

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance:mc
    additional-solrconfig =
      <!-- Generate a unique key when creating documents in solr -->
      <requestHandler name="/update" class="solr.UpdateRequestHandler">
        <lst name="defaults">
          <str name="update.chain">uuid</str>
        </lst>
      </requestHandler>

      <!-- Generate a unique key when importing documents from csv in solr -->
      <requestHandler name="/update/csv" class="solr.UpdateRequestHandler">
        <lst name="defaults">
          <str name="update.chain">uuid</str>
        </lst>
      </requestHandler>

      <updateRequestProcessorChain name="uuid">
        <processor class="solr.UUIDUpdateProcessorFactory">
          <str name="fieldName">id</str>
        </processor>
        <processor class="solr.RunUpdateProcessorFactory" />
      </updateRequestProcessorChain>


    [solr-geolocations-import]
    recipe = collective.recipe.template
    input = inline:
      #!/bin/sh
      # Delete all data
      curl http://${settings:solr-host}:${settings:solr-port}/solr/solr-core-geospatial/update?commit=true -H "Content-Type: text/xml" --data-binary '<delete><query>*:*</query></delete>'
      # Import data
      curl http://${settings:solr-host}:${settings:solr-port}/solr/solr-core-geospatial/update/csv?commit=true --data-binary @etc/geolocations.csv -H 'Content-type:text/csv; charset=utf-8'
    output = ${buildout:directory}/bin/solr-geolocations-import
    mode = 755


geolocations.csv::

    "location","geolocation"
    "01067 Dresden","51.057379, 13.715954"
    "01069 Dresden","51.04931, 13.744873"
    "01097 Dresden","51.060424, 13.745002"
    ...


Geospatial Search (with Autocomplete)
*************************************

Works just when querying Solr directly. collective.solr needs some minor
fixes. See https://github.com/collective/collective.solr/tree/spatial-filters.

solr.cfg::

    [solr-core-geospatial]
    max-num-results = 10
    unique-key = id
    index =
      name:id type:uuid indexed:true stored:true multivalued:false required:true
      name:location type:text indexed:true stored:true
      name:geolocation type:location indexed:true stored:true
      name:autocomplete type:text_auto indexed:true stored:true multivalued:true

    additionalFieldConfig =
      <dynamicField name="*_coordinate"  type="tdouble" indexed="true"  stored="false"/>

    extra-field-types =
      <fieldType name="uuid" class="solr.UUIDField" indexed="true" />
      <fieldType class="solr.TextField" name="text_auto">
        <analyzer>
          <tokenizer class="solr.WhitespaceTokenizerFactory"/>
          <filter class="solr.LowerCaseFilterFactory"/>
          <filter class="solr.ShingleFilterFactory" maxShingleSize="4" outputUnigrams="true"/>
          <filter class="solr.EdgeNGramFilterFactory" maxGramSize="20" minGramSize="1"/>
         </analyzer>
      </fieldType>

    # Copy field city -> autocomplete
    additional-schema-config =
      <copyField source="location" dest="autocomplete" />

    additional-solrconfig =
      <!-- Generate a unique key when creating documents in solr -->
      <requestHandler name="/update" class="solr.UpdateRequestHandler">
        <lst name="defaults">
          <str name="update.chain">uuid</str>
        </lst>
      </requestHandler>

      <!-- Generate a unique key when importing documents from csv in solr -->
      <requestHandler name="/update/csv" class="solr.UpdateRequestHandler">
        <lst name="defaults">
          <str name="update.chain">uuid</str>
        </lst>
      </requestHandler>

      <updateRequestProcessorChain name="uuid">
        <processor class="solr.UUIDUpdateProcessorFactory">
          <str name="fieldName">id</str>
        </processor>
        <processor class="solr.RunUpdateProcessorFactory" />
      </updateRequestProcessorChain>

    filter =
        text solr.LowerCaseFilterFactory

