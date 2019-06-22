Package setup
=============


Create Package
--------------

Create virtual Python environment:

.. code-block:: console

  $ virtualenv-2.7 .env

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

Run all tests including robot tests:

.. code-block:: console

  $ bin/test --all
