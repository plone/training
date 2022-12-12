---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-dexterity-reference-label)=

# Dexterity: Reference

This chapter documents all types fields, widgets, directives that you can use with dexterity.

## Fields included in Plone

This is a schema with examples for all field-types that are shipped with Plone by default. They are arranged in fieldsets:

Default

: Textline, Text, Boolean, Richtext (html), Email

Number fields

: Integer, Float

Date and time fields

: Datetime,
Date,
Time,
Timedelta

Choice and Multiple Choice fields

: Choice,
Choice with radio widget,
Choice with Select2 widget,
Choice with named vocabulary,
List,
List with checkboxes,
List with Select2 widget,
List with values from named vocabulary but open to additions,
Tuple,
Set,
Set with checkboxes

Relation fields

: Relationchoice, Relationlist

File fields

: File, Image

Other fields

: Uri, Sourcetext, Ascii, Bytesline, Asciiline, Pythonidentifier, Dottedname, Dict, Dict with Choice

```{code-block} python
:linenos:

# -*- coding: utf-8 -*-
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.supermodel.directives import primary
from ploneconf.site import _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import Relation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IExample(model.Schema):
    """Dexterity-Schema with all field-types."""

    # The most used fields
    # textline, text, bool, richtext, email


    fieldset(
        'numberfields',
        label=u'Number fields',
        fields=('int_field', 'float_field'),
    )

    fieldset(
        'datetimefields',
        label=u'Date and time fields',
        fields=('datetime_field', 'date_field', 'time_field', 'timedelta_field'),
    )

    fieldset(
        'choicefields',
        label=u'Choice and Multiple Choice fields',
        fields=(
            'choice_field',
            'choice_field_radio',
            'choice_field_select',
            'choice_field_voc',
            'list_field',
            'list_field_checkbox',
            'list_field_select',
            'list_field_voc_unconstrained',
            'tuple_field',
            'set_field',
            'set_field_checkbox',
        ),
    )

    fieldset(
        'relationfields',
        label=u'Relation fields',
        fields=('relationchoice_field', 'relationlist_field'),
    )

    fieldset(
        'filefields',
        label=u'File fields',
        fields=('file_field', 'image_field'),
    )

    fieldset(
        'otherfields',
        label=u'Other fields',
        fields=(
            'uri_field',
            'sourcetext_field',
            'ascii_field',
            'bytesline_field',
            'asciiline_field',
            'pythonidentifier_field',
            'dottedname_field',
            'dict_field',
            'dict_field_with_choice',
            ),
    )

    primary('title')
    title = schema.TextLine(
        title=u'Primary Field (Textline)',
        required=True,
        )

    text_field = schema.Text(
        title=u'Text Field',
        required=False,
        missing_value=u'',
    )

    textline_field = schema.TextLine(
        title=u'Textline field',
        description=u'A simple input field',
        required=False,
        )

    bool_field = schema.Bool(
        title=u'Boolean field',
        required=False,
    )

    choice_field = schema.Choice(
        title=u'Choice field',
        values=[u'One', u'Two', u'Three'],
        required=True,
        )

    directives.widget(choice_field_radio=RadioFieldWidget)
    choice_field_radio = schema.Choice(
        title=u'Choice field with radio boxes',
        values=[u'One', u'Two', u'Three'],
        required=True,
        )

    choice_field_voc = schema.Choice(
        title=u'Choicefield with values from named vocabulary',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
        )

    directives.widget(choice_field_select=SelectFieldWidget)
    choice_field_select = schema.Choice(
        title=u'Choicefield with select2 widget',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
        )

    list_field = schema.List(
        title=u'List field',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value=[],
        )

    directives.widget(list_field_checkbox=CheckBoxFieldWidget)
    list_field_checkbox = schema.List(
        title=u'List field with checkboxes',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value=[],
        )

    directives.widget(list_field_select=SelectFieldWidget)
    list_field_select = schema.List(
        title=u'List field with select widget',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value=[],
        )

    list_field_voc_unconstrained = schema.List(
        title=u'List field with values from vocabulary but not constrained to them.',
        value_type=schema.TextLine(),
        required=False,
        missing_value=[],
        )
    directives.widget(
        'list_field_voc_unconstrained',
        AjaxSelectFieldWidget,
        vocabulary='plone.app.vocabularies.Users'
    )


    tuple_field = schema.Tuple(
        title=u'Tuple field',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value=(),
        )

    set_field = schema.Set(
        title=u'Set field',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value={},
        )

    directives.widget(set_field_checkbox=CheckBoxFieldWidget)
    set_field_checkbox = schema.Set(
        title=u'Set field with checkboxes',
        value_type=schema.Choice(
            values=[u'Beginner', u'Advanced', u'Professional'],
            ),
        required=False,
        missing_value={},
        )

    # File fields
    image_field = NamedBlobImage(
        title=u'Image field',
        description=u'A upload field for images',
        required=False,
        )

    file_field = NamedBlobFile(
        title=u'File field',
        description=u'A upload field for files',
        required=False,
        )

    # Date and Time fields
    datetime_field = schema.Datetime(
        title=u'Datetime field',
        description=u'Uses a date and time picker',
        required=False,
    )

    date_field = schema.Date(
        title=u'Date field',
        description=u'Uses a date picker',
        required=False,
    )

    time_field = schema.Time(
        title=u'Time field',
        required=False,
        )

    timedelta_field = schema.Timedelta(
        title=u'Timedelta field',
        required=False,
        )

    # Relation Fields
    relationchoice_field = RelationChoice(
        title=u"Relationchoice field",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "relationchoice_field",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )

    relationlist_field = RelationList(
        title=u"Relationlist Field",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "relationlist_field",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )

    # Number fields
    int_field = schema.Int(
        title=u"Integer Field (e.g. 12)",
        description=u"Allocated (maximum) number of objects",
        required=False,
    )

    float_field = schema.Float(
        title=u"Float field (e.g. 12.2)",
        required=False,
    )

    # Text fields
    email_field = Email(
        title=u'Email field',
        description=u'A simple input field for a email',
        required=False,
        )

    uri_field = schema.URI(
        title=u'URI field',
        description=u'A simple input field for a URLs',
        required=False,
        )

    richtext_field = RichText(
        title=u'RichText field',
        description=u'This uses a richtext editor.',
        max_length=2000,
        required=False,
        )

    sourcetext_field = schema.SourceText(
        title=u'SourceText field',
        required=False,
        )

    ascii_field = schema.ASCII(
        title=u'ASCII field',
        required=False,
        )

    bytesline_field = schema.BytesLine(
        title=u'BytesLine field',
        required=False,
        )

    asciiline_field = schema.ASCIILine(
        title=u'ASCIILine field',
        required=False,
        )

    pythonidentifier_field = schema.PythonIdentifier(
        title=u'PythonIdentifier field',
        required=False,
        )

    dottedname_field = schema.DottedName(
        title=u'DottedName field',
        required=False,
        )

    dict_field = schema.Dict(
        title=u'Dict field',
        required=False,
        key_type = schema.TextLine(
            title=u'Key',
            required=False,
            ),
        value_type = schema.TextLine(
            title=u'Value',
            required=False,
            ),
        )

    dict_field_with_choice = schema.Dict(
        title=u'Dict field with key and value as choice',
        required=False,
        key_type = schema.Choice(
            title=u'Key',
            values=[u'One', u'Two', u'Three'],
            required=False,
            ),
        value_type = schema.Set(
            title=u'Value',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            missing_value={},
            ),
        )

@implementer(IExample)
class Example(Container):
    """Example instance class"""
```

## How fields look like

This is how these fields look like when editing content:

```{figure} _static/dexterity_reference_default_fields.png
:alt: Default fields

Default fields
```

```{figure} _static/dexterity_reference_number_fields.png
:alt: Number fields

Number fields
```

```{figure} _static/dexterity_reference_datetime_fields.png
:alt: Date and time fields

Date and time fields
```

```{figure} _static/dexterity_reference_choice_and_list_fields.png
:alt: Choice and multiple choice fields

Choice and multiple choice fields
```

```{figure} _static/dexterity_reference_file_fields.png
:alt: File fields

File fields
```

```{figure} _static/dexterity_reference_relation_fields.png
:alt: Reference fields

Reference fields
```

```{figure} _static/dexterity_reference_other_fields.png
:alt: Other fields including the dict field

Other fields including the dict field
```

## 3rd party fields

- To control the avilable values of other fields or hide/show them based on user input use the [Masterselect Field](https://pypi.org/project/plone.formwidget.masterselect/).
- For spam-protection use [collective.z3cform.norobots](https://pypi.org/project/collective.z3cform.norobots/).
- Color-Picker [collective.z3cform.colorpicker](https://github.com/collective/collective.z3cform.colorpicker)
- There is no Computedfield but most use-cases can be achieved with a readonly-field and a property. See the [discussion](https://community.plone.org/t/computed-field-for-dexterity/11405)

## Datagrid Field

The [Datagridfield](https://pypi.org/project/collective.z3cform.datagridfield/) allows you to enter multiple values at once as rows in a table. Each row is a sub form defined in a separate schema.

Here is an example:

```{code-block} python
:linenos:

# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IMyRowSchema(Interface):

    choice_field = schema.Choice(
        title=u'Choice Field',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
        )
    directives.widget('objective', SelectFieldWidget)

    textline_field = schema.TextLine(
        title=u'Textline field',
        required=False,
        )

    bool_field = schema.Bool(
        title=u'Boolean field',
        required=False,
    )


class IExampleWithDatagrid(model.Schema):

    title = schema.TextLine(title=u'Title', required=True)

    datagrid_field = schema.List(
        title=u'Datagrid field',
        value_type=DictRow(title=u'Table', schema=IMyRowSchema),
        default=[],
        required=False,
    )
    directives.widget('datagrid_field', DataGridFieldFactory)
```

The edit-form looks like this:

```{figure} _static/dexterity_reference_datagridfield_edit.png

```

The output looks like this:

```{figure} _static/dexterity_reference_datagridfield_view.png

```

```{seealso}
- [All available Fields](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/fields.html#field-types)
- [Schema-driven types with Dexterity](https://5.docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-driven-types)
```

## Widgets

```{eval-rst}
.. todo::

    Document all available widgets

```

## Directives

Directives can be placed anywhere in the class body (annotations are made directly on the class). By convention they are kept next to the fields they apply to.

For example, here is a schema that omits a field:

```python
from plone.autoform import directives
from plone.supermodel import model
from zope import schema


class ISampleSchema(model.Schema):

    title = schema.TextLine(title=u'Title')

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

    title = schema.TextLine(title=u'Title')

    directives.omitted(IAddForm, 'done')
    done = schema.Bool(
        title=_(u'Done'),
        required=False,
    )
```

The same works for custom forms.

With the directive {py:meth}`widget` you can not only change the widget used for a field. With {py:data}`pattern_options` you can pass additional parameters to the widget. Here, we configure the datetime widget powered by the JavaScript library [pickadate](https://amsul.ca/pickadate.js/) by adding options that are used by it. Plone passes the options to the library.

```python
class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title=_(default=u'Date and Time'),
        required=False,
    )
    directives.widget(
        'meeting_date',
        DatetimeFieldWidget,
        pattern_options={
            'time': {'interval': 60, 'min': [7, 0], 'max': [19, 0]}},
    )
```

### Validation and default values

In the following example we add a validator and a default value.

```python
from zope.interface import Invalid
import datetime


def future_date(value):
    if value and not value.date() >= datetime.date.today():
        raise Invalid(_(u"Meeting date can not be before today."))
    return True

def meeting_date_default_value():
    return datetime.datetime.today() + datetime.timedelta(7)


class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title=_(default=u'Date and Time'),
        required=False,
        constraint=future_date,
        defaultFactory=meeting_date_default_value,
    )
```

Validators and defaults can be also be made aware of the context (i.e. to check against the values of other fields).

For context aware defaults you need to use a {py:class}`IContextAwareDefaultFactory`. It will be passed the container for which the add form is being displayed:

```python
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

@provider(IContextAwareDefaultFactory)
def get_container_id(context):
    return context.id.upper()

class IMySchema(model.Schema):

    parent_id = schema.TextLine(
        title=_(u'Parent ID'),
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
        title=_(u'Start date'),
        required=False)

    end = schema.Datetime(
            title=_(u"End date"),
            required=False)

    @invariant
    def validate_start_end(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise Invalid(_('Start must be before the end.'))
```

```{seealso}
To learn more about directives, validators and default values, refer to the following:

- [Form schema hints and directives](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/form-schema-hints.html)
- [Validation](https://5.docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/validation.html) (this documentation unfortunately still uses the obsolete grok technology)
- [z3c.form documentation](https://z3cform.readthedocs.io/en/latest/advanced/validator.html)
- [Default values for fields on add forms](https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/defaults.html)
```
