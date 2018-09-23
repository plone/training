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

   gatsby new hello-world https://github.com/gatsbyjs/gatsby-starter-hello-world

This command creates a new Gatsby project with name `hello-world` with the starter boilerplate named `gatsby-starter-hello-world`.

.. code-block:: console

   cd hello-world
   gatsby develop

This command starts a development server.
You will be able to see and interact with your new site in a development environment at http://localhost:8000.
