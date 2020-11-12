===================
Basic working block
===================

Let's improve the block edit. We'll detect when the block has just been added
and provide the user with a way to immediately pick a file, from the block's
main area.

.. code-block:: jsx

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
                    widget="pick_object"
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


Add the following ``datatable-edit.less`` file:

.. code-block:: less

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
        margin: 0em auto;
      }
    }

Notice that by importing ``'../../theme.config'`` we're able to have access to
Volto's LESS variables.

For the view, we'll fetch the data directly from Plone and bring it to the
client browser.

Note: there are other possible approaches to this problem, including
transforming the block data on outbound with a block serializer transformer, to
automatically insert CSV file in the block and remove it on inbound
(deserialization). By having it available separately we make it easier to
reference the same data from multiple blocks.

.. code-block:: jsx

    import React from 'react';
    import { useDispatch, useSelector } from 'react-redux';
    import { getRawContent } from '@plone/datatable-tutorial/actions';

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


We'll need to write a new action/reducer pair to fetch the data.

Create action type in the ``constants.js`` file:

.. code-block:: jsx

    export const GET_RAW_CONTENT = 'GET_RAW_CONTENT';

Create the ``rawcontent.js`` action module:

.. code-block:: jsx

    import { GET_RAW_CONTENT } from '@plone/datatable-tutorial/constants';

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

Then create the ``reducers/rawdata.js`` module:

.. code-block:: jsx

    import { GET_RAW_CONTENT } from '@plone/datatable-tutorial/constants';

    export default function rawdata(state = {}, action = {}) {
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

Finally, register the addon reducer. In ``src/index.js``'s default export:

.. code-block:: jsx

    import { rawdata } from './reducers';

    ...

    config.addonReducers.rawdata = rawdata;

Note: make sure to change the project's src/config.js to import default
addonReducers and them export them.
