We'll add editing to the block. The most basic schema looks something like
this:

.. code-block:: jsx

    export const TableSchema = () => ({
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

This schema is based on the one used by the plone.restapi to edit the
server-side Dexterity content.  We're appropriating it, it lives in the client
side right now, so we have some freedom in extending it with new logic and
capabilities. The only requirement is that Volto's form understands it, but
even here we have a lot of freedom, as the form passes all the field props to
the widgets.

To understand how to structure the schema you need to read Volto's Field.jsx
code. In it we see the following logic:

.. code-block:: jsx

  const Widget =
    getWidgetByFieldId(props.id) ||
    getWidgetByName(props.widget) ||
    getWidgetByChoices(props) ||
    getWidgetByVocabulary(props.vocabulary) ||
    getWidgetByVocabularyFromHint(props) ||
    getWidgetByFactory(props.factory) ||
    getWidgetByType(props.type) ||
    getWidgetDefault();

Now we add a basic schema to control the tabel styling:

.. code-block:: jsx

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
          widget: 'pick_object',
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

And the view module can become:

.. code-block:: jsx

    import React from 'react';
    import { Table } from 'semantic-ui-react';
    import { withFileData } from '@plone/datatable-tutorial/hocs';

    const format = (data) => {
      return {
        fixed: data.fixed,
        compact: data.compact,
        basic: data.basic ? 'very' : undefined,
        celled: data.celled,
        inverted: data.inverted,
        striped: data.striped,
      };
    };

    const DataTableView = ({ file_data, data }) => {
      const fields = file_data?.meta?.fields || [];

      return file_data ? (
        <Table {...format(data)}>
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

    export default withFileData(({ data: { file_path } }) => file_path)(
      DataTableView,
    );

To use the schema we need to change the block edit component:

.. code-block:: jsx

    const DataTableEdit = (props) => {
      const { selected, onChangeBlock, block, data } = props;
      const schema = TableSchema(props);

      return (
        <div className="datatable-edit">
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
                  widget="pick_object"
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

