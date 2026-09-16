---
myst:
  html_meta:
    "description": "Simple block architecture"
    "property=og:description": "Simple block architecture"
    "property=og:title": "Create a custom block"
    "keywords": "Plone, Volto, block, add-on"
---

(volto-custom-block-label)=

# Create a custom block 

````{card}

In this part you will create a new block for the Volto frontend.
````

````{card}

Check out `mastering-plone-project` at tag `sponsors`:

```shell
git checkout sponsors
```

The code at the end of the chapter:

```shell
git checkout block
```

More info in {doc}`code`
````

We want to provide some information for speakers of the conference:
Which topics are possible?
What do I have to consider for speaking at an online conference?
A FAQ section would come in handy.
This could be done by creating a block type that offers a form for question and answer pairs and displays an accordion.

```{figure} _static/volto_addon_accordion_display.png
:alt: Volto add-on volto-accordion-block
```

```{figure} _static/volto_addon_accordion_sidebar.png
:alt: Editing Volto add-on volto-accordion-block
```

## The block schema

Let's first define the schema for the data that will be stored for this block.
We want to store a list of question and answer pairs, like this:

```json
[
  {
    "question": "What is Plone?",
    "answer": "Plone is a CMS..."
  },
  {
    "question": "Where is the conference?",
    "answer": "Maastricht"
  }
]
```

Create a folder {file}`src/frontend/volto-ploneconf-site/src/components/Blocks/FAQ` containing {file}`schema.js`.

```{code-block} jsx
:linenos:

export const QuestionAnswerPairSchema = {
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
      title: 'Question',
      type: 'string',
      widget: 'textarea',
    },
    answer: {
      title: 'Answer',
      type: 'string',
      widget: 'richtext',
    },
  },
  required: ['question', 'answer'],
};

export const FAQBlockSchema = {
  title: 'FAQ',
  fieldsets: [
    {
      id: 'default',
      title: 'Default',
      fields: ['faqs'],
    },
  ],
  properties: {
    faqs: {
      title: 'Question and Answers',
      type: 'array',
      widget: 'object_list',
      schema: QuestionAnswerPairSchema,
    },
  },
  required: [],
};
```

`QuestionAnswerPairSchema` is the schema for a single question-answer pair, and `FAQBlockSchema` is the schema for the entire block, with a list of those pairs.

## Block view

We need a view for the block.
The BlockView is a simple function component that displays a FAQ component with the data stored in the block.

Create the file {file}`src/frontend/volto-ploneconf-site/src/components/Blocks/FAQ/BlockView.jsx`.

```{code-block} jsx
:linenos:

import FAQ from './FAQ';

const View = ({ data }) => {
  return (
    <div className="block faq">
      <FAQ data={data} />
    </div>
  );
};

export default View;
```

We outsource the FAQ component to file {file}`src/packages/volto-ploneconf-site/src/components/Blocks/FAQ/FAQ.jsx` and make heavy use of Semantic UI components, especially the accordion with its behavior of expanding and collapsing.

```{code-block} jsx
:linenos:

import { useState } from 'react';

import Icon from '@plone/volto/components/theme/Icon/Icon';
import rightSVG from '@plone/volto/icons/right-key.svg';
import downSVG from '@plone/volto/icons/down-key.svg';
import AnimateHeight from 'react-animate-height';

import { Accordion, Grid, Divider, Header } from 'semantic-ui-react';

const FAQ = ({ data }) => {
  const [activeIndex, setActiveIndex] = useState(new Set());

  return data.faqs ? (
    <>
      <Divider section />
      {data.faqs.map(({ '@id': id, question, answer }) => (
        <Accordion key={id} fluid exclusive={false}>
          <Accordion.Title
            index={id}
            className="stretched row"
            active={activeIndex.has(id)}
            onClick={() => {
              const newSet = new Set(activeIndex);
              activeIndex.has(id) ? newSet.delete(id) : newSet.add(id);
              setActiveIndex(newSet);
            }}
          >
            <Grid>
              <Grid.Row>
                <Grid.Column width="1">
                  {activeIndex.has(id) ? (
                    <Icon name={downSVG} size="20px" />
                  ) : (
                    <Icon name={rightSVG} size="20px" />
                  )}
                </Grid.Column>
                <Grid.Column width="11">
                  <Header as="h3">{question}</Header>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Accordion.Title>
          <div>
            <Accordion.Content
              className="stretched row"
              active={activeIndex.has(id)}
            >
              <Grid>
                <Grid.Row>
                  <Grid.Column width="1"></Grid.Column>
                  <Grid.Column width="11">
                    <div>
                      <AnimateHeight
                        key={id}
                        duration={300}
                        height={activeIndex.has(id) ? 'auto' : 0}
                      >
                        <div
                          dangerouslySetInnerHTML={{
                            __html: answer.data,
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
```
````

## Edit form

We also need an edit form.
The edit form also uses the same `FAQ` component to show the current data, along with the `FAQSidebar` with the form for editing the data.

Create the file {file}`frontend/packages/volto-ploneconf-site/src/components/Block/FAQ/BlockEdit.jsx`.

```{code-block} jsx
:linenos:

import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';

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
```

```{tip}
Everything inside the `SidebarPortal` is rendered in the sidebar instead of inside the block.
```

We outsource the edit form to {file}`FAQSidebar.jsx` which displays a form using the block schema.
The _onChangeBlock_ prop is a function we can use to store changes to the block data.

```{code-block} jsx
:linenos:

import { FAQBlockSchema } from './schema';
import InlineForm from '@plone/volto/components/manage/Form/InlineForm';

const FAQSidebar = ({ data, block, onChangeBlock }) => {
  return (
    <InlineForm
      schema={FAQBlockSchema}
      title={FAQBlockSchema.title}
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
```

## Register the block in Volto config

What's left to do?
You created a block type with view and edit form and even a nice widget for the editor to fill in questions and answers. 
We still need to register the block type in the Volto configuration so that Volto knows it exists.

Add the file {file}`frontend/volto-ploneconf-site/src/config/blocks.ts`.

```{code-block} tsx
:linenos:

import icon from '@plone/volto/icons/list-bullet.svg';

import FAQBlockEdit from '../components/Blocks/FAQ/BlockEdit';
import FAQBlockView from '../components/Blocks/FAQ/BlockView';
import { FAQBlockSchema } from '../components/Blocks/FAQ/schema';

import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  config.blocks.blocksConfig.faq = {
    id: 'faq',
    title: 'FAQ',
    blockSchema: FAQBlockSchema,
    edit: FAQBlockEdit,
    view: FAQBlockView,
    icon: icon,
    group: 'text',
    restricted: false,
    mostUsed: false,
    sidebarTab: 1,
  };
  return config;
}
```

Update {file}`frontend/src/volto-ploneconf-site/src/index.ts` to include the block configuration.

```{code-block} tsx
:linenos:
:emphasize-lines: 3, 7

import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';

function applyConfig(config: ConfigType) {
  installSettings(config);
  installBlocks(config);

  return config;
}

export default applyConfig;
```

Restart the frontend, and now the FAQ block should be available.

```{figure} _static/volto_addon_accordion_add.png
:alt: "@rohberg/volto-accordion-block"
```

```{seealso}

[@rohberg/volto-accordion-block](https://www.npmjs.com/package/@rohberg/volto-accordion-block) is a released add-on similar to the one from this chapter.
```
