.. _volto_addon-label:

Using Volto add-ons
=====================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  This chapter is about the React frontend Volto.

  For Plone add-ons see chapter :ref:`add-ons-label`


.. _add-ons-volto-overview-label:

Volto Add-ons
-------------

Add-ons enrich a Volto app with specialized blocks, themes, integration of Node packages, and more.
A selection of add-ons can be found on:

-   Github: https://github.com/collective/awesome-volto#addons
-   npm: https://www.npmjs.com/search?q=keywords:volto-addon

One typical add-on is about adding a new block to present content in columns: `@eeacms/volto-columns-block <https://github.com/eea/volto-columns-block>`_

.. figure:: _static/volto-columns-block.png
    :alt: The eea volto-columns-block package gives you a block with columns. Each column is its own separate blocks container.

Here is how you would install a Volto add-on:

Update ``package.json``:

..  code-block:: bash

    "addons": [
      "@eeacms/volto-columns-block"
    ],

    "dependencies": {
      "@plone/volto": "12.3.0",
      "@eeacms/volto-columns-block": "github:eea/volto-columns-block#x.y.z"
    },

Add-ons that are already released on npm https://www.npmjs.com:

..  code-block:: bash
    :linenos:
    :emphasize-lines: 8-9

    "addons": [
      "@eeacms/volto-columns-block"
    ],

    "dependencies": {
      "@plone/volto": "8.3.0",
      "@eeacms/volto-columns-block": "^1.0.0"
    },


Install new add-ons and restart Volto:

..  code-block:: bash

    $ yarn
    $ yarn start


.. _add-ons-volto-backedupbyplone-label:

Complementing Volto with Plone add-ons
--------------------------------------

With some additional features of Volto add-ons in place, where do we need to work on the Plone side? With the split of Plone in backend and frontend, Plone is still the place to shape your data model. For our training story 'Platform for a Plone Conference' we need to model the content type talk. So in an earlier :doc:`dexterity` chapter we created a **new Plone add-on** ``ploneconf.site`` that adds the content type ``talk`` and the correspondent views for a talk and a list of talks in our Volto app ``volto-ploneconf`` in chapter :doc:`volto_talkview`.
