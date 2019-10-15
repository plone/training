.. _voltohandson-editblocks-label:

========================
Blocks - Edit components
========================

The edit component part of a block anatomy is specially different to the view component because they have to support the UX for editing the block.
This UX can be very complex depending on the kind of block and the feature that it is trying to provide.
The project requirements will tell how far you should go with the UX story of each tile, and how complex it will become.
You can use all the props that the edit component is receiving to model the UX for the block and how it will render.

See the complete list :ref:`voltohandson-introtoblocks-editprops-label`.

We have several UI/UX artifacts in order to model our block edit component UX.
The sidebar and the object browser are the main ones.

Sidebar
=======

We can use the new sidebar when building our blocks' edit components.
It's a new resource that is available in Volto 4.
You need to instantiate it this way:

.. code-block:: jsx

    import { SidebarPortal } from '@plone/volto/components';

    ...

    <SidebarPortal selected={this.props.selected}>
      ...
    </SidebarPortal>

Everything that's inside the ``SidebarPortal`` component will be rendered in the sidebar.

Object Browser
==============

Volto has an object browser component that allows you to select an existing content object from the site.
It has the form of an HOC (High Order Component), and you have to wrap the component you want to be able to call the object browser from, like this:

.. code-block:: jsx

    import withObjectBrowser from '@plone/volto/components/manage/Sidebar/ObjectBrowser';

    ...

    export default withObjectBrowser(MyComponent)

The HOC component ``withObjectBrowser`` wraps your component by making available this props:

  - isObjectBrowserOpen - (Bool) tells if the browser is currently open
  - openObjectBrowser - handler for opening the browser
  - closeObjectBrowser - handler for closing the browser

Teaser block
============

Let's create a new block (not in the project) but can be handy too.
Create a new block called Teaser.
We will add the ability to select an existing object as source for showing in this block.

Follow the previous chapters to create a new basic block.

Teaser block edit component
---------------------------

We will start this time with the `Edit.jsx` component. We'll be creating two children components:

`src/components/Blocks/Teaser/Edit.jsx`

.. code-block:: jsx

    import React from 'react';
    import { SidebarPortal } from '@plone/volto/components';
    import TeaserSidebar from './TeaserSidebar';
    import TeaserBody from './TeaserBody';

    const Edit = ({ data, onChangeTile, tile, selected, properties }) => {
      return (
        <>
          <TeaserBody data={data} properties={properties} id={tile} isEditMode />
          <SidebarPortal selected={selected}>
            <TeaserSidebar data={data} tile={tile} onChangeTile={onChangeTile} />
          </SidebarPortal>
        </>
      );
    };

    export default Edit;

`src/components/Blocks/Teaser/TeaserSidebar.jsx`

.. code-block:: jsx

    import React from 'react';
    import { Segment } from 'semantic-ui-react';
    import { FormattedMessage } from 'react-intl';

    import TeaserData from './TeaserData';

    const TeaserSidebar = props => {
      return (
        <Segment.Group raised>
          <header className="header pulled">
            <h2>
              <FormattedMessage id="Teaser" defaultMessage="Teaser" />
            </h2>
          </header>

          <TeaserData {...props} />
        </Segment.Group>
      );
    };

    export default TeaserSidebar;

`src/components/Blocks/Teaser/TeaserData.jsx`

