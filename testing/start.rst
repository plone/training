How to test a Plone product
===========================

To better understand how to test a Plone product, the best thing is to create a new Plone package from scratch
and use it to see different testing techniques.

We are going to use `plonecli <https://pypi.org/project/plonecli/>`_ tool heavily because it allows to easily create new Plone package
and features (content-types, views, vocabularies) with simple commands.

Create Package
--------------

First of all we need to install plonecli:

.. code-block:: console

  $ pip install plonecli --user

.. note::

  This command will install plonecli in the global user site-packages according to the official documentation.
  Feel free to install it with your preferred method (virtualenv, pipenv, pyenv) if you want.

.. note::
  If you have already installed plonecli, please update at least bobtemplates.plone to last version (>= 5.0.1) because there are
  some important fixes needed for this training.

Now we can create a new package:

.. code-block:: console

  $ plonecli create addon plonetraining.testing


Buildout
--------

Run buildout:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli build

.. note::

    This command will create a virtualenv, install dependencies and run buildout.


Run tests (plonecli provides some default tests when creating a new package):

.. code-block:: console

  $ plonecli test

Run all tests including robot tests (we will see later what they are):

.. code-block:: console

  $ plonecli test --all
