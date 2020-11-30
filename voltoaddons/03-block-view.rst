======================
Improve the block view
======================

Let's add CSV file parsing.

There are many CSV parsers available for Nodejs, we'll use Papaparse_ because
it also works in the browser.

.. _Papaparse: https://www.npmjs.com/package/papaparse

We'll need to add the dependency to the add-on. When using yarn workspaces, the
workflow is a bit different. For our simple use case, we could probably run
``yarn add papaparse`` inside the ``src/addons/datatable-tutorial``, but
the correct way is to run this command through the project root.

First run ``yarn workspaces info`` to see the workspaces we have available.

.. code-block:: sh

    > yarn workspaces info
    {
      "@plone-collective/datatable-tutorial": {
        "location": "src/addons/datatable-tutorial",
        "workspaceDependencies": [],
        "mismatchedWorkspaceDependencies": []
      }
    }

To add a dependency to the package, run:

.. code-block:: sh

    > yarn workspace @plone-collective/datatable-tutorial add papaparse


And finally, the new block code:

.. code-block:: jsx

    import React from 'react';
    import { useDispatch, useSelector } from 'react-redux';
    import { Table } from 'semantic-ui-react';
    import csv from 'papaparse';
    import { getRawContent } from '@plone-collective/datatable-tutorial/actions';

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

Writing components where the ``useEffect`` triggers network calls can be pretty
tricky. According to the `rule of hooks`_, hooks can't be triggered
conditionally, they always have to be run. For this reason it's important to
add relevant conditions inside the hook code, so be sure to identify and
prepare a way to tell, from inside the hook, if the network-fetching action
should be dispatched.

.. _`rule of hooks`: https://reactjs.org/docs/hooks-rules.html

The React HOC Pattern
---------------------

It is a good idea to split the code in generic "code blocks" so that behavior
and look are separated. This has many benefits: it makes components easier to
write and test, it separates business logic in reusable behaviors, etc.

So, can we abstract the data grabbing logic? Let's write a simple Higher Order
Component (HOC) that does the data grabbing:

.. code-block:: jsx

    const withFileData = (WrappedComponent) => {
      return (props) => <WrappedComponent {...props} />;
    };

    export default withFileData(DataTableView);

And now let's move the file download and parsing logic to this HOC.
We'll create the ``src/hocs/withFileData.js`` file:

.. code-block:: jsx

    import React from 'react';

    import { useDispatch, useSelector } from 'react-redux';
    import csv from 'papaparse';
    import { getRawContent } from '@plone-collective/datatable-tutorial/actions';

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
          if (path && !request?.loading && !request?.loaded && !content)
            dispatch(getRawContent(path));
        }, [dispatch, path, content, request?.loaded, request?.loading]);

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

This HOC now gets the data from the Redux store using the logic and code we've
used previously and then simply injects it as a new property to the original
wrapped component.

An HOC is a simple function that gets a component and returns another
component.  For a Python developer, the decorators are a very similar concept.
One thing to pay attention, React component names need to be referenced as
PascalCase in JSX code.

And now the view component is simple, neat and focused:

.. code-block:: jsx

    import React from 'react';
    import { Table } from 'semantic-ui-react';
    import { withFileData } from '@plone-collective/datatable-tutorial/hocs';

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

Note: for the purpose of this tutorial, the ``withFileData`` HOC has been
created a bit simplistic. To make it more generic, we could avoid hard-coding
the field name, by doing something like this:

.. code-block:: jsx

    const withFileData = (getFilePath) => (WrappedComponent) => {
      return (props) => {
        const file_path = getFilePath(props);
    ...

And we change how we wrap the ``DataTableView`` to keep the file_path specific
logic local to the ``DataTable`` component

.. code-block:: jsx

    export default withFileData(({ data: { file_path } }) => file_path)(
      DataTableView,
    );
