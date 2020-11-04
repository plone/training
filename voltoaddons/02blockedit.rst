Improve the block edit. We're now showing an object picker.

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
        <div className="datatable-edit">
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
