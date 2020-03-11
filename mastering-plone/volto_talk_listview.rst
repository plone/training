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

Then you have to edit the :file:`index.js` to export your new View:

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
First we reuse the component ``DefaultView.jsx`` in our custom view again:

..  code-block:: js
    :emphasize-lines: 2,5

    import React from 'react';
    import { DefaultView } from '@plone/volto/components';

    const TalkListView = props => {
      return <DefaultView {...props} />;
    };
    export default TalkListView;

.. note::

    For the next part you should have some talks and no other content in one folder to work on the progressing view.

For displaying the title and the description of the folder you will have to work with the ``content``. To use it, you have to assign it in the first step. Afterwards you cat use it to display every information the ``content`` holds like ``title`` and ``description``.

..  code-block:: js
    :emphasize-lines: 2-3,6-18

    import React from 'react';
    import { Container, Segment, Label, Image } from 'semantic-ui-react';
    import { Helmet } from '@plone/volto/helpers';

    const TalkListView = props => {
        const { content } = props;
        return (
            <Container className="view-wrapper">
            <Helmet title={content.title} />
            <article id="content">
                <header>
                <h1 className="documentFirstHeading">{content.title}</h1>
                {content.description && (
                    <p className="documentDescription">{content.description}</p>
                )}
                </header>
            </Container>
        )
    };
    export default TalkListView;

You can also iterate over all item hold by the content by using the map ``content.items``.

.. code-block:: js
    :emphasize-lines: 2-3,6-18

    import React from 'react';
    import { Container, Segment, Label, Image } from 'semantic-ui-react';
    import { Helmet } from '@plone/volto/helpers';

    const TalkListView = props => {
        const { content } = props;
        return (
            <Container className="view-wrapper">
            <Helmet title={content.title} />
            <article id="content">
                <header>
                <h1 className="documentFirstHeading">{content.title}</h1>
                {content.description && (
                    <p className="documentDescription">{content.description}</p>
                )}
                </header>
                <section id="content-core">
                    {results &&
                        results.map(item => (
                        <Segment padded>
                            <h2>
                            <Link to={item['@id']} title={item['@type']}>
                                {item.type_of_talk.title}: {item.title}
                            </Link>
                            </h2>
                            {item.audience.map(item => {
                            let audience = item.title;
                            let color = color_mapping[audience] || 'green';
                            return (
                                <Label key={audience} color={color}>
                                {audience}
                                </Label>
                            );
                            })}
                            {item.image && (
                            <Image
                                src={flattenToAppURL(item.image.scales.preview.download)}
                                size="small"
                                floated="right"
                                alt={content.image_caption}
                                avatar
                            />
                            )}
                            {item.description && <div>{item.description}</div>}
                            <Link to={item['@id']} title={item['@type']}>
                            read more ...
                            </Link>
                        </Segment>
                    ))}
                </section>
            </article>
            </Container>
        )
    };
    export default TalkListView;

* Explain overview with content items

* build bridge why search is needed
* Explain Search

To get all talks you added to your site, you'll have to implement a search for your 

Whole View:

.. code-block:: js

    import React from 'react';
    import { searchContent } from '@plone/volto/actions';
    import { Container, Segment, Label, Image } from 'semantic-ui-react';
    import { Helmet } from '@plone/volto/helpers';
    import { useDispatch, useSelector } from 'react-redux';
    import { Link } from 'react-router-dom';
    import { flattenToAppURL } from '@plone/volto/helpers';

    const TalkListView = props => {
    const { content } = props;
    const searchRequests = useSelector(state => state.search);
    const dispatch = useDispatch();
    const results = searchRequests.items;

    const color_mapping = {
        Beginner: 'green',
        Advanced: 'yellow',
        Professionals: 'red',
    };

    React.useEffect(() => {
        dispatch(
        searchContent('/', {
            portal_type: ['Talk'],
            fullobjects: true,
        }),
        );
    }, [dispatch]);

    return (
        <Container className="view-wrapper">
        <Helmet title={content.title} />
        <article id="content">
            <header>
            <h1 className="documentFirstHeading">{content.title}</h1>
            {content.description && (
                <p className="documentDescription">{content.description}</p>
            )}
            </header>
            <section id="content-core">
            {results &&
                results.map(item => (
                <Segment padded>
                    <h2>
                    <Link to={item['@id']} title={item['@type']}>
                        {item.type_of_talk.title}: {item.title}
                    </Link>
                    </h2>
                    {item.audience.map(item => {
                    let audience = item.title;
                    let color = color_mapping[audience] || 'green';
                    return (
                        <Label key={audience} color={color}>
                        {audience}
                        </Label>
                    );
                    })}
                    {item.image && (
                    <Image
                        src={flattenToAppURL(item.image.scales.preview.download)}
                        size="small"
                        floated="right"
                        alt={content.image_caption}
                        avatar
                    />
                    )}
                    {item.description && <div>{item.description}</div>}
                    <Link to={item['@id']} title={item['@type']}>
                    read more ...
                    </Link>
                </Segment>
                ))}
            </section>
        </article>
        </Container>
    );
    };

    export default TalkListView;