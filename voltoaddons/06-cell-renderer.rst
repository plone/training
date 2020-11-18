=========================
Make the block extendible
=========================

Wouldn't it be nice if we could have a way to customize, per column, how the
values are rendered and go even further then the ``textTemplate`` field would
allow?

Let's create the following extension mechanism: for any column, we'll be able
to choose between available "cell renderers". These would be components that
get passed the value and can render themselves as they want. For example, we
could implement a "progress bar" that could be used to render the numbers in
a column as a solid bar of color. We'll also migrate the text template field to
the new system.

What's more, we'll use the global Volto config registry to register our custom
components, so it will be completely open to extension from projects or other
addons.

We could use the global ``config.settings`` object to register the new cell
renderers, but this functionality is directly related to our custom data block,
so let's just use the block's config object.

.. code-block:: jsx

    config.blocks.blocksConfig.dataTable = {
      id: 'dataTable',
      title: 'Data Table',
      icon: tableSVG,
      group: 'common',
      view: DataTableView,
      edit: DataTableEdit,
      restricted: false,
      mostUsed: false,
      sidebarTab: 1,
      security: {
        addPermission: [],
        view: [],
      },
      cellRenderers: {
        textTemplate: {
          id: 'textTemplate',
          title: 'Text Template',
          view: TextTemplateRenderer,
          schemaExtender: TextTemplateRenderer.schemaExtender,
        },
        progress: {
          id: 'progress',
          title: 'Progress',
          view: ProgressCellRenderer,
        },
      },
    };

Notice the ``schemaExtender`` field. We'll use it to allow each extension to
provide its own fields in the column edit widget. volto-object-widget allows
the schema used in its FlatObjectList widget to be extended by a provided
schema extender, so we'll integrate with that.

The old text template-based implementation can be moved to an component and
a schema extension, like:

.. code-block:: jsx

    const TextTemplateRenderer = ({ column, value }) => {
      return column.textTemplate ? column.textTemplate.replace('{}', value) : value;
    };

    TextTemplateRenderer.schemaExtender = (schema) => {
      schema.properties.textTemplate = {
        title: 'Text template',
        description: 'Add suffix/prefix to text. Use {} for value placeholder',
      };
      schema.fieldsets[0].fields.push('textTemplate');

      return schema;
    };

    export default TextTemplateRenderer;

For the Progress renderer, we won't need to extend the schema:

.. code-block:: jsx

    import React from 'react';

    import { Progress as UiProgress } from 'semantic-ui-react';

    const Progress = ({ value }) => {
      const v = Math.round(parseFloat(value));
      return <UiProgress percent={v} />;
    };

    export default Progress;

.. note::

    As an exercise you could extend the Progress renderer to include a color
    field. Build a color widget using react-color_

.. _react-color: https://github.com/casesandberg/react-color

The ``ColumnSchema`` needs to be tweaked to add the new renderer field. It can
be as simple as:

.. code-block:: jsx

    renderer: {
      title: 'Format',
      choices: [],
    },

Now, back to the ``DataTableEdit`` component, we'll add this schema tweaking
code:

.. code-block:: jsx

    const tweakSchema = (schema, data, file_data) => {
      const columnsField = schema.properties.columns;
      const ColumnsSchema = columnsField.schema;

      const columns = (file_data?.meta?.fields || []).sort().map((n) => [n, n]);
      ColumnsSchema.properties.column.choices = columns;

      const { cellRenderers } = blocks.blocksConfig.dataTable;
      const renderers = Object.keys(cellRenderers).map((k) => [
        k,
        cellRenderers[k].title,
      ]);
      ColumnsSchema.properties.renderer.choices = renderers;

      columnsField.schemaExtender = (schema, data) => {
        const extension = data.renderer
          ? cellRenderers[data.renderer].schemaExtender
          : null;
        return extension ? extension(schema, data) : schema;
      };

      return schema;
    };

With the "schema tweaking code" we're doing three things:

- add the columns from the file as choices to the "Column" widget
- provide the "renderer" field with the available cellRenderer choices
- plug into the schemaExtender of the columnsField our own schema extender.

And we'll replace the old schema tweak with the new one:

.. code-block:: jsx

    const schema = tweakSchema(TableSchema(props), data, file_data);

Again, back to the ``columnsField.schemaExtender`` bit. This is an invention
that volto-object-widget supports, to allow schema customizations per object,
in a list of objects.

It is a function with signature ``(schema, data) => schema``
