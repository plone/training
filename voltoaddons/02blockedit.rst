Improve the block edit. We're now showing an object picker.

.. code-block:: jsx

    import React from 'react';
    import { Segment, Form } from 'semantic-ui-react';
    import { SidebarPortal, Field } from '@plone/volto/components';
    import DataTableView from './DataTableView';

    const DataTableEdit = (props) => {
      const { selected, onChangeBlock, block, data } = props;
      return (
        <div className="datatable-edit">
          <SidebarPortal selected={selected}>
            <Segment.Group raised>
              <header className="header pulled">
                <h2>Data table</h2>
              </header>
            </Segment.Group>
          </SidebarPortal>
          {data.url ? <DataTableView /> : ''}
          {!data.url ? (
            <div className="no-value">
              <Form>
                <Field
                  id="url"
                  widget="pick_object"
                  title="Pick a file"
                  value={data.url}
                  onChange={(id, value) =>
                    onChangeBlock(block, { ...data, [id]: value })
                  }
                />
              </Form>
            </div>
          ) : (
            ''
          )}
        </div>
      );
    };

    export default DataTableEdit;

Add the following ``datatable.less`` file:

.. code-block:: less

    @type: 'extra';
    @element: 'custom';

    @import (multiple) '../../theme.config';

    .datatable-edit {
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

And include it somewhere where it would be loaded, for example
DataTableView.jsx.

.. code-block:: jsx

    import './datatable.less';
