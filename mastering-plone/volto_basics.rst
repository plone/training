.. _volto_basics-label:

Volto Basics
============

Volto is a React-based frontend for Plone. It is the default frontend since Plone 6.

Here are some things you should know if you are new to Plone 6 or Volto:

* Volto uses `plone.restapi <https://github.com/plone/plone.restapi/>`_ to communicate with Plone.
* Volto will only work of ``plone.restapi`` is installed in your Plone site. In Plone 6 this should be the case by default.
* ``yarn`` is used to build Volto
* Volto currently needs to be installed separately. See chapter :ref:`instructions-install_frontend-label` for instructions.
* Volto runs in a different process than the Plone-backend. By default Volto runs on port 3000. If you start Volto with ``yarn start`` you can see the frontend on http://localhost:3000. The Plone backend runs on http://localhost:8080
* To create a new Plone site you need to use the backend, this is not possible in Volto.
* All changes you make in Volto are visible in Plone and vice versa.
* Volto uses the components from `Semantic UI React <https://react.semantic-ui.com/>`_ to compose most of the views. For example the component `Image <https://react.semantic-ui.com/elements/image/>`_ is used to render images.
* Volto is highly extendable and and customizable with a technology similar to ``z3c.jbot`` that uses component shadowing.
* Volto uses node.js and razzle to render the first request on the server (e.g. for SEO-purposes)
* Volto uses `Redux <https://redux.js.org/>`_ and `React Router <https://reacttraining.com/react-router/web/guides/quick-start>`_ to ...
* Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks.
* When you use the Pastanaga Editor the data you add in blocks and the arrangement of the blocks is stored as json in the schema-fields ``blocks`` and ``blocks_layout`` provided by the dexterity-behavior ``volto.blocks``. The blocks are is not displayed in the backend.
* If you do not use the behavior ``volto.blocks`` the fields from a content-type schema are edited and stored like previously in Plone.


Here is a example for a view in Volto, the view for News Items:

..   code-block:: js

    /**
     * NewsItemView view component.
     * @module components/theme/View/NewsItemView
     */

    import React from 'react';
    import PropTypes from 'prop-types';
    import { Helmet } from '@plone/volto/helpers';
    import { Container, Image } from 'semantic-ui-react';

    import { flattenToAppURL } from '../../../helpers';

    /**
     * NewsItemView view component class.
     * @function NewsItemView
     * @params {object} content Content object.
     * @returns {string} Markup of the component.
     */
    const NewsItemView = ({ content }) => (
      <Container className="view-wrapper">
        <Helmet title={content.title} />
        {content.title && (
          <h1 className="documentFirstHeading">
            {content.title}
            {content.subtitle && ` - ${content.subtitle}`}
          </h1>
        )}
        {content.description && (
          <p className="documentDescription">{content.description}</p>
        )}
        {content.image && (
          <Image
            className="documentImage"
            alt={content.title}
            title={content.title}
            src={
              content.image['content-type'] === 'image/svg+xml'
                ? flattenToAppURL(content.image.download)
                : flattenToAppURL(content.image.scales.mini.download)
            }
            floated="right"
          />
        )}
        {content.text && (
          <div dangerouslySetInnerHTML={{ __html: content.text.data }} />
        )}
      </Container>
    );

    /**
     * Property types.
     * @property {Object} propTypes Property types.
     * @static
     */
    NewsItemView.propTypes = {
      content: PropTypes.shape({
        title: PropTypes.string,
        description: PropTypes.string,
        text: PropTypes.shape({
          data: PropTypes.string,
        }),
      }).isRequired,
    };

    export default NewsItemView;
