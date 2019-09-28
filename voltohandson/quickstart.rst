.. _voltohandson-quickstart-label:

============
Quick Start
============

Using the hands on repo
========================

You can find the repository with the code that we will be using during all the training in:

TODO - repo final location

This repo has the final stage of what we will achieve at the end of the
training in the ``master`` branch and there's a branch with the name of each
chapter. In case you get lost at some point, you are able to forward (or
rewind) and get the complete code for the end of each chapter the training
easily.

The repo has an ``api`` folder, where you can find a preconfigured buildout
that will build Plone 5.2 along with the package ``kitconcept.voltodemo`` that
readies a site for the immediate use of Volto.

Build environments
------------------

To build it, you just have to use the convenience ``Makefile`` command:

.. code-block:: console

  $ make build-backend

.. note::
    It assumes the fact that you have ``Python 3`` in your path and all the usual
    system dependencies for building Plone installed in your machine.

.. note::
    If any of you have problems with the traditional build of Plone
    backend, you can use a docker container to run it:

    .. code-block:: console

      $ make start-backend-docker

The repo also has a Volto project ready to build in the root. You should have all the :ref:`Volto dependencies <install-deps-volto-label>` installed in your machine. To build it you should do:

.. code-block:: console

  $ make build-frontend

or just:

.. code-block:: console

    $ yarn

Executing environments
----------------------

Use this command to run Plone:

.. code-block:: console

  $ make start-backend

and this command to run Volto:

.. code-block:: console

  $ yarn start

.. note::
    From now on, it's convenient to open a terminal for each process, and a third one to edit and issue commands.

Volto source code
=================

When developing Volto you'll find yourself quite often with an eye on Volto source code, taking a look on how things are done, syntax, cloning or overriding components.
For convenience a symlink to the Volto copy inside ``node_modules`` is setup in the hands-on repository.
You'll find it under the ``omelette`` folder.

Recommended plugins
===================

No matter what IDE of choice you have, you'll need these plugins:

- Prettier
- ESlint
- prettier-stylelint (VSCode)
