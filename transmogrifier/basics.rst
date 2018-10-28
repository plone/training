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

With mr.bob and bobtemplates.plone, you can easily set up a package for handling migrations.

    $ pip install bobtemplates.plone
    $ mrbob -O ploneconf.migration bobtemplates.plone:migration_package

This command will ask a few questions about the author (you),
and what version of Plone to use.
Check plone.org for the latest version.

The created package can be used as an add-on in an existing buildout,
or as a buildout on its own.
For this training, we'll use it on its own.
Follow the instructions below to get a sample Plone site running.
You can use Python 3 if you are creating a Plone 5.2+ instance.

    $ cd ploneconf.migration
    $ virtualenv env --python=python2.7
    $ env/bin/pip install zc.buildout
    $ env/bin/buildout
    $ bin/instance fg

This will start up the instance for you, and will be accessible in your browser at http://localhost:8080.
Click the 'Create a new Plone site' button, and create a site with the id `Plone`.