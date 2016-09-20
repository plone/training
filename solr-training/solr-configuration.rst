Solr Buildout Configuration
------------------------------------------------------------------------------

Solr Multi Core
***************

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance:mc
    cores =
      collection1
      collection2
      collection3
      testing
    default-core-name = collection1


Stopwords
*********

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    filter =
        text solr.StopFilterFactory ignoreCase="true" words="${buildout:directory}/etc/stopwords.txt"

stopwords.txt::

    der
    die
    das
    und
    oder

http://svn.apache.org/repos/asf/lucene/dev/trunk/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/german_stop.txt


Stemming
********

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    ...
    filter =
    #    text solr.GermanMinimalStemFilterFactory  # Less aggressive
    #    text solr.GermanLightStemFilterFactory  # Moderately aggressiv
    #    text solr.SnowballPorterFilterFactory language="German2"  # More aggressive
        text solr.StemmerOverrideFilterFactory dictionary="${buildout:directory}/etc/stemdict.txt" ignoreCase="false"

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
********

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    ...
    filter-index =
    # The recommended approach for dealing with synonyms is to expand the synonym
    # when indexing. See: http://wiki.apache.org/solr/AnalyzersTokenizersTokenFilters#solr.SynonymFilterFactory
        text solr.SynonymFilterFactory synonyms="${buildout:directory}/etc/synonyms.txt" ignoreCase="true" expand="true"

synonyms.txt::

    #Explicit mappings match any token sequence on the LHS of "=>"
    #and replace with all alternatives on the RHS.  These types of mappings #ignore the expand parameter in the schema.
    #Examples:
    i-pod, i pod => ipod,
    sea biscuit, sea biscit => seabiscuit

    #Equivalent synonyms may be separated with commas and give #no explicit mapping.  In this case the mapping behavior will #be taken from the expand parameter in the schema.  This allows #the same synonym file to be used in different synonym handling strategies.
    #Examples:
    ipod, i-pod, i pod
    foozball , foosball
    universe , cosmos

    # If expand==true, "ipod, i-pod, i pod" is equivalent to the explicit mapping:
    ipod, i-pod, i pod => ipod, i-pod, i pod # If expand==false, "ipod, i-pod, i pod" is equivalent to the explicit mapping:
    ipod, i-pod, i pod => ipod

    #multiple synonym mapping entries are merged.
    foo => foo bar
    foo => baz
    #is equivalent to
    foo => foo bar, baz


Autocomplete
************

solr.cfg::

    [solr]
    recipe = collective.recipe.solrinstance
    ...
    additional-schema-config =
      <copyField source="Title" dest="title_autocomplete" />
      <copyField source="Description" dest="description_autocomplete" />
      <copyField source="Title" dest="title_suggest" />

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


    # Solr Config => parts/solr/solr/collection1/conf/solrconfig.xml
    additional-solrconfig =

      <!-- =================================================================== -->
      <!-- AUTOCOMPLETE                                                        -->
      <!-- =================================================================== -->

      <requestHandler name="/autocomplete" class="solr.SearchHandler">
        <lst name="defaults">

          <!-- defType: a reference to the query parser that is used.
               The 'edismax' query parser adds features to enhance search relevancy.
               https://wiki.apache.org/solr/ExtendedDisMax -->
          <str name="defType">edismax</str>

          <!-- rows: maximum number of documents included in the response
               https://wiki.apache.org/solr/CommonQueryParameters#rows -->
          <str name="rows">10</str>

          <!-- fl: field list to be returned in the response. -->
          <str name="fl">description_autocomplete,title_autocomplete,score</str>

          <!-- qf: query fields list with 'boosts' that are associated with each
               field.
               https://wiki.apache.org/solr/ExtendedDisMax#qf_.28Query_Fields.29
               -->
          <str name="qf">title_autocomplete^30 description_autocomplete^50.0</str>

          <!-- pf: phrase fields list to 'boost' the score (after 'fq' and 'qf')
               of documents where terms in 'q' appear in close proximity.
               https://wiki.apache.org/solr/ExtendedDisMax#pf_.28Phrase_Fields.29
               -->
          <str name="pf">title_autocomplete^30 description_autocomplete^50.0</str>

          <!-- result grouping:
               https://wiki.apache.org/solr/FieldCollapsing#Request_Parameters -->
          <str name="group">true</str>
          <str name="group.field">title_autocomplete</str>
          <str name="group.field">description_autocomplete</str>
          <str name="sort">score desc</str>
          <str name="group.sort">score desc</str>

        </lst>
      </requestHandler>


Suggest
*******

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

