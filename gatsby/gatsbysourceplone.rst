gatsby-source-plone
===================

With the previous sections on source nodes, retrieving data from ``plone.restapi`` and finally using the search traversal method, we have understood how our source-plugin works at base level.

Cheers! That was amazing work.

We have already built this plugin with additional helpful features and functionality to handle all kinds of data, caching and so on in an optimal manner.

So let us try out the `gatsby-source-plone <https://github.com/collective/gatsby-source-plone/>`_ plugin with our `gatsby-starter-plone <https://github.com/collective/gatsby-starter-plone/>`_ to instantly kickstart GatsbyJS development with Plone.

With the GatsbyJS CLI installed, starting up is as simple as:

.. code-block:: console

  gatsby new gatsby-plone-training https://github.com/collective/gatsby-starter-plone
  

This is will setup a GatsbyJS project in the gatsby-plone-training folder with gatsby-source-plone setup already along with a couple of useful extra features.

To see the starter along with the plugin in action, just run these and navigate to ``localhost:8000``.

.. code-block:: console
  cd gatsby-plone-training
  gatsby develop

Yes! simple as that we have a GatsbyJS site sourced from a Plone site up and running.


Configuration
-------------

All of the settings for the gatsby-source-plone plugin is in the ``gatsby-node.js``:

.. code-block:: javascript

  {
    resolve: 'gatsby-source-plone',
    options: {
      baseUrl: 'https://plonedemo.kitconcept.com/en',
      logLevel: 'DEBUG',
    },
  },


**baseUrl** is the Plone site from which data is to be sourced from.
It can be a Plone site root or a Plone folder to be used as root.

**logLevel** decides what levels of logging is displayed as the plugin is run.
The multiple levels include: ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG`` in order of priority of logged messages.

**searchParams** although not used in the example, is worth noting. 
It is used to limit by retrieved content objects by a search parameter.
This allows users to use and display only filtered content in the generated static site.
For examples and more detailed explanation refer the `docs <https://collective.github.io/gatsby-source-plone/reference/search_parameters/>`_.

**token** is the ``JWT`` (JSON Web Token) for ``plone.restapi``.
This is used in some Plone sites that require authentication to query data.
For configuring authentication with ``JWT`` and `dotenv <https://github.com/motdotla/dotenv>`_, read the full `documentation <https://collective.github.io/gatsby-source-plone/reference/authentication/>`_ for a step by step reference.



