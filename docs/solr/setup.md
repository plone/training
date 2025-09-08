---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Setup

For using {term}`Solr` with Plone you need:

- A running Solr server
- An integration product (like [collective.solr](https://github.com/collective/collective.solr)) for delegation of indexing and searching to the Solr server.

In this training we will focus on collective.solr for this purpose.

Bootstrap project:

```console
mkdir plone-training-solr
cd plone-training-solr
curl -O https://bootstrap.pypa.io/bootstrap-buildout.py
curl -o plone5.cfg https://raw.githubusercontent.com/collective/minimalplone5/master/buildout.cfg
mkdir -p config/conf
cd config
curl -O https://raw.githubusercontent.com/kitconcept/kitconcept.recipe.solr/master/config/core.properties
cd conf
curl -O 'https://raw.githubusercontent.com/kitconcept/kitconcept.recipe.solr/master/config/conf/{mapping-FoldToASCII.txt,schema.xml,solrconfig.xml,stopwords.txt,synonyms.txt}'
cd ../..
```

Create a buildout (*buildout.cfg*) which installs both requirements

```ini
[buildout]
extends =
    plone5.cfg
parts +=
    solr

[instance]
eggs +=
    collective.solr

[solr]
recipe = kitconcept.recipe.solr
src = http://archive.apache.org/dist/lucene/solr/8.2.0/solr-8.2.0.tgz
solr-config = config

[versions]
collective.solr = 8.0.0a5
kitconcept.recipe.solr = 1.0.0a5
```

Run buildout:

```console
python bootstrap-buildout.py
bin/buildout
```

Start Plone in foreground mode to see that everything is working:

```console
bin/instance fg
```

Start Solr in another terminal in foreground mode:

```console
bin/solr-foreground
```

## Solr Buildout

We assume you are more or less familiar with the Plone buildout,
but let's analyze the solr buildout configuration a bit.

First we have an extra buildout part in *buildout.cfg*:

```ini
[buildout]
parts +=
    solr

[...]

[solr]
recipe = kitconcept.recipe.solr
src = http://archive.apache.org/dist/lucene/solr/8.2.0/solr-8.2.0.tgz
solr-config = config
```

The recipe kitconcept.recipe.solr takes care of downloading solr and putting the configuration files in the right place.
The *src* option specifies the URL to download solr from. With *solr-config* you specify a local directory that holds the configuration for the solr server.

In a production environment you might set up solr with a provisioning tool like ansible or chef instead. For buildout there is also [collective.recipe.solrinstance](https://pypi.org/project/collective.recipe.solrinstance/) but it doesn't support current solr versions.

```{note}
At time of writing the latest working version of Solr was 8.4.x
```

Like the Zope ZCatalog the Solr index has a schema consisting of index and metadata fields.
You can think of index fields as something you can use for querying / searching and metadata something you return as result list.

Solr defines its schema in a big XML file called `schema.xml`. The main part is the *\<fields>* element, which lists the fields that are indexed.

```xml
<fields>
  <field name="id"                    type="string"   indexed="true"  stored="true" required="false" />
  <field name="_version_"             type="long"     indexed="true"  stored="true"/>

  <!-- Plone Core Fields -->
  <field name="allowedRolesAndUsers"  type="string"   indexed="true"  stored="true"  multiValued="true" />
  <field name="created"               type="date"     indexed="true"  stored="true" />
  <field name="Creator"               type="string"   indexed="true"  stored="true" />
  <field name="Date"                  type="date"     indexed="true"  stored="true" />
  <field name="default"               type="text"     indexed="true"  stored="false"  multiValued="true" />
  <field name="Description"           type="text"     indexed="true"  stored="true" />
  <field name="effective"             type="date"     indexed="true"  stored="true" />
  <field name="exclude_from_nav"      type="boolean"  indexed="false" stored="true" />
  <field name="expires"               type="date"     indexed="true"  stored="true" />
  <field name="getIcon"               type="string"   indexed="false" stored="true" />
  <field name="getId"                 type="string"   indexed="false" stored="true" />
  <field name="getRemoteUrl"          type="string"   indexed="false" stored="true" />
  <field name="is_folderish"          type="boolean"  indexed="true"  stored="true" />
  <field name="Language"              type="string"   indexed="true"  stored="true" />
  <field name="modified"              type="date"     indexed="true"  stored="true" />
  <field name="object_provides"       type="string"   indexed="true"  stored="true"  multiValued="true" />
  <field name="path_depth"            type="tint"     indexed="true"  stored="true" />
  <field name="path_parents"          type="string"   indexed="true"  stored="true"  multiValued="true" />
  <field name="path_string"           type="string"   indexed="false" stored="true" />
  <field name="portal_type"           type="string"   indexed="true"  stored="true" />
  <field name="review_state"          type="string"   indexed="true"  stored="true" />
  <field name="SearchableText"        type="text"     indexed="true"  stored="true" />
  <field name="searchwords"           type="string"   indexed="true"  stored="true"  multiValued="true" />
  <field name="showinsearch"          type="boolean"  indexed="true"  stored="true" />
  <field name="sortable_title"        type="string"     indexed="true"  stored="true" />
  <field name="Subject"               type="string"   indexed="true"  stored="true"   multiValued="true" />
  <field name="Title"                 type="text"     indexed="true"  stored="true" />
  <field name="Type"                  type="string"   indexed="true"  stored="true" />
  <field name="UID"                   type="string"   indexed="true"  stored="true"   required="false" />

  <copyField source="Title" dest="default"/>
  <copyField source="Description" dest="default"/>
  <copyField source="Subject" dest="default"/>

  <copyField source="default" dest="SearchableText"/>

</fields>
```

- name: Name of the field
- type: Type of the field (e.g. `string` , `text`, `date`, `boolean`)
- indexed: The field is searchable
- stored: The field is returned as metadata

copyField: copy content to another field, e.g. copy title, description and subject to default.

```{seealso}
https://cwiki.apache.org/confluence/display/solr/SchemaXml#SchemaXml-Commonfieldoptions
```

This is the bare minimum for configuring Solr. There are more options supported by Solr,
most notably the custom extensions for *schema.xml* and *solrconfig.xml*.

We will see examples for this later on in the training.

To learn more about all the files in the config/ directory please refer to the apache solr documentation ([Solr Configuration Files](https://solr.apache.org/guide/8_2/solr-configuration-files.html), [The Well-Configured Solr Instance](https://solr.apache.org/guide/8_2/the-well-configured-solr-instance.html)).

After running the buildout,
which downloads and configures Solr and Plone, we are ready to fire up both servers.

## Plone And Solr

To activate Solr in Plone *collective.solr* needs to be activated as an add-on in Plone.

Activating the Solr add-on adds a configuration page to the controlpanel.
It can be accessed via \<PORTAL_URL>/@@solr-controlpanel or via "Configuration" -> "Solr Settings"

Check: {guilabel}`Active`, click {guilabel}`Save`

Activating Solr in the control panel activates a patch of Plones indexing
and search methods to use Solr for indexing and querying.

```{note}
Note that ZCatalog is not replaced but Solr is *additionally* used
for indexing and searching.
```

### Control Panel Configuration

> - *Active* - Turn connection between Plone and Solr on/off.
> - *Host* - The host name of the Solr instance to be used. Defaults to 127.0.0.1
> - *Port* - The port of the Solr instance to be used. Defaults to 8983
> - *Base* - The base prefix of the Solr instance to be used. Defaults to /solr
> - *Asynchronous indexing* - Check to enable asynchronous indexing operations,
>   which will improve Zope response times in return for not having the Solr
>   index updated immediately.
> - *Automatic commit* - If enabled each index operation will cause a commit to be sent to Solr,
>   which causes it to update its index.
>   If you disable this, you need to configure commit policies on the Solr server side.
> - *Commit within*

#### Timeouts And Search Limit

> - Index timeout
> - Search timeout
> - Maximum search results

#### Search Query Configuration

> - Required query parameters
> - Pattern for simple search queries
> - Default search facets
> - Filter query parameters
> - Slow query threshold
> - Effective date steps
> - Exclude user from allowedRolesAndUsers

#### Highlighting

<https://cwiki.apache.org/confluence/display/solr/HighlightingParameters>

> - Highlighting fields
> - Highlight formatter: pre
> - Highlight formatter: post
> - Highlight Fragment Size
> - Default fields to be returned
> - Levensthein distance

#### Atomic Updates And Boosting

> - Enable atomic updates
> - Python script for custom index boosting

With Solr activated, searching in Plone works like the following:

> - Search contains one of the fields set as required
>   (which is normally the fulltext field *SearchableText*)
>   -> Solr results are returned
> - Search does not contain all fields marked as required
>   -> ZCatalog results are returned.
>   Which is the case for rendering the navigation,
>   folder contents, etc.
> - The search contains the stanza *use_solr=True*.
>   -> Solr results are returned independent of the required fields.

After first activating collective.solr, the search will not find anything yet. Every object you subsequently add or modify will be indexed in solr, but at the moment the solr index is still empty. To populate it, go to the solr configuration and click "Solr Reindex", or call \<PORTAL_URL>/@@solr-maintenance/reindex.

Then you are ready for your first search.
Search for *Plone*.

You should get the frontpage as a result--which is not super awesome to begin with because we have this without Solr too--but it is the first step in utilizing the full power of Solr.

### Configuration With ZCML

Another way to configure the connection is via {term}`ZCML`.
You can use the following snippet to configure host, port und basepath:

```xml
<configure xmlns:solr="http://namespaces.plone.org/solr">
  <solr:connection host="127.0.0.23" port="3898" base="/foo" />
</configure>
```

The ZCML configuration takes precedence over the configuration in the registry / control-panel.

## Committing Strategies

### Synchronous Immediately

The default commit strategy is to commit to Solr on every Zope commit.
This ensures an always up to date index but may come at the cost of indexing time especially when doing batch operations like data import.

To use this behavior, turn **Automatic commit** ON in the Solr control panel in Plone.

### Synchronous Batched

Another commit strategy is to do timed commits in Solr.
This method is usually way faster but comes with the downside of index delays.

To use this behavior you have to do two things:

> - Turn **Automatic commit** OFF in the Solr control panel in Plone.
>
> - Set one or both of the following *\<autoCommit>* options in solrconfig.xml:
>
>   - `<maxDocs>` - The number of updates that have occurred since the last commit.
>   - `<maxTime>` - The number of milliseconds since the oldest uncommitted update.

It could look like this:

```xml
<autoCommit>
  <maxTime>15000</maxTime>
  <openSearcher>false</openSearcher>
</autoCommit>
```

### Asynchronous

The third commit strategy is to do full asynchronous commits.
This can be activated by setting the Flag **Asynchronous indexing** in the Solr control panel to {guilabel}`ON`.
This behavior is the most efficient in terms of Zope response time.

Since it is fire and forget the consistency could be harmed in the interim.
It is advisable to do a sync or full-index from time to time if you work with this strategy.

Additional information can be found in the Solr documentation:

```{seealso}
https://solr.apache.org/guide/8_2/updatehandlers-in-solrconfig.html#UpdateHandlersinSolrConfig-commitWithin
```

## Exercise

Have a running Plone and Solr with collective.solr active and experiment with commit strategies.
