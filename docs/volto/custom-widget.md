---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(custom-widget-label)=

# Custom Widget

In this chapter we are going to build a custom widget.
The widget we are going to build is a rating widget with one to five stars.

## Setup The Content Type

We will add a rating field to the `Page` content type.
Go to the Plone Control Panel at <http://localhost:8080/Plone/dexterity-types/Document>.
Add a field called `Rating` with short name `rating` and type `Integer`.

Next we will create a file `components/RatingWidget/RatingWidget.jsx`.
We will start with a copy of the `components/manage/Widgets/TextWidget.jsx` file from Volto,
and rename the class to `RatingWidget`.

```jsx
/**
 * RatingWidget component.
 * @module components/RatingWidget/RatingWidget
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Form, Grid, Icon, Input, Label } from 'semantic-ui-react';
import { map } from 'lodash';
import { defineMessages, injectIntl, intlShape } from 'react-intl';

const messages = defineMessages({
  default: {
    id: 'Default',
    defaultMessage: 'Default',
  },
  idTitle: {
    id: 'Short Name',
    defaultMessage: 'Short Name',
  },
  idDescription: {
    id: 'Used for programmatic access to the fieldset.',
    defaultMessage: 'Used for programmatic access to the fieldset.',
  },
  title: {
    id: 'Title',
    defaultMessage: 'Title',
  },
  description: {
    id: 'Description',
    defaultMessage: 'Description',
  },
  required: {
    id: 'Required',
    defaultMessage: 'Required',
  },
});

/**
 * RatingWidget component class.
 * @function RatingWidget
 * @returns {string} Markup of the component.
 */
const RatingWidget = ({
  id,
  title,
  required,
  description,
  error,
  value,
  onChange,
  onEdit,
  onDelete,
  intl,
}) => {
  const schema = {
    fieldsets: [
      {
        id: 'default',
        title: intl.formatMessage(messages.default),
        fields: ['title', 'id', 'description', 'required'],
      },
    ],
    properties: {
      id: {
        type: 'string',
        title: intl.formatMessage(messages.idTitle),
        description: intl.formatMessage(messages.idDescription),
      },
      title: {
        type: 'string',
        title: intl.formatMessage(messages.title),
      },
      description: {
        type: 'string',
        widget: 'textarea',
        title: intl.formatMessage(messages.description),
      },
      required: {
        type: 'boolean',
        title: intl.formatMessage(messages.required),
      },
    },
    required: ['id', 'title'],
  };

  return (
    <Form.Field
      inline
      required={required}
      error={error.length > 0}
      className={description ? 'help' : ''}
    >
      <Grid>
        <Grid.Row stretched>
          <Grid.Column width="4">
            <div className="wrapper">
              <label htmlFor={`field-${id}`}>
                {onEdit && (
                  <i
                    aria-hidden="true"
                    className="grey bars icon drag handle"
                  />
                )}
                {title}
              </label>
            </div>
          </Grid.Column>
          <Grid.Column width="8">
            {onEdit && (
              <div className="toolbar">
                <a className="item" onClick={() => onEdit(id, schema)}>
                  <Icon name="write square" size="large" color="blue" />
                </a>
                <a className="item" onClick={() => onDelete(id)}>
                  <Icon name="close" size="large" color="red" />
                </a>
              </div>
            )}
            <Input
              id={`field-${id}`}
              name={id}
              value={value || ''}
              disabled={onEdit !== null}
              onChange={({ target }) =>
                onChange(id, target.value === '' ? undefined : target.value)
              }
            />
            {map(error, message => (
              <Label key={message} basic color="red" pointing>
                {message}
              </Label>
            ))}
          </Grid.Column>
        </Grid.Row>
        {description && (
          <Grid.Row stretched>
            <Grid.Column stretched width="12">
              <p className="help">{description}</p>
            </Grid.Column>
          </Grid.Row>
        )}
      </Grid>
    </Form.Field>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
RatingWidget.propTypes = {
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  required: PropTypes.bool,
  error: PropTypes.arrayOf(PropTypes.string),
  value: PropTypes.string,
  onChange: PropTypes.func,
  onEdit: PropTypes.func,
  onDelete: PropTypes.func,
  intl: intlShape.isRequired,
};

/**
 * Default properties.
 * @property {Object} defaultProps Default properties.
 * @static
 */
RatingWidget.defaultProps = {
  description: null,
  required: false,
  error: [],
  value: null,
  onChange: null,
  onEdit: null,
  onDelete: null,
};

export default injectIntl(RatingWidget);
```

