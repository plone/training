.. _volto_addon-label:

Using Volto add-ons
=====================


.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about the react frontend Volto.


  For Plone add-ons see chapter :ref:`add-ons-label`


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout


.. _add-ons-volto-overview-label:

Volto Add-ons
-------------

| A selection of add-ons can be found on: 
| https://github.com/collective/awesome-volto#addons    

| One typical add-on is about adding a new block to present content in columns:
| https://github.com/eea/volto-columns-block

.. figure:: _static/volto-columns-block.png
    :alt: The eea volto-columns-block package gives you a block with columns. Each column is its own separate blocks container.

Here is how you would install a Volto add-on:

Update `package.json`:

..  code-block:: bash

    "addons": [
      "@eeacms/volto-blocks-form",
      "@eeacms/volto-columns-block"
    ],

    "dependencies": {
      "@plone/volto": "8.3.0",
      "@eeacms/volto-blocks-form": "github:eea/volto-blocks-form#0.5.0",
      "@eeacms/volto-columns-block": "github:eea/volto-columns-block#0.3.2"
    },

Install new add-ons and restart Volto:

..  code-block:: bash

    $ yarn
    $ yarn start


.. _add-ons-volto-backedupbyplone-label

Complementing Volto with Plone add-ons
--------------------------------------

With some additional features of Volto add-ons in place, where do we need to work on the Plone side? With the split of Plone in backend and frontend, Plone is still the place to shape your data model. For our training story 'Platform for a Plone Conference' we need to model the content types talk and speaker. 

So in the next chapters we will create a **new add-on** that adds the content types talk and speaker. We will also **use an existing add-on** that provides us with the logic to handle votes on talks.
