---
myst:
  html_meta:
    "description": "Volto add-ons development training module 2, add-ons block edit"
    "property=og:description": "Volto add-ons development training"
    "property=og:title": "Volto add-ons development"
    "keywords": "Volto"
---

# Basic working block

Let's improve the block edit. We'll detect when the block has just been added
and provide the user with a way to immediately pick a file, from the block's
main area.


## Style the block with LESS files

Add the following `src/DataTable/datatable-edit.less` file:

```{code-block} less
:force: true

@type: 'extra';
@element: 'custom';

@import (multiple) '../../theme.config';

.dataTable-edit {
  background: @offWhite;

  .form {
    display: flex;
    max-width: 26em !important;
    min-height: 10em;
    flex-direction: column;
    justify-content: center;
    margin: 0 auto;
  }
}
```

Notice that by importing `'../../theme.config'`, we're able to have access to
Volto's (and, by extension, all Semantic UI) LESS variables.

## User-friendly block edit behavior

Change the `src/DataTable/DataTableEdit.jsx` file to:

```jsx
import React from 'react';
import { Segment, Form } from 'semantic-ui-react';
import { SidebarPortal, Field, Icon } from '@plone/volto/components';
import tableSVG from '@plone/volto/icons/table.svg';

import DataTableView from './DataTableView';

import './datatable-edit.less';

const DataTableEdit = (props) => {
  const { selected, onChangeBlock, block, data } = props;

  return (
    <div className="dataTable-edit">
      <SidebarPortal selected={selected}>
        <Segment.Group raised>
          <header className="header pulled">
            <h2>Data table</h2>
          </header>
          {!data.file_path?.length ? (
            <>
              <Segment className="sidebar-metadata-container" secondary>
                No file selected
                <Icon name={tableSVG} size="100px" color="#b8c6c8" />
              </Segment>
            </>
          ) : (
            <Form>
              <Field
                id="file_path"
                widget="object_browser"
                mode="link"
                title="Data file"
                value={data.file_path || []}
                onChange={(id, value) => {
                  onChangeBlock(block, {
                    ...data,
                    [id]: value,
                  });
                }}
              />
            </Form>
          )}
        </Segment.Group>
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

In the sidebar area, if we don't have a file picked, we show a placeholder icon.
Otherwise we show the field to edit the picked file.
In the main block area, if we don't have a file picked, we show the file input.
Otherwise we show the `View` component.

## Fetching data for the block

For the view, we'll fetch the data directly from Plone, and bring it to the
client browser. We want data to come from the `@@download`
view of that file, something which is not treated by Volto's "get content"
machinery, so we'll need to write our flavor of data fetching.

```{note}
There are other possible approaches to this problem, including transforming
the outbound block data with a block serializer transformer to
automatically insert a CSV file in the block, then remove it inbound
(deserialization). By having it available separately, we make it easier to
reference the same data from multiple blocks, and of course keep things
simple for this training.

But if you want to have the content of the table rendered with the SSR
mechanism, then you'll have to avoid the extra data fetch and serialize the
table data together with the main block data using plone.restapi backend-based
block transformers.

This is because there would be two serialized data fetches. The first one is
for the main content, which would return the blocks, then the blocks are
rendered and, as a result of that rendering, the second network fetch would be
called from one of the blocks as an async request.
```

```jsx
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getRawContent } from '@plone-collective/volto-datatable-tutorial/actions';

const DataTableView = (props) => {
  const {
    data: { file_path },
  } = props;

  const id = file_path?.[0]?.['@id'];
  const path = id ? `${id}/@@download` : null;

  const dispatch = useDispatch();
  const request = useSelector((state) => state.rawdata?.[path]);

  const content = request?.data;
  const hasData = !!content;

  React.useEffect(() => {
    if (path && !hasData) dispatch(getRawContent(path));
  }, [dispatch, path, hasData]);

  return <div>Table here...</div>;
};

export default DataTableView;
```

We'll need to write a new action/reducer pair to fetch the data.

Create action type in the `src/constants.js` file:

```jsx
export const GET_RAW_CONTENT = 'GET_RAW_CONTENT';
```

Create the `src/actions.js` action module:

```jsx
import { GET_RAW_CONTENT } from './constants';

export function getRawContent(url, headers = {}) {
  return {
    type: GET_RAW_CONTENT,
    request: {
      op: 'get',
      path: url,
      headers,
    },
    url,
  };
}
```

Then create the `src/reducers.js` module:

```jsx
import { GET_RAW_CONTENT } from './constants';

export function rawdata(state = {}, action = {}) {
  let { result, url } = action;

  switch (action.type) {
    case `${GET_RAW_CONTENT}_PENDING`:
      return {
        ...state,
        [url]: {
          ...state[url],
          loading: true,
          loaded: false,
          error: undefined,
        },
      };
    case `${GET_RAW_CONTENT}_SUCCESS`:
      return {
        ...state,
        [url]: {
          ...state[url],
          loading: false,
          loaded: true,
          error: undefined,
          data: result,
        },
      };
    case `${GET_RAW_CONTENT}_FAIL`:
      return {
        ...state,
        [url]: {
          ...state[url],
          loading: false,
          loaded: false,
          error: action.error,
        },
      };
    default:
      break;
  }
  return state;
}
```

The reducer code looks scary, but it shouldn't be. To understand it, you need
to know:

- In Volto, all actions that have a `request` field are treated as network
  requests, and they will be processed by the [API middleware](https://github.com/plone/volto/blob/main/src/middleware/api.js).
- That middleware will then trigger several new actions, derived from the main
  function and prefixed with its name, either `PENDING`, `SUCCESS`, or `FAIL`.
- For each of these new actions, we will reduce the state of the store to
  something that makes sense. First, we want to store different
  information for each requested URL. Then we want to store information
  according to the triggered action, either loading state, error information, or the
  final result.
- In all cases, we're using object spreads as a pattern to quickly redefine some values inside the make store object.

Finally, register the add-on reducer. In `src/index.js`'s default export:

```jsx
//...
import { rawdata } from './reducers';
//...

export default (config) => {
  config.addonReducers.rawdata = rawdata;
  //...
  return config;
}
```