Next we will add `RatingWidget` to the `components/index.js` file so we can import the widget.

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
import FullView from './FullView/FullView';
import RatingWidget from './RatingWidget/RatingWidget';

export { AlbumView, FullView, RatingWidget };
```

## Registering The Widget

We can register a widget based on multiple checks for the widget set by the backend,
the type of the field and so on.
For this example we will be using the selection based on `id`.
This way we will only change the widget of this field.

```jsx
import { AlbumView, FullView, RatingWidget } from './components';

export const widgets = {
  ...defaultWidgets,
  id: {
    ...defaultWidgets.id,
    rating: RatingWidget,
  },
};
```

## Exercise

Finish the `RatingWidget` by converting the `TextWidget`.
You can use the `Rating` component from `semantic-ui`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```jsx
/**
 * RatingWidget component.
 * @module components/RatingWidget/RatingWidget
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Form, Grid, Icon, Label, Rating } from 'semantic-ui-react';
import { map } from 'lodash';
import { defineMessages, injectIntl, intlShape } from 'react-intl';

const messages = defineMessages({
  default: {
    id: 'Default',
    defaultMessage: 'Default',
  },
  idTitle: {
    id: 'Short Name',
    defaultMessage: 'Short Name',
  },
  idDescription: {
    id: 'Used for programmatic access to the fieldset.',
    defaultMessage: 'Used for programmatic access to the fieldset.',
  },
  title: {
    id: 'Title',
    defaultMessage: 'Title',
  },
  description: {
    id: 'Description',
    defaultMessage: 'Description',
  },
  required: {
    id: 'Required',
    defaultMessage: 'Required',
  },
});

/**
 * RatingWidget component class.
 * @function RatingWidget
 * @returns {string} Markup of the component.
 */
const RatingWidget = ({
  id,
  title,
  required,
  description,
  error,
  value,
  onChange,
  onEdit,
  onDelete,
  intl,
}) => {
  const schema = {
    fieldsets: [
      {
        id: 'default',
        title: intl.formatMessage(messages.default),
        fields: ['title', 'id', 'description', 'required'],
      },
    ],
    properties: {
      id: {
        type: 'string',
        title: intl.formatMessage(messages.idTitle),
        description: intl.formatMessage(messages.idDescription),
      },
      title: {
        type: 'string',
        title: intl.formatMessage(messages.title),
      },
      description: {
        type: 'string',
        widget: 'textarea',
        title: intl.formatMessage(messages.description),
      },
      required: {
        type: 'boolean',
        title: intl.formatMessage(messages.required),
      },
    },
    required: ['id', 'title'],
  };

  return (
    <Form.Field
      inline
      required={required}
      error={error.length > 0}
      className={description ? 'help' : ''}
    >
      <Grid>
        <Grid.Row stretched>
          <Grid.Column width="4">
            <div className="wrapper">
              <label htmlFor={`field-${id}`}>
                {onEdit && (
                  <i
                    aria-hidden="true"
                    className="grey bars icon drag handle"
                  />
                )}
                {title}
              </label>
            </div>
          </Grid.Column>
          <Grid.Column width="8">
            {onEdit && (
              <div className="toolbar">
                <a className="item" onClick={() => onEdit(id, schema)}>
                  <Icon name="write square" size="large" color="blue" />
                </a>
                <a className="item" onClick={() => onDelete(id)}>
                  <Icon name="close" size="large" color="red" />
                </a>
              </div>
            )}
            <Rating
              id={`field-${id}`}
              name={id}
              rating={value || 0}
              disabled={onEdit !== null}
              maxRating={5}
              onRate={(e, { rating }) => onChange(id, rating)}
            />
            {map(error, message => (
              <Label key={message} basic color="red" pointing>
                {message}
              </Label>
            ))}
          </Grid.Column>
        </Grid.Row>
        {description && (
          <Grid.Row stretched>
            <Grid.Column stretched width="12">
              <p className="help">{description}</p>
            </Grid.Column>
          </Grid.Row>
        )}
      </Grid>
    </Form.Field>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
RatingWidget.propTypes = {
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  required: PropTypes.bool,
  error: PropTypes.arrayOf(PropTypes.string),
  value: PropTypes.number,
  onChange: PropTypes.func,
  onEdit: PropTypes.func,
  onDelete: PropTypes.func,
  intl: intlShape.isRequired,
};

/**
 * Default properties.
 * @property {Object} defaultProps Default properties.
 * @static
 */
RatingWidget.defaultProps = {
  description: null,
  required: false,
  error: [],
  value: 0,
  onChange: null,
  onEdit: null,
  onDelete: null,
};

export default injectIntl(RatingWidget);
```
````
