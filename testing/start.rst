How to test a Plone product
===========================

To better understand how to test a Plone product, the best thing is to create a new Plone package from scratch
and use it to see different testing techniques.

We are going to use `plonecli <https://pypi.org/project/plonecli/>`_ tool heavily because it allows to easily create new Plone package
and features (content-types, views, vocabularies) with simple commands.

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

Create a new addon package where you want:

.. code-block:: console

  $ plonecli create addon plonetraining.testing


Buildout
--------

Run buildout:

.. code-block:: console

  $ cd plonetraining.testing
  $ pip install -r requirements.txt
  $ bin/buildout

Run tests (plonecli provides some default tests when creating a new package):

.. code-block:: console

  $ bin/test

Run all tests including robot tests (we will see later what they are):

.. code-block:: console

  $ bin/test --all
