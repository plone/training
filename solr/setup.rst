=====
Setup
=====

For using :term:`Solr` with Plone you need:

- A running Solr server
- An integration product (like `collective.solr <https://github.com/collective/collective.solr>`_) for delegation of indexing and searching to the Solr server.

In this training we will focus on collective.solr for this purpose.

Bootstrap project:

.. code-block:: console

   mkdir plone-training-solr
   cd plone-training-solr
   curl -O https://bootstrap.pypa.io/bootstrap-buildout.py
   curl -O https://raw.githubusercontent.com/collective/collective.solr/master/solr.cfg
   curl -o plone5.cfg https://raw.githubusercontent.com/collective/minimalplone5/master/buildout.cfg
   curl -o solr4.cfg https://raw.githubusercontent.com/collective/collective.solr/master/solr-4.10.x.cfg

Create a buildout (*buildout.cfg*) which installs both requirements

.. code-block:: ini

    [buildout]
    extends =
        plone5.cfg
        solr.cfg
        solr4.cfg

    [instance]
    eggs +=
        collective.solr

    [versions]
    collective.solr = 6.0a1
    collective.recipe.solrinstance = 6.0.0b3


Run buildout:

.. code-block:: console

   python2.7 bootstrap-buildout.py
   bin/buildout

Start Plone in foreground mode to see that everything is working:

.. code-block:: console

   bin/instance fg

Start Solr in another terminal in foreground mode:

.. code-block:: console

   bin/solr-instance fg

Solr Buildout
=============

We assume you are more or less familiar with the Plone buildout,
but let's analyze the solr buildout configuration a bit.

First we have two buildout parts in *solr.cfg*:

.. code-block:: ini

    [buildout]
    parts +=
        solr-download
        solr-instance

As the name suggests *solr-download* gets the full Solr package from the official download server and unpacks it.
The part *solr-instance* is for configuring Solr. Let's continue with the details.

The base Solr settings specify the host (usually localhost or 127.0.0.1),
the port (8983 is the standard port of Solr)
and two Java parameters for specifying lower and upper memory limit.

More is usually better.

.. code-block:: ini

    [settings]
    solr-host = 127.0.0.1
    solr-port = 8983
    solr-min-ram = 128M
    solr-max-ram = 256M

If you want a rough idea on how much memory you should use,
follow the guidelines found in this article:

.. seealso:: https://lucidworks.com/2011/09/14/estimating-memory-and-storage-for-lucenesolr/

There is nothing fancy in the Solr download part.

It takes an URL to the Solr binary and an md5 sum for verification.

.. note::

   At time of writing the latest working version of Solr was 4.10.x

It looks like this in *solr.cfg* and *solr4.cfg*:

.. code-block:: ini

    [solr-download]
    recipe = hexagonit.recipe.download
    strip-top-level-dir = true

    [solr-download]
    url = https://archive.apache.org/dist/lucene/solr/4.10.4/solr-4.10.4.tgz
    md5sum = 8ae107a760b3fc1ec7358a303886ca06

The Solr instance part is more complicated.
It provides a subset of many,
many configuration options of Solr and the possibility to define the schema of the index::

    [solr-instance]
    recipe = collective.recipe.solrinstance
    solr-location = ${solr-download:location}
    host = ${settings:solr-host}
    port = ${settings:solr-port}
    basepath = /solr
    max-num-results = 500
    section-name = SOLR
    unique-key = UID
    logdir = ${buildout:directory}/var/solr
    default-search-field = default
    default-operator = and
    java_opts =
      -Dcom.sun.management.jmxremote
      -Djava.rmi.server.hostname=127.0.0.1
      -Dcom.sun.management.jmxremote.port=8984
      -Dcom.sun.management.jmxremote.ssl=false
      -Dcom.sun.management.jmxremote.authenticate=false
      -server
      -Xms${settings:solr-min-ram}
      -Xmx${settings:solr-max-ram}

Let's analyze them one by one:

.. code-block:: ini

   solr-location = ${solr-download:location}

Specify the location of Solr, dowloaded with the previous part.

