.. _dexterity1-label:

========================
Dexterity III: Reference
========================

This chapter documents all types fields, widgets, directived that you can use with dexterity


Fields
======

This is a schema that holds examples for each field-type that are shipped with Plone by default.

Some more complex field-types are discussed below.

Many fields have several options that are not discussed here in detail.

Fields shipped with Plone
-------------------------

..  code-block:: python

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

        primary('title')
        title = schema.TextLine(
            title=u'Title',
            required=True,
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
            description=u'List field with checkboxes',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            )

        directives.widget(list_field_checkbox=CheckBoxFieldWidget)
        list_field_checkbox = schema.List(
            title=u'List field with checkboxes',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            )

        directives.widget(list_field_select=SelectFieldWidget)
        list_field_select = schema.List(
            title=u'List field with select widget',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            )

        list_field_voc_unconstrained = schema.Tuple(
            title=u'List field with values from vocabulary but not constrained to them.',
            value_type=schema.TextLine(),
            required=False,
            missing_value=(),
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
            )

        set_field = schema.Set(
            title=u'Set field',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            )

        directives.widget(set_field_checkbox=CheckBoxFieldWidget)
        set_field_checkbox = schema.Set(
            title=u'Set field with checkboxes',
            value_type=schema.Choice(
                values=[u'Beginner', u'Advanced', u'Professional'],
                ),
            required=False,
            )

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
            description=u'Uses a time picker',
            required=False,
        )

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

        int_field = schema.Int(
            title=u"Integer Field",
            description=u"Allocated (maximum) number of objects",
            required=False,
        )

        float_field = schema.Float(
            title=u"Float field",
            required=False,
        )

        richtext_field = RichText(
            title=u'RichText field',
            description=u'This uses a richtext editor.',
            max_length=2000,
            required=False,
            )

        fieldset(
            'myfieldset',
            label=u'A custom fieldset',
            fields=('int_field', 'float_field'),
        )

        # TODO:
        # SourceText
        # Bytes
        # NativeString
        # ASCII
        # BytesLine
        # NativeStringLine
        # ASCIILine
        # Decimal
        # Timedelta
        # Time
        # PythonIdentifier
        # DottedName
        # Id
        # InterfaceField
        # Sequence
        # MutableSequence
        # FrozenSet
        # Mapping
        # MutableMapping
        # Dict

    @implementer(IExample)
    class Example(Container):
        """Example instance class"""





3rd party fields
----------------

Also:

* Datagridfield
* Computedfield -> @property
* @property and acquisition
* Backrelationfield
* ...


..  code-block:: python

    from collective.z3cform.datagridfield import DataGridFieldFactory
    from collective.z3cform.datagridfield import DictRow

    class IMyRowSchema(Interface):

        choice_field = schema.Choice(
            title='Choice Field',
            vocabulary='step.objectives',
            required=False,
            )
        directives.widget('objective', SelectFieldWidget)

        textline_field = schema.TextLine(
            title='Textline field',
            required=False,
            )

        bool_field = schema.Bool(
            title=u'Boolean field',
            required=False,
        )


    class IExampleWithDatagrid(model.Schema):

        datagrid_field = schema.List(
            title=u'Kategorisierung',
            value_type=DictRow(title=u'Table', schema=IMyRowSchema),
            default=[],
            required=False,
        )
        directives.widget('datagrid_field', DataGridFieldFactory)

