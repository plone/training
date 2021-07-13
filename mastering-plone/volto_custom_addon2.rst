.. _volto_custom_addon2-label:

Extending Volto With a FAQ Block Type
=====================================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  Creating a new block type


We want to provide some information for speakers of the conference: Which topics are possible? What do I have to consider speaking at an online conference? FAQ section would come in handy. This could be done by creating a block type that offers a form for question and answer pairs and displays an accordion.

Let's start with our fresh add-on we created in the last chapter :doc:`volto_custom_addon`.


.. figure:: _static/volto_addon_accordion_display.png
    :alt: Volto add-on volto-accordion-block

.. figure:: _static/volto_addon_accordion_sidebar.png
    :alt: Editing Volto add-on volto-accordion-block



We need a view and an edit form for the block. Create a :file:`src/FAQ/BlockView.jsx` :file:`src/FAQ/BlockEdit.jsx`.

The BlockView is a simple function component that displays a FAQ component with the data stored on the block.

.. code-block:: jsx
    :linenos:

    import React from 'react';
    import FAQ from './FAQ';

    const View = ({ data }) => {
      return (
        <div className="block faq">
          <FAQ data={data} />
        </div>
      );
    };

    export default View;

We outsource the FAQ component to file :file:`srch/FAQ/FAQ.jsx` and make heavy use of Semantic UI components especially of an accordion with its respective behavior of expanding and collapsing.

