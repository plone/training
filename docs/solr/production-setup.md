---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Production Setup

## Multi Core

Multi core setup is the default for Solr 5 and above but unfortunately not supported by collective.solr.
You can access a multicore Solr but only the default core,
which can be specified in the `collective.recipe.solrinstance` buildout recipe.

The following options only apply if `collective.recipe.solrinstance:mc` is specified.
They are optional if the normal recipe is being used.
All options defined in the solr-instance section will we inherited to cores.
A core could override a previous defined option.

cores

: A list of identifiers of Buildout configuration sections that correspond to individual Solr core configurations.
  Each identifier specified will have the section it relates to processed according to the given options above to generate Solr configuration files for each core.

  Each identifier specified will result in a Solr `instanceDir` being created and entries for each core placed in Solr's `solr.xml` configuration.

default-core-name

: Optional and deprecated.
  This option controls which core is set as the default for incoming requests that do not specify a core name.
  See <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=120722784>.
  *No longer* used in Solr 5.

An example for a multi-core configuration you can find in the documentation of `collective.recipe.solrinstance`:

```{seealso}
<https://github.com/collective/collective.recipe.solrinstance/blob/master/README.rst#multi-core-solr>
```

## Monitoring

`collective.solr` comes with some predefined [Munin](https://munin-monitoring.org/) configuration.
The values for Munin are collected and exposed via the Java JMX framework.

You will need Munin and the JMX\_ extension.

```{seealso}
<https://github.com/collective/collective.solr/blob/main/docs/usage/monitoring.rst>
```

The Munin config however seems a little outdated.

## Different host setup

One use case in a production setup might be the split between the Plone server runs on and the Solr server(s).
To make this happen you have to consider a couple of things:

> - configure host of Solr in `collective.solr`, it can be done TTW (Through-The-Web), via ZCML or via /etc/hosts
> - make sure the blobstorage directory of Plone is available via a network drive to the Solr host.
>   You need to make sure Solr has read permissions which means it has the *SAME* User ID than the user which runs the Zope server.

## Further reading

Solr is documented in its own [Wiki](https://cwiki.apache.org/confluence/display/solr/).

```{seealso}
https://solr.apache.org/guide/6_6/
```

There are a couple of books available.
