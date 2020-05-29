.. _volto_frontpage-label:

Creating a dynamic frontpage with Volto blocks
==============================================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  This chapter is about the react frontent Volto.

  Solve the same tasks in classic frontend in chapter :doc:`frontpage`

In this part you will:

* Add own criteria for listing block
* Add listing block to show featured content

Topics covered:

* adding own collection criteria
* adding and configuring listing block

Add Index as collection criteria
--------------------------------

To understand why we need a collection criteria for a dynamic frontpage in Volto and what a collection criteria is, we have to look at the listing block of Volto for a brief moment.

.. figure:: _static/volto_frontpage.png
   :alt: Listing Block sidebar

In the sidebar we see the `criteria` selection and if we click there, it'll show some of the choosable criterias ordered in categories like the following:

* `Metadata` contains indexes that are counting as metadata like Type (means Portal Types) and Review State
* `Text` contains indexes that are counting as text-data like Description and Searchable Text
* `Dates` contains indexes which are working with date-data like Effective Date and Creation Date

To get all talks we marked as `featured` we have to get the listing block to recognize our newly created index. This means we have to add our index to the collection criterias, so we can choose it.

To add our new index as a criteria so we can use it in a listing block or a collection, we have to switch to our `backend`. There we have to create a plone.app.registry record for our index. This can be achieved by editing the `registry.xml` in our `profiles` folder:

.. code-block:: xml
    :linenos:
    :emphasize-lines: 3-14

    <?xml version="1.0" encoding="UTF-8"?>
    <registry xmlns:i18n="http://xml.zope.org/namespaces/i18n"
              i18n:domain="plone">
      <records interface="plone.app.querystring.interfaces.IQueryField"
            prefix="plone.app.querystring.field.featured">
        <value key="title">Featured</value>
        <value key="description">A custom featured index</value>
        <value key="enabled">True</value>
        <value key="sortable">False</value>
        <value key="operations">
          <element>plone.app.querystring.operation.boolean.isTrue</element>
          <element>plone.app.querystring.operation.boolean.isFalse</element>
        </value>
        <value key="group" i18n:translate="">Metadata</value>
      </records>
    </registry>

To understand this code-snippet, we have to know the information and tags we are using:

* The title-value refers to the custom index, in our case the featured-index we just created
* the operations-value is used to filter the items for example `isTrue` and `isFalse` for a boolean field like ours
* the group-value defines under which group the entry shows up in the selection widget, what in our case should be metadata

.. note::

   For a full list of all existing QueryField declarations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L245

.. note::

   For a full list of all existing operations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L1

Like explained in the last chapter we can now restart the instance and import the newly added profile by using the `portal_setup` in our ZMI.

Add listing block to show featured content
------------------------------------------

Now we will go back to our frontend and look up localhost:3000 to checkout the volto. To create a new listing_block on the front-page we have to click on edit first an create one new block space there. Now you have to choose the block `Listing` from the menu:

.. figure:: _static/volto_frontpage_1.png
   :alt: Most used blocks in Volto

And you will gain a new block and sidebar looking like this:

.. figure:: _static/volto_frontpage_2.png
   :alt: Most used blocks in Volto

SCREENSHOTS TO ADD LISTING BLOCK