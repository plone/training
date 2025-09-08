---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(actions-reducers-label)=

# Actions & Reducers

In this chapter we are going to create a custom content type.
We will create an FAQ content type.
We will then create a custom action and reducer to fetch this content type.

We start by creating the content type at: <http://localhost:8080/Plone/dexterity-types>.
We select `Add New Content Type...` and enter `Faq` as `Type Name` and `faq` as `Short Name`.
When we select the `Faq` item and go to the `Fields` tab we can see we already have the Dublin Core fields.
We are going to use the title for the question and the description for the answer.

In the root of the Plone site we will create a folder called `FAQ` with some FAQ items in there.

## Creating The Action

To create an action we will first add the action type to `constants/ActionTypes.js`.

```jsx
export const GET_FAQ = 'GET_FAQ';
```

Next we will create a file for our action at `actions/faq/faq.js`

```jsx
/**
 * Faq actions.
 * @module actions/faq/faq
 */

import { GET_FAQ } from '../../constants/ActionTypes';

/**
 * Get FAQ items.
 * @function getFaq
 * @returns {Object} Faq action.
 */
export function getFaq() {
  return {
    type: GET_FAQ,
    request: {
      op: 'get',
      path: `/@search?portal_type=faq`,
    },
  };
}
```

And we will add the actions to the `actions/index.js` file.

```jsx
import { getFaq } from './faq/faq';

export { getFaq };
```

## Creating The Reducer

Next we will create the reducer by creating the `reducers/faq/faq.js` file.

```jsx
/**
 * Faq reducer.
 * @module reducers/faq/faq
 */

import { map } from 'lodash';
import { settings } from '~/config';

import { GET_FAQ } from '../../constants/ActionTypes';

const initialState = {
  error: null,
  items: [],
  loaded: false,
  loading: false,
};

/**
 * Faq reducer.
 * @function faq
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export default function faq(state = initialState, action = {}) {
  switch (action.type) {
    case `${GET_FAQ}_PENDING`:
      return {
        ...state,
        error: null,
        loading: true,
        loaded: false,
      };
    case `${GET_FAQ}_SUCCESS`:
      return {
        ...state,
        error: null,
        items: map(action.result.items, item => ({
          ...item,
          '@id': item['@id'].replace(settings.apiPath, ''),
        })),
        loaded: true,
        loading: false,
      };
    case `${GET_FAQ}_FAIL`:
      return {
        ...state,
        error: action.error,
        items: [],
        loading: false,
        loaded: false,
      };
    default:
      return state;
  }
}
```

And we will add the `faq` reducer to the root reducer at `reducers/index.js`.

```jsx
/**
* Root reducer.
* @module reducers/root
*/

import defaultReducers from '@plone/volto/reducers';

import faq from './faq/faq';

/**
* Root reducer.
* @function
* @param {Object} state Current state.
* @param {Object} action Action to be handled.
* @returns {Object} New state.
*/
const reducers = {
    ...defaultReducers,
    faq,
};

export default reducers;
```

## Exercise

Add the `faq_view` as an available view to the `Folder` content type at <http://localhost:8080/Plone/portal_types/Folder/manage_propertiesForm>.
Set the `faq_view` for the folder at `http://localhost:3000/faq`.

Create the `faq_view` in Volto and use the actions and reducers created above.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

`components/FaqView/FaqView.jsx`

```jsx
/**
 * Faq view.
 * @module components/FaqView/FaqView
 */

import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Helmet } from '@plone/volto/helpers';
import { FormattedMessage } from 'react-intl';
import { Container } from 'semantic-ui-react';

import { getFaq } from '../../actions';

/**
 * FaqView class.
 * @class FaqView
 * @extends Component
 */
class FaqView extends Component {
  /**
   * Property types.
   * @property {Object} propTypes Property types.
   * @static
   */
  static propTypes = {
    getFaq: PropTypes.func.isRequired,
    items: PropTypes.arrayOf(
      PropTypes.shape({
        '@id': PropTypes.string,
        title: PropTypes.string,
        description: PropTypes.string,
      }),
    ),
  };

  /**
   * Default properties.
   * @property {Object} defaultProps Default properties.
   * @static
   */
  static defaultProps = {
    items: [],
  };

  /**
   * Component will mount
   * @method componentWillMount
   * @returns {undefined}
   */
  componentWillMount() {
    this.props.getFaq();
  }

  /**
   * Render method.
   * @method render
   * @returns {string} Markup for the component.
   */
  render() {
    return (
      <Container id="page-faq">
        <Helmet title="FAQ" />
        <div className="container">
          <article id="content">
            <header>
              <h1 className="documentFirstHeading">FAQ</h1>
            </header>
            <section id="content-core">
              {this.props.items.map(item => (
                <article className="tileItem" key={item['@id']}>
                  <h2 className="tileHeadline">{item.title}</h2>
                  {item.description && (
                    <div className="tileBody">
                      <span className="description">{item.description}</span>
                    </div>
                  )}
                  <div className="visualClear" />
                </article>
              ))}
            </section>
          </article>
        </div>
      </Container>
    );
  }
}

export default connect(
  state => ({
    items: state.faq.items,
  }),
  dispatch => bindActionCreators({ getFaq }, dispatch),
)(FaqView);
```

`components/index.jsx`

```jsx
/**
 * Add your components here.
 * @module components
 * @example
 * import Footer from './Footer/Footer';
 *
 * export {
 *   Footer,
 * };
 */

import AlbumView from './AlbumView/AlbumView';
import FaqView from './FaqView/FaqView';
import FullView from './FullView/FullView';
import RatingWidget from './RatingWidget/RatingWidget';

export { AlbumView, FaqView, FullView, RatingWidget };
```

`config.js`

```jsx
/**
 * Add your config changes here.
 * @module config
 * @example
 * export const settings = {
 *   ...defaultSettings,
 *   port: 4300,
 *   listBlockTypes: {
 *     ...defaultSettings.listBlockTypes,
 *     'my-list-item',
 *   }
 * }
 */

import React from 'react';
import createInlineStyleButton from 'draft-js-buttons/lib/utils/createInlineStyleButton';
import Icon from '@plone/volto/components/theme/Icon/Icon';
import underlineSVG from '@plone/volto/icons/underline.svg';
import codeSVG from '@plone/volto/icons/code.svg';

import {
  settings as defaultSettings,
  views as defaultViews,
  widgets as defaultWidgets,
  tiles as defaultTiles,
} from '@plone/volto/config';

import { AlbumView, FaqView, FullView, RatingWidget } from './components';

const UnderlineButton = createInlineStyleButton({
  style: 'UNDERLINE',
  children: <Icon name={underlineSVG} size="24px" />,
});

const CodeButton = createInlineStyleButton({
  style: 'CODE',
  children: <Icon name={codeSVG} size="24px" />,
});

export const settings = {
  ...defaultSettings,
  richTextEditorInlineToolbarButtons: [
    CodeButton,
    UnderlineButton,
    ...defaultSettings.richTextEditorInlineToolbarButtons,
  ],
};

export const views = {
  ...defaultViews,
  layoutViews: {
    ...defaultViews.layoutViews,
    album_view: AlbumView,
    full_view: FullView,
    faq_view: FaqView,
  },
};

export const widgets = {
  ...defaultWidgets,
  id: {
    ...defaultWidgets.id,
    rating: RatingWidget,
  },
};

export const tiles = {
  ...defaultTiles,
};
```
````
