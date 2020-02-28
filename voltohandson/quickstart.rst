.. _voltohandson-quickstart-label:

============
Quick Start
============

Using the hands on code repository
==================================

You can find the repository with the code that we will be using during the training in:

https://github.com/collective/volto-hands-on-training

This repo has the starting stage of the training in the ``master`` branch.

Get it like this::

    $ git clone https://github.com/collective/volto-hands-on-training
    $ cd volto-hands-on-training

There's a branch with the name of each chapter.
In case you get lost at any point, you can easily fast forward (or rewind) to get the complete code for each chapter.
You can also start fresh for each new chapter.

The repo has an ``api`` folder, where you can find a preconfigured buildout that will build Plone 5.2 along with the package ``kitconcept.voltodemo``.
Building it is an easy way to get a Volto site running.


Build environments
==================

We need to build two environments.
Start two terminal sessions, one for each environment, Plone and Yarn, and a third session to issue Git and other shell commands.
In each terminal session you should be in the folder ``volto-hands-on-training``.


Plone environment
-----------------

To build your Volto site, use the ``make`` command:

.. code-block:: console

    $ make build-backend

.. note::
    It assumes that you have ``Python 3`` in your path, and that you have all the necessary system dependencies for building Plone already installed on your machine.

.. note::
    If you have problems building the Plone backend, use a Docker container to run it instead:

    .. code-block:: console

        $ make start-backend-docker

Install Volto dependencies
--------------------------

Install the :ref:`Volto dependencies <install-deps-volto-label>` on your machine.

Then use ``nvm`` to ensure you are using the required ``node`` version:

.. code-block:: console

    $ nvm use 10.15.1


Yarn environment
----------------

The repo also has a Volto project ready to build in the root.

To build the yarn environment, you can either use:

.. code-block:: console

    $ make build-frontend

or:

.. code-block:: console

    $ yarn


Executing environments
----------------------

In your Plone environment, use this command to run Plone:

.. code-block:: console

    $ make start-backend

Once Plone is listening on port 8080, use this command to run Volto in your yarn environment in another terminal or shell:

.. code-block:: console

    $ yarn start

Volto source code
=================

When developing Volto you will find yourself looking quite often at the Volto source code to see how things are done, the code syntax, and how to clone or override components.
For convenience, a symlink to a copy of the Volto code is set up inside ``node_modules`` when you run ``yarn`` in the hands-on repository.
You will find this copy of Volto in the ``omelette`` folder.

Recommended plugins
===================

No matter which integrated development environment (IDE) you use, you should also install these plugins:

- Prettier
- ESlint
- prettier-stylelint (for VSCode)