.. code-block:: jsx
    :linenos:

    const FAQ = ({ data }) => {
      const [activeIndex, setActiveIndex] = useState(new Set());

      return data.faq_list?.faqs ? (
        {data.faq_list.faqs.map((id_qa) => (

We primarily loop over the accordion elements and we remember the extended (not collapsed)  elements.

.. admonition:: Complete code of the ``FAQ`` component
  :class: toggle

  .. code-block:: jsx
    :linenos:

    import React, { useState } from 'react';

    import { Icon } from '@plone/volto/components';
    import rightSVG from '@plone/volto/icons/right-key.svg';
    import downSVG from '@plone/volto/icons/down-key.svg';
    import AnimateHeight from 'react-animate-height';

    import { Accordion, Grid, Divider, Header } from 'semantic-ui-react';

    const FAQ = ({ data }) => {
      const [activeIndex, setActiveIndex] = useState(new Set());

      return data.faq_list?.faqs ? (
        <>
          <Divider section />
          {data.faq_list.faqs.map((id_qa) => (
            <Accordion key={id_qa} fluid exclusive={false}>
              <Accordion.Title
                index={id_qa}
                className="stretched row"
                active={activeIndex.has(id_qa)}
                onClick={() => {
                  const newSet = new Set(activeIndex);
                  activeIndex.has(id_qa) ? newSet.delete(id_qa) : newSet.add(id_qa);
                  setActiveIndex(newSet);
                }}
              >
                <Grid>
                  <Grid.Row>
                    <Grid.Column width="1">
                      {activeIndex.has(id_qa) ? (
                        <Icon name={downSVG} size="20px" />
                      ) : (
                        <Icon name={rightSVG} size="20px" />
                      )}
                    </Grid.Column>
                    <Grid.Column width="11">
                      <Header as="h3">{data.faq_list.faqs_layout[id_qa][0]}</Header>
                    </Grid.Column>
                  </Grid.Row>
                </Grid>
              </Accordion.Title>
              <div>
                <Accordion.Content
                  className="stretched row"
                  active={activeIndex.has(id_qa)}
                >
                  <Grid>
                    <Grid.Row>
                      <Grid.Column width="1"></Grid.Column>
                      <Grid.Column width="11">
                        <div>
                          <AnimateHeight
                            key={id_qa}
                            duration={300}
                            height={activeIndex.has(id_qa) ? 'auto' : 0}
                          >
                            <div
                              dangerouslySetInnerHTML={{
                                __html: data.faq_list.faqs_layout[id_qa][1].data,
                              }}
                            />
                          </AnimateHeight>
                        </div>
                      </Grid.Column>
                    </Grid.Row>
                  </Grid>
                </Accordion.Content>
              </div>
              <Divider section />
            </Accordion>
          ))}
        </>
      ) : (
        ''
      );
    };

    export default FAQ;

Let's see how the data is stored on the block. Open your BlockEdit. See the helper component ``SidebarPortal``. Everything inside is displayed in the Sidebar.

.. code-block:: jsx
    :linenos:

    import React from 'react';
    import { SidebarPortal } from '@plone/volto/components';

    import FAQSidebar from './FAQSidebar';
    import FAQ from './FAQ';

    const Edit = ({ data, onChangeBlock, block, selected }) => {
      return (
        <div className={'block faq'}>
          <SidebarPortal selected={selected}>
            <FAQSidebar data={data} block={block} onChangeBlock={onChangeBlock} />
          </SidebarPortal>

          <FAQ data={data} />
        </div>
      );
    };

    export default Edit;

We outsource the edit form in a file :file:`FAQSidebar.jsx` which displays the form according a schema of question and answers. The *onChangeBlock* event handler is inherited, it stores the value on the block.

.. code-block:: jsx
    :linenos:

    import React from 'react';
    import { FAQSchema } from './schema';
    import InlineForm from '@plone/volto/components/manage/Form/InlineForm';

    const FAQSidebar = ({ data, block, onChangeBlock }) => {
      return (
        <InlineForm
          schema={FAQSchema}
          title={FAQSchema.title}
          onChangeField={(id, value) => {
            onChangeBlock(block, {
              ...data,
              [id]: value,
            });
          }}
          formData={data}
        />
      );
    };

    export default FAQSidebar;

We define the schema in :file:`schema.js`.

.. code-block:: jsx
  :linenos:
  :emphasize-lines: 11-14

  export const FAQSchema = {
    title: 'FAQ',
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['faq_list'],
      },
    ],
    properties: {
      faq_list: {
        title: 'Question and Answers',
        type: 'faqlist',
      },
    },
    required: [],
  };

The field *faq_list* has a type *'faqlist'*. This has to be registered as a *widget* in :file:`src/config.js`. This configuration is the central place where your add-on can customize the hosting Volto app. It's the place where we later also register our new block type with information about its view and edit form.

.. code-block:: jsx
  :linenos:

  import FAQListEditWidget from './FAQ/FAQListEditWidget';

  export default function applyConfig(config) {
    config.widgets.type.faqlist = FAQListEditWidget;

    return config;
  }

Now we will code the important part of the whole block type: the widget ``FAQListEditWidget``.
We need a form that consists of a list of existing questions and answers.
The text should be editable.
Additional pairs of questions and answers should be addable.
The next step will be to let the list be drag-and-droppable to reorder the items.
Also an item should be deletable.
That's a lot.
Let's start with the list of fields displaying the existing values.


Create a :file:`FAQListEditWidget.jsx`.

.. code-block:: jsx
  :linenos:

  import { Form as VoltoForm } from '@plone/volto/components';

  const FAQListEditWidget = (props) => {
    const { value = {}, id, onChange } = props;
    // id is the field name: faq_list
    // value is the form data (see example in schema.js)

    // qaList: array of [id_question, [question, answer]]
    const qaList = (value.faqs || []).map((key) => [key, value.faqs_layout[key]]);

    return (
      // loop over question answer pairs *qaList*
        <VoltoForm
          onSubmit={({ question, answer }) => {
            onSubmitQAPair(childId, question, answer);
          }}
          formData={{
            question: value.faqs_layout[childId][0],
            answer: value.faqs_layout[childId][1],
          }}
          schema={QuestionAnswerPairSchema(
            props.intl.formatMessage(messages.question),
            props.intl.formatMessage(messages.answer),
          )}
        />

You see the Volto `Form` component with its onSubmit event, the form data and the schema to be used.

.. admonition:: Complete code of the ``FAQListEditWidget`` component
  :class: toggle

  .. code-block:: jsx
    :linenos:
    :emphasize-lines: 113-125

    import React from 'react';
    import { defineMessages, injectIntl } from 'react-intl';
    import { v4 as uuid } from 'uuid';
    import { omit, without } from 'lodash';
    import move from 'lodash-move';
    import { Icon, FormFieldWrapper } from '@plone/volto/components';
    import { Form as VoltoForm } from '@plone/volto/components';
    import { DragDropList } from '@eeacms/volto-blocks-form/components';

    import dragSVG from '@plone/volto/icons/drag.svg';
    import trashSVG from '@plone/volto/icons/delete.svg';
    import plusSVG from '@plone/volto/icons/circle-plus.svg';

    import { QuestionAnswerPairSchema } from './schema.js';

    const messages = defineMessages({
      question: {
        id: 'Question',
        defaultMessage: 'Question',
      },
      answer: {
        id: 'Answer',
        defaultMessage: 'Answer',
      },
      add: {
        id: 'add',
        defaultMessage: 'add',
      },
    });

    export function moveQuestionAnswerPair(formData, source, destination) {
      return {
        ...formData,
        faqs: move(formData.faqs, source, destination),
      };
    }

    const empty = () => {
      return [uuid(), ['', {}]];
    };

    const FAQListEditWidget = (props) => {
      const { value = {}, id, onChange } = props;
      // id is the field name: faq_list
      // value is the form data (see example in schema.js)

      const onSubmitQAPair = (id_qa, question, answer) => {
        onChange(id, {
          ...value,
          faqs_layout: {
            ...(value.faqs_layout || {}),
            [id_qa]: [question, answer],
          },
        });
      };

      const addQA = () => {
        const [newId, newData] = empty();
        onChange(id, {
          ...value,
          faqs: [...(value.faqs || []), newId],
          faqs_layout: {
            ...(value.faqs_layout || {}),
            [newId]: newData,
          },
        });
      };

      // qaList array of [id_question, [question, answer]]
      const qaList = (value.faqs || []).map((key) => [key, value.faqs_layout[key]]);

      const showAdd = true;
      return (
        <FormFieldWrapper
          {...props}
          draggable={false}
          columns={1}
          className="drag-drop-list-widget"
        >
          <div className="columns-area">
            <DragDropList
              childList={qaList}
              onMoveItem={(result) => {
                const { source, destination } = result;
                if (!destination) {
                  return;
                }
                const newFormData = moveQuestionAnswerPair(
                  value,
                  source.index,
                  destination.index,
                );
                onChange(id, newFormData);
                return true;
              }}
            >
              {(dragProps) => {
                const { childId, draginfo } = dragProps;
                return (
                  <div ref={draginfo.innerRef} {...draginfo.draggableProps}>
                    <div style={{ position: 'relative' }}>
                      <div
                        style={{
                          visibility: 'visible',
                          display: 'inline-block',
                        }}
                        {...draginfo.dragHandleProps}
                        className="drag handle wrapper"
                      >
                        <Icon name={dragSVG} size="18px" />
                      </div>
                      <div className="column-area">
                        <VoltoForm
                          onSubmit={({ question, answer }) => {
                            onSubmitQAPair(childId, question, answer);
                          }}
                          formData={{
                            question: value.faqs_layout[childId][0],
                            answer: value.faqs_layout[childId][1],
                          }}
                          schema={QuestionAnswerPairSchema(
                            props.intl.formatMessage(messages.question),
                            props.intl.formatMessage(messages.answer),
                          )}
                        />
                        {qaList?.length > 1 ? (
                          <button
                            onClick={() => {
                              onChange(id, {
                                faqs: without(value.faqs, childId),
                                faqs_layout: omit(value.faqs_layout, [childId]),
                              });
                            }}
                          >
                            <Icon name={trashSVG} size="18px" />
                          </button>
                        ) : (
                          ''
                        )}
                      </div>
                    </div>
                  </div>
                );
              }}
            </DragDropList>
            {showAdd ? (
              <button
                aria-label={props.intl.formatMessage(messages.add)}
                onClick={addQA}
              >
                <Icon name={plusSVG} size="18px" />
              </button>
            ) : (
              ''
            )}
          </div>
        </FormFieldWrapper>
      );
    };

    export default injectIntl(FAQListEditWidget);

The form is fructified by the schema QuestionAnswerPairSchema. It's simple, just a string field with a textarea widget for the question and a such for the answer, but with a richtext widget to have some editing and styling tools available.

:file:`src/FAQ/schema.js`

.. code-block:: jsx
  :linenos:
  :emphasize-lines: 12,17

  export const QuestionAnswerPairSchema = (title_question, title_answer) => {
    return {
      title: 'Question and Answer Pair',
      fieldsets: [
        {
          id: 'default',
          title: 'QA pair',
          fields: ['question', 'answer'],
        },
      ],
      properties: {
        question: {
          title: title_question,
          type: 'string',
          widget: 'textarea',
        },
        answer: {
          title: title_answer,
          type: 'string',
          widget: 'richtext',
        },
      },
      required: ['question', 'answer'],
    };
  };

What's left to do?
You created a block type with view and edit form and even a nice widget for the editor to fill in questions and answers. Register the block type and you are good to start your app and create an FAQ for the conference speakers.

Go to :file:`config.js` and register your block type.

.. code-block:: jsx
  :linenos:
  :emphasize-lines: 8-22

  import icon from '@plone/volto/icons/list-bullet.svg';

  import FAQBlockEdit from './FAQ/BlockEdit';
  import FAQBlockView from './FAQ/BlockView';
  import FAQListEditWidget from './FAQ/FAQListEditWidget';

  export default function applyConfig(config) {
    config.blocks.blocksConfig.faq_viewer = {
      id: 'faq_viewer',
      title: 'FAQ',
      edit: FAQBlockEdit,
      view: FAQBlockView,
      icon: icon,
      group: 'text',
      restricted: false,
      mostUsed: false,
      sidebarTab: 1,
      security: {
        addPermission: [],
        view: [],
      },
    };

    config.widgets.type.faqlist = FAQListEditWidget;

    return config;
  }

As we now apply our configuration of the new block type, the app is enriched with an accordion block.

:file:`index.js`

.. code-block:: jsx
  :linenos:

  import applyConfig from './config';

  export default applyConfig;


Run

.. code-block:: bash

  yarn start

You see

.. code-block:: text

  Module not found: Can't resolve '@eeacms/volto-blocks-form/components'

Why is this? We want the accordion to be reorderable and use the `DragDropList` component of another add-on: `@eeacms/volto-blocks-form`. Add it to the dependencies of your add-on.

:file:`package.json`

.. code-block:: json

  "dependencies": {
    "@eeacms/volto-blocks-form": "@eeacms/volto-blocks-form"
  },

The following might change the next time:

Add to your **apps** :file:`package.json`:

.. code-block:: json

  "addons": ["@greenthumb/volto-custom-addon", "@eeacms/volto-blocks-form"],

Compile and start your projects app:

.. code-block:: bash

  yarn
  yarn start

.. figure:: _static/volto_addon_accordion_add.png
  :alt: @rohberg/volto-accordion-block

See the complete add-on code @rohberg/volto-accordion-block [1]_



Save your work to Github
---------------------------


Your add-on is ready to use. As by now your repository is on Github. As long as it is published, you can share it with others.

A Volto project uses this add-on via 'mrs.developer' [2]_

Install mrs.developer to let the project know about the *source* of your add-on.

..  code-block:: bash

    yarn add mrs-developer -WD

The configuration file :file:`mrs.developer.json` instructs mrs.developer from where it has to pull the package. So, create mrs.developer.json and add:

..  code-block:: bash

    {
        "greenthumb-volto-custom-addon": {
            "package": "@greenthumb/volto-custom-addon",
            "url": "git@github.com:greenthumb/volto-custom-addon.git",
            "path": "src"
        }
    }

Run

..  code-block:: bash

    yarn develop

An official release is done on npm. Switch to section :ref:`Release a Volto add-on <volto_custom_addon-final-label>`.


Footnotes
----------------

.. [1] `Volto accordion block <https://www.npmjs.com/package/@rohberg/volto-accordion-block>`_
    Started as an example for the training it is ready to use for creating a questions and answer sections.

.. [2] `mrs.developer <https://www.npmjs.com/package/mrs-developer>`_ Pull a package from git and set it up as a dependency for the current project codebase.
