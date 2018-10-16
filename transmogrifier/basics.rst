=====================
Transmogrifier Basics
=====================

In this section you will:

* Learn the basic pipeline setup
* Install the necessary add-ons
* Create a migration package

Transmogrifier Setup and Terminology
------------------------------------

* pipeline, blueprint, etc
* Archetypes vs Dexterity
* The most important piece of the export is the `path`.
* Graph of the process, looping through items in the pipeline


Add-ons
-------

Note that if you follow the next step to create a migration package with mr.bob, these will be automatically installed

* collective.jsonmigrator (when migrating from json)
* transmogrify.dexterity
* collective.transmogrifier is a dependency of transmogrify.dexterity


Create a Migration Package
--------------------------

* install mr.bob
* run the command to create a migration package

.. todo::

    add a migration package to mr.bob, call it mysite.migration