.. code-block:: jsx

    import React from 'react';
    import PropTypes from 'prop-types';
    import { Segment } from 'semantic-ui-react';
    import { defineMessages, injectIntl } from 'react-intl';
    import { CheckboxWidget, TextWidget } from '@plone/volto/components';
    import { compose } from 'redux';
    import withObjectBrowser from '@plone/volto/components/manage/Sidebar/ObjectBrowser';

    import clearSVG from '@plone/volto/icons/clear.svg';
    import navTreeSVG from '@plone/volto/icons/nav.svg';

    const messages = defineMessages({
      Source: {
        id: 'Source',
        defaultMessage: 'Source',
      },
      openLinkInNewTab: {
        id: 'Open in a new tab',
        defaultMessage: 'Open in a new tab',
      },
    });

    const TeaserData = ({
      data,
      tile,
      onChangeTile,
      openObjectBrowser,
      required = false,
      intl,
    }) => {
      return (
        <>
          <Segment className="form sidebar-image-data">
            <TextWidget
              id="source"
              title={intl.formatMessage(messages.Source)}
              required={false}
              value={data.href}
              icon={data.href ? clearSVG : navTreeSVG}
              iconAction={
                data.href
                  ? () => {
                      onChangeTile(tile, {
                        ...data,
                        href: '',
                      });
                    }
                  : () => openObjectBrowser('link')
              }
              onChange={(name, value) => {
                onChangeTile(tile, {
                  ...data,
                  href: value,
                });
              }}
            />
            <CheckboxWidget
              id="openLinkInNewTab"
              title={intl.formatMessage(messages.openLinkInNewTab)}
              value={data.openLinkInNewTab ? data.openLinkInNewTab : false}
              onChange={(name, value) => {
                onChangeTile(tile, {
                  ...data,
                  openLinkInNewTab: value,
                });
              }}
            />
          </Segment>
        </>
      );
    };

    TeaserData.propTypes = {
      data: PropTypes.objectOf(PropTypes.any).isRequired,
      tile: PropTypes.string.isRequired,
      onChangeTile: PropTypes.func.isRequired,
      openObjectBrowser: PropTypes.func.isRequired,
    };

    export default compose(
      withObjectBrowser,
      injectIntl,
    )(TeaserData);

`src/components/Blocks/Teaser/TeaserBody.jsx`

.. code-block:: jsx

    import React from 'react';
    import PropTypes from 'prop-types';
    import { Link } from 'react-router-dom';
    import { useDispatch, useSelector } from 'react-redux';
    import { Message } from 'semantic-ui-react';
    import { defineMessages, injectIntl } from 'react-intl';
    import imageTileSVG from '@plone/volto/components/manage/Tiles/Image/tile-image.svg';
    import { getContent } from '@plone/volto/actions';
    import { flattenToAppURL } from '@plone/volto/helpers';

    const messages = defineMessages({
      PleaseChooseContent: {
        id: 'Please choose an existing content as source for this element',
        defaultMessage:
          'Please choose an existing content as source for this element',
      },
    });

    const TeaserBody = ({ data, id, isEditMode, intl }) => {
      const contentSubrequests = useSelector(state => state.content.subrequests);
      const dispatch = useDispatch();
      const results = contentSubrequests?.[id]?.data;

      React.useEffect(() => {
        if (data.href) {
          dispatch(getContent(data.href, null, id));
        }
      }, [dispatch, data, id]);

      return (
        <>
          {!data.href && (
            <Message>
              <div className="teaser-item default">
                <img src={imageTileSVG} alt="" />
                <p>{intl.formatMessage(messages.PleaseChooseContent)}</p>
              </div>
            </Message>
          )}
          {data.href && results && (
            <div className="teaser-item">
              {(() => {
                const item = (
                  <>
                    {results.image && <img src={results.image.download} alt="" />}
                    <h3>{results.title}</h3>
                    <p>{results.description}</p>
                  </>
                );
                if (!isEditMode) {
                  return (
                    <Link
                      to={flattenToAppURL(results['@id'])}
                      target={data.openLinkInNewTab ? '_blank' : null}
                    >
                      {item}
                    </Link>
                  );
                } else {
                  return item;
                }
              })()}
            </div>
          )}
        </>
      );
    };

    TeaserBody.propTypes = {
      data: PropTypes.objectOf(PropTypes.any).isRequired,
      isEditMode: PropTypes.bool,
    };

    export default injectIntl(TeaserBody);

`src/components/Blocks/Teaser/View.jsx`

.. code-block:: jsx

    import React from 'react';
    import TeaserBody from './TeaserBody';

    const View = props => {
      return <TeaserBody {...props} />;
    };

    export default View;

``src/config.js``

.. code-block:: js

    import TeaserViewBlock from '@package/components/Blocks/Teaser/View';
    import TeaserEditBlock from '@package/components/Blocks/Teaser/Edit';

    const customTiles = {
    ...
      teaser: {
        id: 'teaser',
        title: 'Teaser',
        icon: sliderSVG,
        group: 'common',
        view: TeaserViewBlock,
        edit: TeaserEditBlock,
        restricted: false,
        mostUsed: true,
        security: {
          addPermission: [],
          view: [],
        },
      },

and finally the styling:

.. code-block:: less

    .teaser-item {
      display: flex;
      flex-direction: column;
      margin-bottom: 20px;

      img {
        width: 100%;
        margin-bottom: 20px;
      }

      a {
        color: @textColor;
      }

      h3 {
        margin: 0 0 20px 0;
      }
    }
