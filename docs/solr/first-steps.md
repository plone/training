---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# First Steps

## Maintenance Task

All the maintenance tasks are accessible through the Solr control panel in Plone since version 6.0 of `collective.solr`.
It is good to know the direct URLs sometimes.

Another goodie of accessing the URLs directly is they support GET parameters to limit and change their behavior.

Let's see some examples:

### Reindex

Reindex all Plone objects found in catalog:

<http://localhost:8080/Plone/@@solr-maintainance/reindex>

The call of this URL finds all contentish objects
(meaning all objects derived from one of the catalog mixin classes)
and (re)indexes them.

There are some parameters you can specify:

> - *batch* (default:1000): Batch size for commit. Data is only sent to Solr on commit.
> - *skip* (default:0): Skip N elements when iterating over all contentish objects.
> - *limit* (default:0): Only index N elements.
> - *ignore_portal_types* (default:None): Blacklist of portal types not to be indexed.
> - *only_portal_types* (default:None): Whiltelist of portal types not to be indexed.
> - *idxs* (default:\[\]): Only these index fields will be updated.

### Cleanup

Remove entries from Solr that don't have a corresponding Zope object or have a different UID than the real object:

<http://localhost:8080/Plone/@@solr-maintainance/cleanup>

The only parameter you can specify is the batch size:

> - *batch* (default:1000): Batch size for commit. Data is only sent to Solr on commit.

### Sync Solr Index

Sync the Solr index with the portal catalog.
Records contained in the catalog but not in Solr will be indexed and records not contained in the catalog will be removed.

<http://localhost:8080/Plone/@@solr-maintainance/sync>

There are some parameters you can specify:

> - *batch* (default:1000): Batch size for commit. Data is only sent to Solr on commit.
> - *preImportDeleteQuery* (default:*:*): This **delete** query will be executed on Solr before the sync process starts.

### Purge Solr Index

Clear **all** elements from the Solr default collection.

<http://localhost:8080/Plone/@@solr-maintainance/clear>

There are no parameters you can specify for the clear action.

```{note}
Be careful with required fields.

If you specify required fields in your schema, which are not present in your indexing record indexing will not happen.
```

## Indexing A New Dexterity Field

A common use case is to add an additional field to the index.
We have to inform both sides (Solr and Plone) if we need a new field in the index.

A simple use case is to pass through a raw dexterity field to the index.
First we add the field to the schema.

We do this {term}`TTW` (Through-The-Web) right now.

```{note}
In the production setup you will define your schema with an interface or a supermodel XML but this is beyond the scope of this training.

More information on dexterity schemas and fields can be found in the Plone documentation:
<https://5.docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html>
```

Let's add a field *email* to a task.
We assume this is contact email which can be used to contact the responsible support person for this task.
And we want this field to be found in fulltext search.

It does not matter if we add the field TTW (Through-The-Web), via supermodel or via interface.
The only thing you have to make sure the **name** of the field is identical in Plone and Solr.

Next thing we do is to extend the Solr fields definition in our buildout.cfg.

On the *fields* section of the *solr* part we add the following line:

```
name:email    type:string copyfield:SearchableText stored:true multivalued:false
name:fullname type:string copyfield:SearchableText stored:true multivalued:false
```

After we have done that we need to rerun buildout

```shell
bin/buildout
```

and restart Solr and Plone

```shell
bin/instance restart
bin/solr-instance fg
```

This method works out of the box,
if the name of the Dexterity field in Plone is the same as the field in the schema of Solr.

And assuming you *have* the information you need for the index available as a Dexterity field.

Let's assume we have a field *fullname* in Solr and in Plone we have separate fields for *firstname* and *surname*.
We need an indexing adapter to have the fullname indexed.
This is done like this:

First we need an indexer binding to our dexterity content

```python
from plone.indexer import indexer
from plonetraining.solr_example.interfaces import ITask

@indexer(ITask)
def fullname_indexer(obj):
    """ Construct a fullname for Solr from Dexterity fields """
    return getattr(obj, 'firstname', '') + ' ' + getattr(obj, 'surname', '')
```

And we need a named adapter, which correlates with the name of the field in Solr (*fullname* in our case)

```python
<adapter factory=".indexer.fullname_indexer" name="fullname" />
```

That's it.
After adding a new Task or reindexing an existing one with firstname and surname set,
the *fullname* in Solr appears.

```{note}
Pro tip:

If you need to modify or extend the existing fulltext implementation in Plone
(this could be adding a custom field to it, or removing title or description from it),
there is a handy add-on for this purpose.

It is well documented but further investigation is out of the scope of this training,
see <https://pypi.org/project/collective.dexteritytextindexer>
```

## Boosting

In a standard installation of Solr all fields are treated as equally important for searching.
Usually this is not what we want.
We want the Title to be more important, or a special type (e.g. News) to be prioritized.

Solr offers boosting values at index and at search time.
The search boosting is utilized automatically when you install collective.solr.
It is configured in the control-panel with the default search pattern:

```
+(Title:{value}^5 OR Description:{value}^2 OR SearchableText:{value} OR
SearchableText:({base_value}) OR searchwords:({base_value})^1000)
```

This reads like this.
If a term occurs in the *Title* field prioritize it 5 times,
if it is in the *Description* field prioritize it two times.

Search but don't prioritize terms occuring in the *SearchableText* index.
If a term occurs in the *searchwords* priotize it by the value 1000 so it will show always at the top.

You can override this pattern to fit your needs.

Another way to boost documents is at indexing time.
For this purpose you can specify a Restricted Python script in Solr control panel.
Let's assume we want to put a special emphasis on News Items.

Our script looks like:

```python
return {'': 20} if data.get('portal_type') == 'News Item' else {}
```

This will boost all fields of *News Items* by factor 20.
Which means *News Items* will be prioritized in the ranking and show as first search results with the same term.

```{note}
Boosting at index time is only available if you turn off atomic updates.
```

## Exercise

> 1. Create or enhance a Dexterity type with an additional field which is indexed.
> 2. Create a custom indexer in Plone.
