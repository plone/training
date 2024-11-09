---
myst:
  html_meta:
    "description": "Volto add-ons development training module 4, add-ons block edit"
    "property=og:description": "Volto add-ons development training module 4"
    "property=og:title": "Volto add-ons development block edit options"
    "keywords": "Volto"
---

# Block editing with a form

We'll add schema-based editing of the block settings.
In Volto the convention is to use the schema generated from a function, so that
the resulting object can be freely mutated, as it comes from a closure.

The most basic schema would look something like this:

```jsx
export const TableSchema = ({formData, intl}) => ({
  title: 'Table',
  fieldsets: [
    {
      id: 'default',
      title: 'Default',
      fields: ['description'],
    },
  ],
  properties: {
    description: {
        title: 'Description',
        widget: 'textarea'
    }
  },
  required: ['title'],
});
```

This schema is based on the one used by `plone.restapi` to edit the server-side
`Dexterity` content.  We're appropriating it.  It lives on the client side
right now, so we have some freedom in extending it with new logic and
capabilities.  The only requirement is that Volto's form implementation
understands it.  But even here we have a lot of freedom, as the form passes all
the field props to the widgets.

To understand how to structure the schema, you need to read Volto's
[Field.jsx] code.  In it, we see the following logic:

```jsx
const Widget =
  getWidgetByFieldId(props.id) ||
  getWidgetByName(props.widget) ||
  getWidgetByChoices(props) ||
  getWidgetByVocabulary(props.vocabulary) ||
  getWidgetByVocabularyFromHint(props) ||
  getWidgetByFactory(props.factory) ||
  getWidgetByType(props.type) ||
  getWidgetDefault();
```

The precedence order of the algorithm is pretty self-explanatory.

You can specify a widget for a particular field with:

```jsx
config.widgets.id.some_fieldname = MyWidget`;
```

Or you can set the `widget` property in a schema:

```jsx
//...
properties: {
  headline: {
    title: "Headline",
    widget: "headline_widget",
  }
}
//...
```

See [Volto's widget documentation] for more details, including how to designate
a widget for a particular Dexterity field.

Now we add a basic schema to control the table styling. Create the
`src/DataTable/schema.js` file:

```jsx
import { defineMessages } from 'react-intl';

export const TableSchema = ({ intl }) => ({
  title: 'Table',

  fieldsets: [
    {
      id: 'default',
      title: intl.formatMessage(messages.defaultFieldset),
      fields: ['file_path'],
    },
    {
      id: 'style',
      title: intl.formatMessage(messages.styling),
      fields: ['fixed', 'celled', 'striped', 'compact', 'basic', 'inverted'],
    },
  ],

  properties: {
    file_path: {
      title: intl.formatMessage(messages.dataFile),
      widget: 'object_browser',
      mode: 'link',
    },
    fixed: {
      type: 'boolean',
      title: intl.formatMessage(messages.fixed),
    },
    compact: {
      type: 'boolean',
      title: intl.formatMessage(messages.compact),
    },
    basic: {
      type: 'boolean',
      title: intl.formatMessage(messages.basic),
    },
    celled: {
      type: 'boolean',
      title: intl.formatMessage(messages.celled),
    },
    inverted: {
      type: 'boolean',
      title: intl.formatMessage(messages.inverted),
    },
    striped: {
      type: 'boolean',
      title: intl.formatMessage(messages.striped),
    },
  },

  required: ['file_path'],
});

const messages = defineMessages({
  fixed: {
    id: 'Fixed width table cells',
    defaultMessage: 'Fixed width table cells',
  },
  compact: {
    id: 'Make the table compact',
    defaultMessage: 'Make the table compact',
  },
  basic: {
    id: 'Reduce complexity',
    defaultMessage: 'Reduce complexity',
  },
  celled: {
    id: 'Divide each row into separate cells',
    defaultMessage: 'Divide each row into separate cells',
  },
  inverted: {
    id: 'Table color inverted',
    defaultMessage: 'Table color inverted',
  },
  striped: {
    id: 'Stripe alternate rows with color',
    defaultMessage: 'Stripe alternate rows with color',
  },
  styling: {
    id: 'Styling',
    defaultMessage: 'Styling',
  },
  defaultFieldset: {
    id: 'Default',
    defaultMessage: 'Default',
  },
  dataFile: {
    id: 'Data file',
    defaultMessage: 'Data file',
  },
});
```

Notice that our schema is actually a function that returns a JavaScript object,
not least because we need to have access to the `intl` utility to provide
internationalization.

To use the schema, we need to change the block edit component from
`src/DataTable/DataTableEdit.jsx`:

```jsx
// ...
import { InlineForm } from '@plone/volto/components';
import { TableSchema } from './schema';
// ...

const DataTableEdit = (props) => {
  const { selected, onChangeBlock, block, data } = props;
  const schema = TableSchema(props);

  return (
    <div className="dataTable-edit">
      <SidebarPortal selected={selected}>
        {!data.file_path?.length ? (
          <Segment.Group raised>
            <header className="header pulled">
              <h2>Data table</h2>
            </header>
            <Segment className="sidebar-metadata-container" secondary>
              No file selected
              <Icon name={tableSVG} size="100px" color="#b8c6c8" />
            </Segment>
          </Segment.Group>
        ) : (
          ''
        )}
        {data.file_path ? (
          <InlineForm
            schema={schema}
            title={schema.title}
            onChangeField={(id, value) => {
              onChangeBlock(block, {
                ...data,
                [id]: value,
              });
            }}
            formData={data}
          />
        ) : (
          ''
        )}
      </SidebarPortal>
      {data.file_path?.length ? (
        <DataTableView {...props} />
      ) : (
        <div className="no-value">
          <Form>
            <Icon name={tableSVG} size="100px" color="#b8c6c8" />
            <Field
              id="file_path"
              widget="object_browser"
              mode="link"
              title="Pick a file"
              value={data.file_path || []}
              onChange={(id, value) => {
                onChangeBlock(block, {
                  ...data,
                  [id]: value,
                });
              }}
            />
          </Form>
        </div>
      )}
    </div>
  );
};

