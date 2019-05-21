======================
Advanced Pipeline Tips
======================

One of the most difficult things about Transmogrifier is being aware of everything that is possible in the pipeline.
There is a lot of manipulation that can be done in the pipleline,
but it means you have to know what blueprints are available, and how to use them all.
When starting out, you may find yourself writing a lot more blueprints than is really necessary.
As you learn more about what is possible with the pipeline,
you may end up writing less custom code.

In this section, we'll cover some advanced tips of what is possible in the pipeline.


Multiple pipelines
------------------

If you know you will run an import multiple times,
there are steps that will only need to be run the first time.
Any import run after that can use less steps.
Additional pipelines can still point to your same custom blueprints file.

The pipelines will need to be set up as separate profiles.


Dates Updater
-------------

plone.app.transmogrifier.datesupdater

.. code-block:: console

   [datesupdate]
   blueprint = plone.app.transmogrifier.datesupdater
   modification-key = modified
   effective-key = show_date
   expiration-key = hide_date


Conditions
----------

https://docs.plone.org/external/collective.transmogrifier/docs/source/sections.html
Add a condition section that does the same thing as the blueprint we created that excludes older items.


Changing Types
--------------

.. code-block:: console

   [map-types]
   blueprint = collective.transmogrifier.sections.inserter
   key = string:_type
   value = python:{
       'HTML Document': 'Document',
       'Event Manager': 'Folder',
       'Folder (Ordered)': 'Folder',
       }.get(item['_type'], item['_type'])


Others
------

.. code-block:: console

   [doctext]
   blueprint = collective.transmogrifier.sections.manipulator
   keys =
       document_src
   destination = string:text
   
   [history-item-path]
   blueprint = collective.transmogrifier.sections.inserter
   key = string:_path
   condition = python:item['_type'] == 'coe_history_item'
   value = python:item['_path'].replace('/Images', '')

Next: `Advanced Blueprint <advanced-blueprint>`
