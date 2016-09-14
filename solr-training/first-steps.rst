First Steps
=====================

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
