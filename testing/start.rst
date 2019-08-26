Package setup
=============

In this chapter we are going to create a new Plone package from scratch and use it to see different testing techniques.

We are going to use also ``plonecli`` tool because it allows to easily create new Plone packages and features (content-types, views, vocabularies) with simple cli commands.

Create Package
--------------

First of all we need to create a virtual Python environment:

.. code-block:: console

  $ virtualenv .env


.. note::

  By default you should use Python3 and its virtualenv because Python2 will be deprecated on 01/01/2020.

Activate virtual Python environment:

.. code-block:: console

  $ source .env/bin/activate

Install plonecli:

.. code-block:: console

  $ pip install plonecli

Create a new addon package:

.. code-block:: console

  $ plonecli create addon src/plonetraining.testing


Buildout
--------

Run buildout:

.. code-block:: console

  $ cd plonetraining.testing
  $ pip install -r requirements.txt
  $ bin/buildout

Run tests:

.. code-block:: console

  $ bin/test

Run all tests including robot tests (we will see later what they are):

.. code-block:: console

  $ bin/test --all
