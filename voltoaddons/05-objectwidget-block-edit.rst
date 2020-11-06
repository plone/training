Let's add a bit more control over how the columns are rendered. This is quite
a "low hanging fruit" thanks to the ``volto-object-widget`` addon. This addon
has another dependency, the volto-blocks-form, so let's add them both:

.. code-block:: sh

    yarn workspace @plone/datatable-tutorial add eea/volto-object-widget#0.2.3
    yarn workspace @plone/datatable-tutorial add eea/volto-blocks-form#0.5.2

Add the volto-object-widget addon in the project's package.json:

.. code-block:: json

  "addons": [
    "@eeacms/volto-blocks-form",
    "@eeacms/volto-object-widget",
    "@plone/datatable-tutorial"
  ],

The order in which we load the addons can sometimes be relevant. Ideally the
configuration options are used only at "runtime", on demand, but there are
cases when an addon can depend on a specific configuration at "configure time".

It's not our case, though. It's still a good idea to list generic addons first.

Note: we've had to add ``@eeacms/volto-blocks-form`` to the addons list to help
Volto's webpack resolver, as we're distributing this addon in "source code
form".

What would we like to change about the columns? Let's go for: title, text align
and another field that would allow us to tweak how the values are rendered.

Note: we'll continue without i18n integration for now, to keep things simpler

.. code-block:: jsx

    const ColumnSchema = (props) => ({
      title: 'Column',
      fieldsets: [
        {
          id: 'default',
          title: 'Default',
          fields: ['column', 'title', 'textTemplate', 'textAlign'],
        },
      ],
      properties: {
        title: {
          title: 'Header',
        },
        textTemplate: {
          title: 'Text template',
          description: 'Add suffix/prefix to text. Use {} for value placeholder',
        },
        textAlign: {
          title: 'Align',
          // widget: 'text_align',
          choices: [
            ['left', 'left'],
            ['center', 'center'],
            ['right', 'right'],
          ],
        },
        column: {
          title: 'Data column',
          choices: [],
        },
      },
      required: ['column'],
    });


Now, let's make use of this schema. We'll add a new field to the TableSchema:

.. code-block:: jsx

    //...
    properties: {
        //...
        columns: {
          title: 'Columns',
          description: 'Leave empty to show all columns',
          schema: ColumnSchema({ intl }),
          widget: 'object_list_inline',
        },
    }

Don't forget to add the ``columns`` fieldname to the ``default`` fieldset.

Now we need to plug the available columns as choices to the schema. In Plone's
world we would write an adapter that binds the widget to the context or
something like that. Let's keep things really simple though and hardcode the
available choices to the schema. How? By simply mutating the schema before we
pass it to the ``<InlineForm>`` component.

.. code-block:: jsx

    const DataTableEdit = (props) => {
      const { selected, onChangeBlock, block, data, file_data } = props;
      const schema = TableSchema(props);
      const choices = (file_data?.meta?.fields || []).sort().map((n) => [n, n]);
      schema.properties.columns.schema.properties.column.choices = choices;

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

We'll need to also inject the file data to the edit form, we didn't need to
before, but now it needs to know what are the available columns. Now that we're
wrapping the edit component in two HOCs, we'll use redux's compose to play
nice.

.. code-block:: jsx

    const getFilePath = ({ data: { file_path } }) => file_path;

    export default compose(
      withFileData(getFilePath),
      withBlockDataSource({
        getFilePath,
        icon: tableSVG,
        title: 'Data table',
      }),
    )(DataTableEdit);

Let's go back to the view component and use the column definitions from the
block data.

.. code-block:: jsx

    const DataTableView = ({ file_data, data }) => {
      const columns =
        data.columns?.length > 0
          ? data.columns
          : file_data?.meta?.fields?.map((n) => ({
              column: n,
            }));

      return file_data ? (
        <Table {...format(data)}>
          <Table.Header>
            <Table.Row>
              {show_fields.map((col, i) => (
                <Table.HeaderCell key={i} textAlign={col.textAlign}>
                  {col.title || col.column}
                </Table.HeaderCell>
              ))}
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {file_data.data.map((o, i) => (
              <Table.Row key={i}>
                {columns.map((col, y) => (
                  <Table.Cell textAlign={col.textAlign}>
                    {col.textTemplate
                      ? col.textTemplate.replace('{}', o[col.column])
                      : o[col.column]}
                  </Table.Cell>
                ))}
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      ) : (
        <div>No data</div>
      );
    };

These minimal changes enable our code to have custom column titles, custom text
align and to affect the way the values are rendered in the cells.

Of course, now the sky is the limit. We could enhance this with number
formating provided by a library to humanize and automatically format those
values, or d3's format. There's plenty of choices.

Let's enhance the edit form by creating an align widget for the text align
field. Let's create ``src/widgets/TextAlign.jsx``.

.. code-block:: jsx

    import React from 'react';
    import { Button } from 'semantic-ui-react';
    import { FormFieldWrapper, Icon } from '@plone/volto/components';

    import alignLeftSVG from '@plone/volto/icons/align-left.svg';
    import alignRightSVG from '@plone/volto/icons/align-right.svg';
    import alignJustifySVG from '@plone/volto/icons/align-justify.svg';
    import alignCenterSVG from '@plone/volto/icons/align-center.svg';

    const VALUE_MAP = [
      ['left', alignLeftSVG],
      ['right', alignRightSVG],
      ['center', alignCenterSVG],
      ['justify', alignJustifySVG],
    ];

    export default (props) => {
      const { value, onChange, id } = props;
      return (
        <FormFieldWrapper {...props}>
          <div className="align-tools">
            {VALUE_MAP.map(([name, icon]) => (
              <Button.Group>
                <Button
                  icon
                  basic
                  compact
                  active={value === name}
                  aria-label={name}
                  onClick={() => {
                    onChange(id, name);
                  }}
                >
                  <Icon name={icon} size="24px" />
                </Button>
              </Button.Group>
            ))}
          </div>
        </FormFieldWrapper>
      );
    };

And we'll register it in the src/index.js default configuration method:

.. code-block:: jsx

    import { TextAlign } from './widgets';

    // ... change in the default configuration function
    if (!config.widgets.widget.text_align)
        config.widgets.widget.text_align = TextAlign;

Now go back to the schema and let's use the new text align widget:

.. code-block:: jsx

    // change in TableSchema properties
    textAlign: {
      title: 'Align',
      widget: 'text_align',
    },

volto-object-widget provides drag/drop sorting of the columns so it's possible
to reorder the columns.

we could call this done for now... but let's go some steps further and explore
how to further enhance this addon's reusability and extensability.