.. code-block:: ini

   host = ${settings:solr-host}
   port = ${settings:solr-port}
   basepath = /solr

Base configuration for running Solr referencing previously defined settings.
With this configuration it is possible to access Solr in a browser with the following URL:
http://localhost:8983/solr

The section-name defines the name which can be used to reflect custom address and/or basepath settings in zope.conf.

.. code-block:: ini

   section-name = SOLR

It follows the following pattern in *zope.conf*:
if you use standard settings no changes in *zope.conf* are necessary.

.. code-block:: ini

    <product-config ${part:section-name}>
        address ${part:host}:${part:port}
        basepath ${part:basepath}
    </product-config>

.. note::

   Another easy way to use different hosts on development, staging
   and production machines is to define a host alias in /etc/hosts.

Like the Zope ZCatalog the Solr index has a schema consisting of index and metadata fields.
You can think of index fields as something you can use for querying / searching and metadata something you return as result list.

Solr defines its schema in a big XML file called ``schema.xml``.

There is a section in the ``collective.recipe.solrinstance`` buildout recipe which gives
you access to the most common configuration options in a buildout way

.. code-block:: ini

    index =
        name:allowedRolesAndUsers   type:string stored:false multivalued:true
        name:created                type:date stored:true
        name:Creator                type:string stored:true
        name:Date                   type:date stored:true
        name:default                type:text indexed:true stored:false multivalued:true
        name:Description            type:text copyfield:default stored:true
        name:description            type:text copyfield:default stored:true
        name:effective              type:date stored:true
        name:exclude_from_nav       type:boolean indexed:false stored:true
        name:expires                type:date stored:true
        name:getIcon                type:string indexed:false stored:true
        name:getId                  type:string indexed:false stored:true
        name:getRemoteUrl           type:string indexed:false stored:true
        name:is_folderish           type:boolean stored:true
        name:Language               type:string stored:true
        name:modified               type:date stored:true
        name:object_provides        type:string stored:false multivalued:true
        name:path_depth             type:integer indexed:true stored:false
        name:path_parents           type:string indexed:true stored:false multivalued:true
        name:path_string            type:string indexed:false stored:true
        name:portal_type            type:string stored:true
        name:review_state           type:string stored:true
        name:SearchableText         type:text copyfield:default stored:false
        name:searchwords            type:string stored:false multivalued:true
        name:showinsearch           type:boolean stored:false
        name:Subject                type:string copyfield:default stored:true multivalued:true
        name:Title                  type:text copyfield:default stored:true
        name:Type                   type:string stored:true
        name:UID                    type:string stored:true required:true

- name: Name of the field
- type: Type of the field (e.g. ``string`` , ``text``, ``date``, ``boolean``)
- indexed: The field is searchable
- stored: The field is returned as metadata
- copyfield: copy content to another field, e.g. copy title, description, subject and SearchableText to default.

For a complete list of schema configuration options refer to `Solr documentation <http://lucene.apache.org/solr/resources.html>`_.

.. seealso:: https://wiki.apache.org/solr/SchemaXml#Common_field_options

This is the bare minimum for configuring Solr. There are more options supported by the buildout
recipe ``collective.recipe.solrinstance`` and even more by Solr itself.
Most notably the custom extensions for *schema.xml* and *solrconfig.xml*.

We will see examples for this later on in the training.

Or you can even point to a custom location for the main configuration files.

.. code-block:: ini

   schema-destination = ${buildout:directory}/etc/schema.xml
   config-destination = ${buildout:directory}/etc/solrconfig.xml

After running the buildout,
which downloads and configures Solr and Plone, we are ready to fire up both servers.

Plone And Solr
==============

To activate Solr in Plone *collective.solr* needs to be activated as an add-on in Plone.

Activating the Solr add-on adds a configuration page to the controlpanel.
It can be accessed via <PORTAL_URL>/@@solr-controlpanel or via "Configuration" -> "Solr Settings"

Check: :guilabel:`Active`, click :guilabel:`Save`

Activating Solr in the controlpanel activates a patch of Plones indexing
and search methods to use Solr for indexing and querying.

