---
myst:
  html_meta:
    "description": "Volto add-ons development training module 3, add-ons block view"
    "property=og:description": "Volto add-ons development training module 3"
    "property=og:title": "Volto add-ons development block view"
    "keywords": "Volto"
---

# Improve the block view

Let's add CSV file parsing.

There are many CSV parsers available for NodeJS.
We'll use [Papaparse](https://www.npmjs.com/package/papaparse) because it also works in the browser.

We'll need to add the dependency to the add-on if you haven't already done so,
as instructed in the first chapter. When using yarn workspaces, the
workflow is a bit different. For our simple use case, we could probably run
`yarn add papaparse` inside the `src/addons/volto-datatable-tutorial`, but
the correct way is to run this command within the project root.

First, run `yarn workspaces info` to see the workspaces we have available.

```console
yarn workspaces info

{
  "@plone-collective/volto-datatable-tutorial": {
    "location": "src/addons/volto-datatable-tutorial",
    "workspaceDependencies": [],
    "mismatchedWorkspaceDependencies": []
  }
}
```

To add a dependency to the package, run:

```sh
> yarn workspace @plone-collective/volto-datatable-tutorial add papaparse
```

And finally, the new block code within `src/DataTable/DataTable.jsx`:

```jsx
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Table } from 'semantic-ui-react';
import csv from 'papaparse';
import { getRawContent } from '@plone-collective/volto-datatable-tutorial/actions';

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
```

Writing components where the `useEffect` triggers network calls can be pretty tricky.
According to [Built-in React Hooks](https://legacy.reactjs.org/docs/hooks-rules.html), hooks can't be triggered conditionally.
They always have to be executed.
For this reason, it's important to add relevant conditions inside the hook code.
Be sure to identify and prepare a way to tell, from inside the hook, if the network-fetching action should be dispatched.

## The React HOC Pattern

It is a good idea to split the code into generic "code blocks" so that
behavior and look are separated.
This has many benefits:
- It makes components easier to write and test.
- It separates business logic into reusable behaviors.

Can we abstract the data-grabbing logic?
Let's write a simple Higher-Order Component (HOC) that does the data grabbing.
The simplest HOC wrapper looks like this:

```jsx
const withFileData = (WrappedComponent) => {
  return (props) => <WrappedComponent {...props} />;
};

export default withFileData(DataTableView);
```

Notice the similarity with Python decorators.
In our case, the HOC is a function that, given a component as input, returns
a React component.

Now let's move the file download and parsing logic to this HOC.
We'll create the `src/hocs/withFileData.js` file:

```jsx
import React from 'react';

import { useDispatch, useSelector } from 'react-redux';
import csv from 'papaparse';

import { getRawContent } from '@plone-collective/volto-datatable-tutorial/actions';

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
```

This HOC now gets the data from the `Redux` store using the logic and code we've
previously used.
It then injects it as a new property onto the original wrapped component.

A HOC is a simple function that gets a component and returns another
component.  For a Python developer, decorators are a very similar concept.
Take note that React component names must be referenced as `PascalCase` in JSX code.

Now the view component is simple, neat, and focused.

Now write the `src/hocs/index.js` file where you export the new HOC.

```jsx
import withFileData from './withFileData';
export { withFileData };
```

Back to the `src/DataTable/DataTable.jsx`, it becomes:

```jsx
import React from 'react';
import { Table } from 'semantic-ui-react';
import { withFileData } from '@plone-collective/volto-datatable-tutorial/hocs';

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
```
