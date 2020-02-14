.. _volto_talk_listview-label:

Volto View Components: A Listing View for Talks
===============================================

In this part you will:

* Register a react view component for listings
* Write the component


Topics covered:

* Use search endpoint of REST API
* Displaying data from search results

Volto has different views for listing objects. Most of them list all objects in a folder like the ``listing view``. To show all talks you have in your site you'll have to register and write your own listing view. 

For doing so you have to add another new file ``src/components/Views/TalkListView.jsx`` in the folder :file:`Views` you added in the last chapter.

As a first step the file will hold a placeholder again:

..  code-block:: js

    import React from 'react';

    const TalkListView = props => {
      return <div>I'm the TalkListView component!</div>;
    };
    export default TalkListView;

Then you have to edit the file::index.js to export your new View:

..  code-block:: js
    :emphasize-lines: 1,4

    import TalkListView from './Views/TalkListView';
    import TalkView from './Views/TalkView';

    export { TalkListView, TalkView };

Now register the new component as layout view for folderish types in ``src/config.js``.

..  code-block:: js
    :emphasize-lines: 2,8-11

    import { TalkView } from './components';
    import { TalkListView } from './components';

    [...]

    export const views = {
    ...defaultViews,
    layoutViews: {
        ...defaultViews.layoutViews,
        talkslist_view: TalkListView,
    },
    contentTypesViews: {
        ...defaultViews.contentTypesViews,
        Talk: TalkView,
    },
    };

This extends ``defaultViews.layoutViews`` with the key/value pair ``talkslist_view: TalkListView``.

To add a layout view you also have to add this new view in the ``ZMI`` of your ``Plone``. Login to your instanz by using ``/manage`` and unfold the point Plone in the left sidebar. Now click on ``portal_types`` and search for the ``folder``-Type to add your new ``talklist_view`` to the ``Available view methods`` by adding it to a new line.

.. figure:: _static/add_talklistview_in_zmi.png
	:scale: 50 %
	:alt: Add new View in the ZMI.

	Add new View in the ZMI.

Now we will improve this view step by step.

First we reuse the component ``DefaultView.jsx`` in our custom view:
