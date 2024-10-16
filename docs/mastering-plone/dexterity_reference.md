---
myst:
  html_meta:
    "description": "Fields and widgets"
    "property=og:description": "Fields and widgets"
    "property=og:title": "Content types: Reference"
    "keywords": "field, widget, schema"
---

(dexterity-reference-label)=

# Content types: Reference

This chapter documents common fields, widgets, directives that you can use with content types.
Content types are often called dexterity types which refers to the rework of the content type concept by dexterity and abandoning the Archetypes system.


## Fields included in Plone

This is a schema with examples for all field-types that are shipped with Plone by default. They are arranged in fieldsets:

Text, boolean, email

: Textline, RichText, Boolean, Email, URI

Number fields

: Integer, Float

Date and time fields

: Datetime, Date

Choice and Multiple Choice fields

: Choice, List, Tuple, Set

Relation fields

: Relationchoice, Relationlist

File fields

: File, Image

```{seealso}
See the code in [example.contenttype **branch training**](https://github.com/collective/example.contenttype/blob/training-mastering-plone-development/src/example/contenttype/example.py)
```

```{code-block} python
:linenos:

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container

from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.schema import Email

from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.supermodel.directives import primary
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IExample(model.Schema):
    """Dexterity-Schema with common field-types."""

    # fieldset(
    #     "default",
    #     label="Text, Boolean, Email",
    #     fields=(
    #         "title",
    #         "description",
    #         "richtext_field",
    #         "bool_field",
    #         "email_field",
    #         "uri_field",
    #     ),
    # )

    fieldset(
        "numberfields",
        label="Number",
        fields=("int_field", "float_field"),
    )

    fieldset(
        "datetimefields",
        label="Date and time",
        fields=(
            "datetime_field",
            "date_field",
        ),
    )

    fieldset(
        "choicefields",
        label="Choice",
        fields=(
            "choice_field",
            "list_field",
            "tuple_field",
            "set_field",
        ),
    )

    fieldset(
        "relationfields_volto",
        label="Relation fields – Volto",
        fields=(
            "relationchoice_field_named_staticcatalogvocabulary",
            "relationlist_field_named_staticcatalogvocabulary",
        ),
    )

    fieldset(
        "filefields",
        label="File",
        fields=("file_field", "image_field"),
    )

    # Default fields
    primary("title")
    title = schema.TextLine(
        title="Primary Field (Textline)",
        description="zope.schema.TextLine",
        required=True,
    )

    description = schema.TextLine(
        title="Description (Textline)",
        description="zope.schema.TextLine",
        required=False,
    )

    # text_field = schema.Text(
    #     title="Text Field",
    #     description="zope.schema.Text",
    #     required=False,
    #     missing_value="",
    #     default="",
    # )

    # textline_field = schema.TextLine(
    #     title="Textline field",
    #     description="A simple input field (zope.schema.TextLine)",
    #     required=False,
    # )

    richtext_field = RichText(
        title="RichText field",
        description="This uses a richtext editor. (plone.app.textfield.RichText)",
        max_length=2000,
        required=False,
    )

    bool_field = schema.Bool(
        title="Boolean field",
        description="zope.schema.Bool",
        required=False,
    )

    email_field = Email(
        title="Email field",
        description="A simple input field for a email (plone.schema.email.Email)",
        required=False,
    )

    uri_field = schema.URI(
        title="URI field",
        description="A simple input field for a URLs (zope.schema.URI)",
        required=False,
    )

    # Choice fields
    choice_field = schema.Choice(
        title="Choice field",
        description="zope.schema.Choice",
        values=["One", "Two", "Three"],
        required=False,
    )

    list_field = schema.List(
        title="List field",
        description="zope.schema.List",
        value_type=schema.Choice(
            values=["Beginner", "Advanced", "Professional"],
        ),
        required=False,
        missing_value=[],
        default=[],
    )

    tuple_field = schema.Tuple(
        title="Tuple field",
        description="zope.schema.Tuple",
        value_type=schema.Choice(
            values=["Beginner", "Advanced", "Professional"],
        ),
        required=False,
        missing_value=(),
        default=(),
    )

    set_field = schema.Set(
        title="Set field",
        description="zope.schema.Set",
        value_type=schema.Choice(
            values=["Beginner", "Advanced", "Professional"],
        ),
        required=False,
        missing_value=set(),
        default=set(),
    )

    # File and image fields
    image_field = NamedBlobImage(
        title="Image field",
        description="A upload field for images (plone.namedfile.field.NamedBlobImage)",
        required=False,
    )

    file_field = NamedBlobFile(
        title="File field",
        description="A upload field for files (plone.namedfile.field.NamedBlobFile)",
        required=False,
    )

    # Date and Time fields
    datetime_field = schema.Datetime(
        title="Datetime field",
        description="Uses a date and time picker (zope.schema.Datetime)",
        required=False,
    )

    date_field = schema.Date(
        title="Date field",
        description="Uses a date picker (zope.schema.Date)",
        required=False,
    )

    """Relation fields like Volto likes it

    RelationChoice and RelationList with named StaticCatalogVocabulary

    StaticCatalogVocabulary registered with same name as field/relation.
    This allowes Volto relations control panel to restrict potential targets.
    """

    relationchoice_field_named_staticcatalogvocabulary = RelationChoice(
        title="RelationChoice – named StaticCatalogVocabulary – Select widget",
        description="field/relation: relationchoice_field_named_staticcatalogvocabulary",
        vocabulary="relationchoice_field_named_staticcatalogvocabulary",
        required=False,
    )
    directives.widget(
        "relationchoice_field_named_staticcatalogvocabulary",
        frontendOptions={
            "widget": "select",
        },
    )

    relationlist_field_named_staticcatalogvocabulary = RelationList(
        title="RelationList – named StaticCatalogVocabulary – Select widget",
        description="field/relation: relationlist_field_named_staticcatalogvocabulary",
        value_type=RelationChoice(
            vocabulary="relationlist_field_named_staticcatalogvocabulary",
        ),
        required=False,
        default=[],
        missing_value=[],
    )
    directives.widget(
        "relationlist_field_named_staticcatalogvocabulary",
        frontendOptions={
            "widget": "select",
        },
    )

    # Number fields
    int_field = schema.Int(
        title="Integer Field (e.g. 12)",
        description="zope.schema.Int",
        required=False,
    )

    float_field = schema.Float(
        title="Float field, e.g. 12.7",
        description="zope.schema.Float",
        required=False,
    )


@implementer(IExample)
class Example(Container):
    """Example instance class"""
```


## How fields look like

This is how these fields look like when editing content in Volto:

```{figure} _static/dexterity/dex1.png
:alt: Default fields

Text and boolean fields
```

```{figure} _static/dexterity/dex_number.png
:alt: Number fields

Number fields
```

```{figure} _static/dexterity/dex2.png
:alt: Date and time fields

Date and time fields
```

```{figure} _static/dexterity/dex3.png
:alt: Choice and multiple choice fields

Choice and multiple choice fields
```

```{figure} _static/dexterity/dex4.png
:alt: Reference fields

Reference fields
```

```{figure} _static/dexterity/dex5.png
:alt: File fields

File fields
```


## mixedfield (datagrid field)

The mixedfield empowers your user to create a list of objects of mixed value types sharing the same schema.
If you are familiar with the Plone Classic datagrid field this is the complementary field / widget combo for Plone.
**mixedfield** is a combination of a Plone Classic JSONField and a widget for Plone. Nothing new, just a term to talk about linking backend and frontend.

Example is a custom history:

```{figure} _static/dexterity/mixedfield_view.png
:alt: view mixedfield values
```

### Backend

Add a `JSONField` field to your content type schema.

```{code-block} python
:emphasize-lines: 1-8, 35, 39, 40
:linenos:

from plone.schema import JSONField

MIXEDFIELD_SCHEMA = json.dumps(
    {
        'type': 'object',
        'properties': {'items': {'type': 'array', 'items': {'type': 'object', 'properties': {}}}},
    }
)

class IExample(model.Schema):
    """Dexterity-Schema"""

    fieldset(
        'datagrid',
        label='Datagrid field',
        fields=(
            # 'datagrid_field',
            'mixed_field',
            ),
    )

    primary('title')
    title = schema.TextLine(
        title='Primary Field (Textline)',
        description='zope.schema.TextLine',
        required=True,
        )

    description = schema.TextLine(
        title='Description (Textline)',
        description='zope.schema.TextLine',
        required=False,
        )

    history_field = JSONField(
        title='Mixedfield: datagrid field for Plone',
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget='history_widget',
        default={'items': []},
        missing_value={'items': []},
        )
```

### Frontend

Provide a widget in your favorite add-on with a schema of elementary fields you need.

```{code-block} jsx
:emphasize-lines: 1,35,37
:linenos:

import ObjectListWidget from '@plone/volto/components/manage/Widgets/ObjectListWidget';

const ItemSchema = {
    title: 'History-Entry',
    properties: {
        historydate: {
            title: 'Date',
            widget: 'date',
        },
        historytopic: {
            title: 'What',
        },
        historyversion: {
            title: 'Version',
        },
        historyauthor: {
            title: 'Who',
        },
    },
    fieldsets: [
        {
            id: 'default',
            title: 'History-Entry',
            fields: [
                'historydate',
                'historytopic',
                'historyversion',
                'historyauthor',
            ],
        },
    ],
    required: [],
};

const HistoryWidget = (props) => {
    return (
        <ObjectListWidget
            schema={ItemSchema}
            {...props}
            value={props.value?.items || props.default?.items || []}
            onChange={(id, value) => props.onChange(id, { items: value })}
        />
    );
};

export default HistoryWidget;
```

Keeping this example as simple as possible we skipped the localization. Please see Volto documentation for details.

Register this widget for the backend field of your choice in your **apps** configuration {file}`config.js`.
The following config code registers the custom Plone _HistoryWidget_ for Plone Classic fields with widget "history_widget".

```{code-block} js
:emphasize-lines: 12
:linenos:

import { HistoryWidget } from '@rohberg/voltotestsomevoltothings/components';

// All your imports required for the config here BEFORE this line
import '@plone/volto/config';

export default function applyConfig(config) {
    config.settings = {
        ...config.settings,
        supportedLanguages: ['en', 'de', 'it'],
        defaultLanguage: 'en',
    };
    config.widgets.widget.history_widget = HistoryWidget;

    return config;
}
```

Please be sure to use `plone.restapi` version >= 7.3.0. If you cannot upgrade `plone.restapi` then a registration per field id instead of a registration per field widget name is needed.

```js
export default function applyConfig(config) {
  config.widgets.id.history_field = HistoryWidget;
  return config;
}
```

The user can now edit the values of the new field _history_field_.

That's what you did to accomplish this:

- You added a new field of type JSONField with widget "history_widget" and default schema to your content type schema.
- You registered the custom Plone widget for widget name "history_widget".

```{figure} _static/dexterity/mixedfield_edit.png
:alt: edit mixedfield values
```

A view ({file}`ExampleView`) of the content type integrates a component to display the values of the field _history_field_.

```{code-block} jsx
:emphasize-lines: 40
:linenos:

import React from 'react';
import moment from 'moment';
import { Container, Table } from 'semantic-ui-react';

const MyHistory = ({ history }) => {
    return (
        _CLIENT__ && (
        <Table celled className="history_list">
            <Table.Header>
            <Table.Row>
                <Table.HeaderCell>Date</Table.HeaderCell>
                <Table.HeaderCell>What</Table.HeaderCell>
                <Table.HeaderCell>Version</Table.HeaderCell>
                <Table.HeaderCell>Who</Table.HeaderCell>
            </Table.Row>
            </Table.Header>

            <Table.Body>
            {history?.items?.map((item) => (
                <Table.Row>
                <Table.Cell>
                    {item.historydate && moment(item.historydate).format('L')}
                </Table.Cell>
                <Table.Cell>{item.historytopic}</Table.Cell>
                <Table.Cell>{item.historyversion}</Table.Cell>
                <Table.Cell>{item.historyauthor}</Table.Cell>
                </Table.Row>
            ))}
            </Table.Body>
        </Table>
        )
    );
};

const ExampleView = ({ content }) => {
    return (
        <Container>
        <h2>I am an ExampleView</h2>
        <h3>History</h3>
        <MyHistory history={content.history_field} />
        </Container>
    );
 };

 export default ExampleView;
```

Et voilà.

```{figure} _static/dexterity/mixedfield_view.png
:alt: view mixedfield values
```


## Widgets

Volto makes suggestions which widget to use, based on the fields type, backend widget and id.

All widgets are listed here: [frontend widgets](https://6.docs.plone.org/storybook)

### Determine frontend widget

If you want to register a frontend widget for your field, you can define your field such as:

```python
directives.widget(
    "specialfield",
    frontendOptions={
        "widget": "specialwidget"
    })
specialfield = schema.TextLine(title="Field with special frontend widget")
```

Then register your frontend widget in your apps configuration.

```jsx
import { MySpecialWidget } from './components';

const applyConfig = (config) => {
  config.widgets.widget.specialwidget = MySpecialWidget;
  return config;
}
```

You can also pass additional props to the frontend widget using the `widgetProps` key:

```python
directives.widget(
    "specialfield",
    frontendOptions={
        "widget": "specialwidget",
        "widgetProps": {"isLarge": True, "color": "red"}
    })
specialfield = schema.TextLine(title="Field with special frontend widget")
```

The props will be injected into the corresponding widget component, configuring it as specified.


## Directives

Directives can be placed anywhere in the class body (annotations are made directly on the class). By convention they are kept next to the fields they apply to.

For example, here is a schema that omits a field:

```python
from plone.autoform import directives
from plone.supermodel import model
from zope import schema


class ISampleSchema(model.Schema):

    title = schema.TextLine(title='Title')

    directives.omitted('additionalInfo')
    additionalInfo = schema.Bytes()
```

You can also handle multiple fields with one directive:

```python
directives.omitted('field_1', 'field_2')
```

With the directive "mode" you can set fields to 'input', 'display' or 'hidden'.

```python
directives.mode(additionalInfo='hidden')
```

You can apply directives to certain forms only. Here we drop a field from the add-form, it will still show up in the edit-form.

```python
from z3c.form.interfaces import IAddForm

class ITask(model.Schema):

    title = schema.TextLine(title='Title')

    directives.omitted(IAddForm, 'done')
    done = schema.Bool(
        title='Done',
        required=False,
    )
```

The same works for custom forms.

With the directive {py:meth}`widget` you can not only change the widget used for a field. With {py:data}`pattern_options` you can pass additional parameters to the widget. Here, we configure the datetime widget powered by the JavaScript library [pickadate](https://amsul.ca/pickadate.js/) by adding options that are used by it. Plone passes the options to the library.

```python
class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title='Date and Time',
        required=False,
    )
    directives.widget(
        'meeting_date',
        DatetimeFieldWidget,
        pattern_options={
            'time': {'interval': 60, 'min': [7, 0], 'max': [19, 0]}},
    )
```

## Validation and default values

In the following example we add a validator and a default value.

```python
from zope.interface import Invalid
import datetime


def future_date(value):
    if value and not value.date() >= datetime.date.today():
        raise Invalid('Meeting date can not be before today.')
    return True


def meeting_date_default_value():
    return datetime.datetime.today() + datetime.timedelta(7)


class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title='Date and Time',
        required=False,
        constraint=future_date,
        defaultFactory=meeting_date_default_value,
    )
```

Validators and defaults can also be made aware of the context (i.e. to check against the values of other fields).

For context aware defaults you need to use a {py:class}`IContextAwareDefaultFactory`. It will be passed the container for which the add form is being displayed:

```python
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def get_container_id(context):
    return context.id.upper()


class IMySchema(model.Schema):

    parent_id = schema.TextLine(
        title='Parent ID',
        required=False,
        defaultFactory=get_container_id,
    )
```

For context-aware validators you need to use {py:meth}`invariant`:

```python
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IContextAwareDefaultFactory


class IMyEvent(model.Schema):

    start = schema.Datetime(
        title='Start date',
        required=False,
    )

    end = schema.Datetime(
        title='End date',
        required=False,
    )

    @invariant
    def validate_start_end(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise Invalid('Start must be before the end.')
```