.. note::

   Note that ZCatalog is not replaced but Solr is *additionally* used
   for indexing and searching.

Control Panel Configuration
---------------------------

 - *Active* - Turn connection between Plone and Solr on/off.
 - *Host* - The host name of the Solr instance to be used. Defaults to 127.0.0.1
 - *Port* - The port of the Solr instance to be used. Defaults to 8983
 - *Base* - The base prefix of the Solr instance to be used. Defaults to /solr
 - *Asynchronous indexing* - Check to enable asynchronous indexing operations,
   which will improve Zope response times in return for not having the Solr
   index updated immediately.

 - *Automatic commit* - If enabled each index operation will cause a commit to be sent to Solr,
   which causes it to update its index.
   If you disable this, you need to configure commit policies on the Solr server side.

 - *Commit within*

Timeouts And Search Limit
~~~~~~~~~~~~~~~~~~~~~~~~~

 - Index timeout
 - Search timeout
 - Maximum search results

Search Query Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

 - Required query parameters
 - Pattern for simple search queries
 - Default search facets
 - Filter query parameters
 - Slow query threshold
 - Effective date steps
 - Exclude user from allowedRolesAndUsers

Highlighting
~~~~~~~~~~~~

https://wiki.apache.org/solr/HighlightingParameters

 - Highlighting fields
 - Highlight formatter: pre
 - Highlight formatter: post
 - Highlight Fragment Size


 - Default fields to be returned
 - Levensthein distance


Atomic Updates And Boosting
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 - Enable atomic updates
 - Python script for custom index boosting


With Solr activated, searching in Plone works like the following:

 - Search contains one of the fields set as required
   (which is normally the fulltext field *SearchableText*)
   -> Solr results are returned

 - Search does not contain all fields marked as required
   -> ZCatalog results are returned.
   Which is the case for rendering the navigation,
   folder contents, etc.

 - The search contains the stanza *use_solr=True*.
   -> Solr results are returned independent of the required fields.

Then you are ready for your first search.
Search for *Plone*.

You should get the frontpage as a result--which is not super awesome to begin with because we have this without Solr too--but it is the first step in utilizing the full power of Solr.

Configuration With ZCML
-----------------------

Another way to configure the connection is via :term:`ZCML`.
You can use the following snippet to configure host, port und basepath:

.. code-block:: xml

  <configure xmlns:solr="http://namespaces.plone.org/solr">
    <solr:connection host="127.0.0.23" port="3898" base="/foo" />
  </configure>

The ZCML configuration takes precedence over the configuration in the registry / control-panel.

Committing Strategies
=====================

Synchronous Immediately
-----------------------

The default commit strategy is to commit to Solr on every Zope commit.
This ensures an always up to date index but may come at the cost of indexing time especially when doing batch operations like data import.

To use this behavior, turn **Automatic commit** ON in the Solr controlpanel in Plone.

Synchronous Batched
-------------------

Another commit strategy is to do timed commits in Solr.
This method is usually way faster but comes with the downside of index delays.

To use this behavior you have to do two things:

 - Turn **Automatic commit** OFF in the Solr controlpanel in Plone.
 - Set one or both of the following options in the Solr server configuration via the collective.recipe.solrinstance buildout recipe:

   - ``autoCommitMaxDocs`` - The number of updates that have occurred since the last commit.
   - ``autoCommitMaxTime`` - The number of milliseconds since the oldest uncommitted update.

Asynchronous
------------

The third commit strategy is to do full asynchronous commits.
This can be activated by setting the Flag **Asynchronous indexing** in the Solr control panel to :guilabel:`ON`.
This behavior is the most efficient in terms of Zope response time.

Since it is fire and forget the consistency could be harmed in the interim.
It is advisable to do a sync or full-index from time to time if you work with this strategy.

Additional information can be found in the Solr documentation:

.. seealso:: https://lucene.apache.org/solr/guide/6_6/updatehandlers-in-solrconfig.html#UpdateHandlersinSolrConfig-commitWithin

Exercise
========

Have a running Plone and Solr with collective.solr active and experiment with commit strategies.
