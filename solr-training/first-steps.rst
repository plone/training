First Steps
=====================

Maintenacne Tasks
-----------------

All the maintenance tasks are accessible through the
Solr controlpanel in Plone since version 6.0 of
collective.solr. Nevertheless it is good to know
the direct URLs sometimes.
Another goodie of accessing the URLs directly is
they support GET parameters to limit and change
their behavior. Let's see some examples:

Reindex all Plone objects found in catalog:

        """ find all contentish objects (meaning all objects derived from one
            of the catalog mixin classes) and (re)indexes them """


http://localhost:8080/Plone/@@solr-maintainance/reindex

batch=1000, skip=0, limit=0, ignore_portal_types=None,
                only_portal_types=None, idxs=[]):


Cleanup

remove entries from solr that don't have a corresponding Zope
            object or have a different UID than the real object


http://localhost:8080/Plone/@@solr-maintainance/cleanup

batch=1000

Sync Solr Index

        """Sync the Solr index with the portal catalog. Records contained
        in the catalog but not in Solr will be indexed and records not
        contained in the catalog will be removed.
        """


http://localhost:8080/Plone/@@solr-maintainance/sync

batch=1000, preImportDeleteQuery='*:*'

Purge Solr index

http://localhost:8080/Plone/@@solr-maintainance/clear


.. note:: Be careful with required fields. If you specify
   required fields in your schema, which are not present
   in your indexing record indexing will not happen.

Indexing a new dexterity field
------------------------------

A common use case is to add an aditional field to the index.
We have two inform both sides (Solr and Plone) if we
need a new field in the index.

A simple use case is to pass through a raw dexterity field
to the index. First we add the field to the schema.
We do this TTW right now.

.. note:: In the production setup you will define your schema
   with an interface or a supermodel XML but this is beyond of
   this training. More information on dexterity schemas and
   fields can be found in the Plone documention:
   http://docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html

Let's add a field *email* to a task. We assume this is contact
email which can be used to contact the reponsible support person
for this task. And we want to make this field to be found in
fulltext search.

TBD Steps to add field
TBD Store schema.xml?
TBD Screenshot adding field to schema

Next thing we do is to extend the Solr fields definition in
our buildout.cfg

to the *fields* section of the *solr* part we add the
following line: ::

 name:email    type:string copyfield:default stored:true multivalued:false
 name:fullname type:string copyfield:default stored:true multivalued:false

After we have done that we need to rerun the buildout ::

 $ bin/buildout

and restart Solr and Plone ::

 $ bin/instance restart
 $ bin/solr-instance fg

This method works out of the box, if the name of the Dexterity field in Plone
is the same as the field in the schema of Solr. And asuming you *have* the
information you need for the index available as a Dexterity field.

Let's assume we have a field *fullname* in Solr and in Plone we have separate
fields for *firstname* and *sirname*. We need an indexing adapter to have
the fullname indexed. This is done like this:

First we need an indexer binding to our DX content: ::

  from plone.indexer import indexer
  from plonetraining.solr_example.interfaces import ITask

  @indexer(ITask)
  def fullname_indexer(obj):
      """ Construct a fullname for Solr from Dexterity fields """
      return getattr(obj, 'firstname', '') + ' ' + getattr(obj, 'sirname', '')


And we need a named adapter, which corelates with the name of the field
in Solr (*fullname* in our case). ::

  <adapter factory=".indexer.fullname_indexer" name="fullname" />

That's it. After adding a new Task or reindexing an existing one with first-
and sirname set, the *fullname* in Solr appears.


.. note:: Pro tip: If you need to modify or extend the existing
   fulltext implementation in Plone (This could be adding a
   custom field to it, or remove title or dexription from it),
   there is a handy addon for this purpose. It is well documentend
   but further investigation is out of the scope of this training
   See https://pypi.python.org/pypi/collective.dexteritytextindexer

Boosting
--------

In a standard installation of Solr all fields are treated equaly important
for searching. Usually this is not what we want. We want the Title to be
more important, or a special type (e.g. News) to be prioritized.
Solr offers boosting values at index and at search time.
The search boosting is utilized automatically when you install
collective.solr. It is configured in the control-panel with the default
search pattern: ::

  +(Title:{value}^5 OR Description:{value}^2 OR SearchableText:{value} OR
  SearchableText:({base_value}) OR searchwords:({base_value})^1000)

This reads like this. If a term occurs in the *Title*-field priortize it
5 times, if it is in the *Description*-field priotize it two times.
Search but don't priotize terms occuring in the *SearchableText* index.
If a term occurs in the *searchwords* priotize it by value 1000 so it
always be on top.

You can override this pattern to fit your needs.

Another way to boost documents is at indexing time. For this purpose
you can specify a Restricted Python script in the control panel
of Solr. Let's assume we want to put a special emphasis on News Items.
Our script looks as follows: ::

   return {'': 20} if data.get('portal_type') == 'News Item' else {}

This will boost all fields of  *News Items* by factor 20. Which means
*News Items* will be prioritized in the ranking and show as first
search results with the same term. 

.. note:: Boosting at index time is only available if you turn off
   atomic updates.

