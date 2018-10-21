Installing The Development Environment
======================================

First, we need last LTS NodeJS version (8.12.0 at writing time).
We recommend to use nvm to install NodeJS instead of using your OS-based version.

Install nvm on your system using the instructions and provided script at:

https://github.com/creationix/nvm#install-script

Using nvm we will look up the latest lts version of NodeJS and install it

.. code-block:: console

   nvm install --lts
   nvm use --lts

NodeJS is provided with npm, its package manager, we will use it to install the GatsbyJS CLI

.. code-block:: console

   npm install --global gatsby-cli

.. note:: ``-g`` means the CLI will be available globally in our nvm instance.

Creating a new Gatsby site
==========================

The CLI allows to initialize a project:

.. code-block:: console

   gatsby new hello-world

This command says gatsby-cli to create a new Gatsby project with name `hello-world` with a basic default file structure.
There are several boilerplates created by the community that allows to easily bootstrap an application for different use-cases.

These boilerplates are called "starters" and in the `offical site <https://www.gatsbyjs.org/docs/gatsby-starters/>`_ you could
find a complete list of available starters. There are starters with some themes already configured (for example material-ui or bootstrap),
others with the support for authentication or for some CMS integration. There are also source-plugin specific starters which
specifically implement and use a recommended configuration for the source-plugin, allowing users to use it to kickstart
GatsbyJS sites with that plugin or use it as reference.

.. note:: To create a new project with a starter, you need to append the github url of the desired starter in the cli command: ``gatsby new [SITE_DIRECTORY] [URL_OF_STARTER_GITHUB_REPO]``


.. code-block:: console

   cd hello-world
   gatsby develop

This command starts a development server.
You will be able to see and interact with your new site in a development environment at http://localhost:8000.