export default DataTableEdit;
```

We're using the `InlineForm`, a component provided by Volto that renders an "embeddable" form.
This form requires, as parameters, the schema, and the form values.
We'll render this form in the sidebar.

Now the view module from `src/DataTable/DataTable.jsx` can become:

```{code-block} jsx
:force: true

import React from 'react';
import { Table } from 'semantic-ui-react';
import { withFileData } from '@plone-collective/volto-datatable-tutorial/hocs';

const format = (data) => {
  return {
    fixed: data.fixed,
    compact: data.compact,
    basic: data.basic ? 'very' : undefined,
    celled: data.celled,
    inverted: data.inverted,
    striped: data.striped
  };
};

const DataTableView = ({ file_data, data }) => {
  const fields = file_data?.meta?.fields || [];

  return file_data ? (
    <Table { ...format(data) }>
      <Table.Header>
        <Table.Row>
          {fields.map((f) => (
            <Table.Cell key={f}>{f}</Table.Cell>
          ))}
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {file_data.data.map((o, i) => (
          <Table.Row key={i}>
            {fields.map((f) => (
              <Table.Cell>{o[f]}</Table.Cell>
            ))}
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  ) : (
    <div>No data</div>
  );
};

export default withFileData(DataTableView);
```

Here's how your block would look like:

```{image} _static/basic-table-edit.png
```

## Initial block data as a reusable pattern

For the view component, we've created a `HOC` mechanism that grants automatic data injection.
Can we do the same and simplify the `Edit` component?
Let's make the "new block needs to point to a file", a mechanism that we can reuse.
Perhaps later we'll write a chart block that uses the CSV file, so we'll be
able to reuse code by composing.

Add the `src/hocs/withBlockDataSource.js` HOC file:

```jsx
import React from 'react';
import { Segment, Form } from 'semantic-ui-react';
import { SidebarPortal, Field, Icon } from '@plone/volto/components';

const withBlockDataSource = (opts) => (WrappedComponent) => {
  const { icon, title, getFilePath } = opts;

  return (props) => {
    const { data, selected, onChangeBlock, block } = props;
    const file_path = getFilePath(props);

    return (
      <div className={`${data['@type']}-edit`}>
        {!file_path ? (
          <>
            <div className="no-value">
              <Form>
                <Icon name={icon} size="100px" color="#b8c6c8" />
                <Field
                  id="file_path"
                  widget="object_browser"
                  mode="link"
                  title="Pick a file"
                  value={file_path || []}
                  onChange={(id, value) => {
                    onChangeBlock(block, {
                      ...data,
                      [id]: value,
                    });
                  }}
                />
              </Form>
            </div>

            <SidebarPortal selected={selected}>
              <Segment.Group raised>
                <header className="header pulled">
                  <h2>{title}</h2>
                </header>
                <Segment className="sidebar-metadata-container" secondary>
                  No file selected
                  <Icon name={icon} size="100px" color="#b8c6c8" />
                </Segment>
              </Segment.Group>
            </SidebarPortal>
          </>
        ) : (
          <WrappedComponent {...props} />
        )}
      </div>
    );
  };
};

export default withBlockDataSource;
```

Make sure to export this new `HOC` from the `src/hocs/index.js` file with:

```jsx
export withFileData from './withFileData';
export withBlockDataSource from './withBlockDataSource';
```

Within `src/DataTable/DataTableEdit.js` now import the newly added
`withBlockDataSource` higher-order component.

Make use of it by replacing the `DataTableEdit` component, and it's export with:

```jsx
import React from 'react';
import { InlineForm, SidebarPortal } from '@plone/volto/components';
import tableSVG from '@plone/volto/icons/table.svg';

import { withBlockDataSource } from '@plone-collective/volto-datatable-tutorial/hocs';

import { TableSchema } from './schema';
import DataTableView from './DataTableView';

import './datatable-edit.less';

const DataTableEdit = (props) => {
  const { selected, onChangeBlock, block, data } = props;
  const schema = TableSchema(props);

  return (
    <>
      <SidebarPortal selected={selected}>
        <InlineForm
          schema={schema}
          title={schema.title}
          onChangeField={(id, value) => {
            onChangeBlock(block, {
              ...data,
              [id]: value,
            });
          }}
          formData={data}
        />
      </SidebarPortal>
      <DataTableView {...props} />
    </>
  );
};

export default withBlockDataSource({
  icon: tableSVG,
  title: 'Data table',
  getFilePath: ({ data: { file_path } }) => file_path?.[0],
})(DataTableEdit);
```

[field.jsx]: https://github.com/plone/volto/blob/main/packages/volto/src/components/manage/Form/Field.jsx
[Volto's widget documentation]: https://github.com/plone/volto/blob/main/docs/source/development/widget.md
