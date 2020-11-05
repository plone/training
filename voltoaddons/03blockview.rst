Let's add CSV file parsing.

There are many CSV parsers available for node/js, we'll just pick one and move
on.

We'll need to add the dependency to the addon. When using yarn workspaces, the
workflow is a bit different. For our simple use case, we could probably run
``yarn add @fast-csv/parse`` inside the ``src/addons/datatable-tutorial``, but
the correct way is to run this command through the project root.

First run ``yarn workspaces info`` to see the workspaces we have available.

.. code-block:: sh

    > yarn workspaces info
    {
      "@plone/datatable-tutorial": {
        "location": "src/addons/datatable-tutorial",
        "workspaceDependencies": [],
        "mismatchedWorkspaceDependencies": []
      }
    }

To add a dependency to the package, run:

.. code-block:: sh

    > yarn workspace @plone/datatable-tutorial add @fast-csv/parse


And finally, the new block code:

.. code-block:: jsx

    import React from 'react';
    import { useDispatch, useSelector } from 'react-redux';
    import { Table } from 'semantic-ui-react';
    import csv from 'papaparse';
    import { getRawContent } from '@plone/datatable-tutorial/actions';

    const DataTableView = ({ data: { file_path } }) => {
      const id = file_path?.[0]?.['@id'];
      const path = id ? `${id}/@@download` : null;

      const dispatch = useDispatch();
      const request = useSelector((state) => state.rawdata?.[path]);

      const content = request?.data;

      React.useEffect(() => {
        if (path && !content) dispatch(getRawContent(path));
      }, [dispatch, path, content]);

      const file_data = React.useMemo(() => {
        if (content) {
          const res = csv.parse(content, { header: true });
          return res;
        }
      }, [content]);

      const fields = file_data?.meta?.fields || [];

      return file_data ? (
        <Table celled>
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

    export default DataTableView;

Can we abstract the data grabbing logic?

Let's write a simple Higher Order Component that does the data grabbing:

.. code-block:: jsx

    const withFileData = (WrappedComponent) => {
      return (props) => <WrappedComponent {...props} />;
    };

    export default withFileData(DataTableView);

And now let's move the file download and parsing logic to this HOC.
We'll create the ``withFileData.js`` file in ``hocs``:

.. code-block:: jsx

    import React from 'react';

    import { useDispatch, useSelector } from 'react-redux';
    import csv from 'papaparse';
    import { getRawContent } from '@plone/datatable-tutorial/actions';

    const withFileData = (WrappedComponent) => {
      return (props) => {
        const {
          data: { file_path },
        } = props;
        const id = file_path?.[0]?.['@id'];
        const path = id ? `${id}/@@download` : null;

        const dispatch = useDispatch();
        const request = useSelector((state) => state.rawdata?.[path]);

        const content = request?.data;

        React.useEffect(() => {
          if (path && !content) dispatch(getRawContent(path));
        }, [dispatch, path, content]);

        const file_data = React.useMemo(() => {
          if (content) {
            const res = csv.parse(content, { header: true });
            return res;
          }
        }, [content]);
        return <WrappedComponent file_data={file_data} {...props} />;
      };
    };

    export default withFileData;

And now the view component is simple, neat and focused:

.. code-block:: jsx

    import React from 'react';
    import { Table } from 'semantic-ui-react';
    import { withFileData } from '@plone/datatable-tutorial/hocs';

    const DataTableView = ({ file_data }) => {
      const fields = file_data?.meta?.fields || [];

      return file_data ? (
        <Table celled>
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

Note: for the purpose of this tutorial, the withFileData HOC has been created
a bit simplistic. To make it more generic, we could avoid hard-coding the field
name, by doing something like this:

.. code-block:: jsx

    const withFileData = (getFilePath) => (WrappedComponent) => {
      return (props) => {
        const file_path = getFilePath(props);
    ...

And we change how we wrap the DataTableView to keep the file_path specific
logic local to the DataTable component

.. code-block:: jsx

    export default withFileData(({ data: { file_path } }) => file_path)(
      DataTableView,
    );
