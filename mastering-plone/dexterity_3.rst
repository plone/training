.. _dexterity3-label:

Dexterity Types III: Python
===========================

.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout resources

   Code for the end of this chapter::

        git checkout dexterity_3


Without sponsors, a conference would be hard to finance! Plus it is a good opportunity for Plone companies to advertise their services.
But sponsors want to be displayed in a nice way according to the size of their sponsorship.

In this part we will:

* create the content type *sponsor* that has a Python schema,
* create a viewlet that shows the sponsor logos sorted by sponsoring level.


The topics we cover are:

* Python schema for Dexterity
* schema hint and directives
* field permissions
* image scales
* caching


The Python schema
-----------------

First we create the schema for the new type. Instead of XML, we use Python this time.
In chapter :ref:`export_code-label` you already created a folder :file:`content` with an empty :file:`__init__.py` in it.
We don't need to register that folder in :file:`configure.zcml` since we don't need a :file:`content/configure.zcml` (at least not yet).

Now add a new file :file:`content/sponsor.py`.

.. code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-
    from plone.app.textfield import RichText
    from plone.autoform import directives
    from plone.namedfile import field as namedfile
    from plone.supermodel import model
    from plone.supermodel.directives import fieldset
    from ploneconf.site import _
    from z3c.form.browser.radio import RadioFieldWidget
    from zope import schema
    from zope.schema.vocabulary import SimpleTerm
    from zope.schema.vocabulary import SimpleVocabulary


    LevelVocabulary = SimpleVocabulary(
        [SimpleTerm(value=u'platinum', title=_(u'Platinum Sponsor')),
         SimpleTerm(value=u'gold', title=_(u'Gold Sponsor')),
         SimpleTerm(value=u'silver', title=_(u'Silver Sponsor')),
         SimpleTerm(value=u'bronze', title=_(u'Bronze Sponsor'))]
        )


    class ISponsor(model.Schema):
        """Dexterity Schema for Sponsors
        """

        directives.widget(level=RadioFieldWidget)
        level = schema.Choice(
            title=_(u'Sponsoring Level'),
            vocabulary=LevelVocabulary,
            required=True
        )

        text = RichText(
            title=_(u'Text'),
            required=False
        )

        url = schema.URI(
            title=_(u'Link'),
            required=False
        )

        fieldset('Images', fields=['logo', 'advertisement'])
        logo = namedfile.NamedBlobImage(
            title=_(u'Logo'),
            required=False,
        )

        advertisement = namedfile.NamedBlobImage(
            title=_(u'Advertisement (Gold-sponsors and above)'),
            required=False,
        )

        directives.read_permission(notes='cmf.ManagePortal')
        directives.write_permission(notes='cmf.ManagePortal')
        notes = RichText(
            title=_(u'Secret Notes (only for site-admins)'),
            required=False
        )

Some things are notable here:

* The fields in the schema are mostly from :py:mod:`zope.schema`. A reference of available fields is at https://docs.plone.org/external/plone.app.dexterity/docs/reference/fields.html
* In :samp:`directives.widget(level=RadioFieldWidget)` we change the default widget for a Choice field from a dropdown to radio-boxes. An incomplete reference of available widgets is at https://docs.plone.org/external/plone.app.dexterity/docs/reference/widgets.html
* :py:class:`LevelVocabulary` is used to create the options used in the field ``level``. This way we could easily translate the displayed value.
* :samp:`fieldset('Images', fields=['logo', 'advertisement'])` moves the two image fields to another tab.
* :samp:`directives.read_permission(...)` sets the read and write permission for the field ``notes`` to users who can add new members. Usually this permission is only granted to Site Administrators and Managers. We use it to store information that should not be publicly visible. Please note that :py:attr:`obj.notes` is still accessible in templates and Python. Only using the widget (like we do in the view later) checks for the permission.
* We no longer use grok, an obsolete Plone technology.

..  seealso::

    * `All available Fields <https://docs.plone.org/external/plone.app.dexterity/docs/reference/fields.html#field-types>`_
    * `Schema-driven types with Dexterity <https://docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-driven-types>`_
    * `Form schema hints and directives <https://docs.plone.org/external/plone.app.dexterity/docs/reference/form-schema-hints.html>`_


Directives
----------

Directives can be placed anywhere in the class body (annotations are made directly on the class). By convention they are kept next to the fields they apply to.

For example, here is a schema that omits a field:

..  code-block:: python

    from plone.autoform import directives
    from plone.supermodel import model
    from zope import schema


    class ISampleSchema(model.Schema):

        title = schema.TextLine(title=u'Title')

        directives.omitted('additionalInfo')
        additionalInfo = schema.Bytes()


You can also handle multiple fields with one directive:

..  code-block:: python

    directives.omitted('field_1', 'field_2')

With the directive "mode" you can set fields to 'input', 'display' or 'hidden'.

..  code-block:: python

    directives.mode(additionalInfo='hidden')

You can apply directives to certain forms only. Here we drop a field from the add-form, it will still show up in the edit-form.

..  code-block:: python

    from z3c.form.interfaces import IAddForm

    class ITask(model.Schema):

        title = schema.TextLine(title=u'Title')

        directives.omitted(IAddForm, 'done')
        done = schema.Bool(
            title=_(u'Done'),
            required=False,
        )

The same works for custom forms.

With the directive :py:meth:`widget` you can not only change the widget used for a field. With :py:data:`pattern_options` you can pass additional parameters to the widget. Here, we configure the datetime widget powered by the JavaScript library `pickadate <https://amsul.ca/pickadate.js/>`_  by adding options that are used by it. Plone passes the options to the library.

..  code-block:: python

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


Validation and default values
-----------------------------

In the following example we add a validator and a default value.


..  code-block:: python

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

Validators and defaults can be also be made aware of the context (i.e. to check against the values of other fields).

For context aware defaults you need to use a :py:class:`IContextAwareDefaultFactory`. It will be passed the container for which the add form is being displayed:

..  code-block:: python

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

For context-aware validators you need to use :py:meth:`invariant`:

..  code-block:: python

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

To learn more about directives, validators and default values, refer to the following:

* `Form schema hints and directives <https://docs.plone.org/external/plone.app.dexterity/docs/reference/form-schema-hints.html>`_
* `Validation <https://docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/validation.html>`_ (this documentation unfortunately still uses the obsolete grok technology)
* `z3c.form documentation <https://pypi.org/project/z3c.form#validators>`_
* `Default values for fields on add forms <https://docs.plone.org/external/plone.app.dexterity/docs/advanced/defaults.html>`_


The Factory Type Information, or FTI
------------------------------------

Next, we create the factory type information ("FTI") for the new type in :file:`profiles/default/types/sponsor.xml`

.. code-block:: xml
    :linenos:
    :emphasize-lines: 26

    <?xml version="1.0"?>
    <object name="sponsor" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <property name="title" i18n:translate="">Sponsor</property>
     <property name="description" i18n:translate=""></property>
     <property name="icon_expr">string:${portal_url}/document_icon.png</property>
     <property name="factory">sponsor</property>
     <property name="add_view_expr">string:${folder_url}/++add++sponsor</property>
     <property name="link_target"></property>
     <property name="immediate_view">view</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types"/>
     <property name="allow_discussion">False</property>
     <property name="default_view">view</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     <property name="default_view_fallback">False</property>
     <property name="add_permission">cmf.AddPortalContent</property>
     <property name="klass">plone.dexterity.content.Container</property>
     <property name="behaviors">
      <element value="plone.dublincore"/>
      <element value="plone.namefromtitle"/>
     </property>
     <property name="schema">ploneconf.site.content.sponsor.ISponsor</property>
     <property name="model_source"></property>
     <property name="model_file"></property>
     <property name="schema_policy">dexterity</property>
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     <action title="View" action_id="view" category="object" condition_expr=""
        description="" icon_expr="" link_target="" url_expr="string:${object_url}"
        visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        description="" icon_expr="" link_target=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

Then we register the FTI in :file:`profiles/default/types.xml`

.. code-block:: xml
    :linenos:
    :emphasize-lines: 5

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <property name="title">Controls the available contenttypes in your portal</property>
     <object name="talk" meta_type="Dexterity FTI"/>
     <object name="sponsor" meta_type="Dexterity FTI"/>
     <!-- -*- more types can be added here -*- -->
    </object>

After reinstalling our package we can create the new type.


Exercise 1
++++++++++

Sponsors are containers but they don't need to be. Turn them into items by changing their class to :py:class:`plone.dexterity.content.Item`.

..  admonition:: Solution
    :class: toggle

    Simply modify the property ``klass`` in the FTI and reinstall.

    .. code-block:: xml
        :linenos:

        <property name="klass">plone.dexterity.content.Item</property>


The view
--------

We use the default view provided by Dexterity for testing since we will only display the sponsors in a viewlet and not in their own page.

.. note::

    If we really want a custom view for sponsors it could look like this.

    .. code-block:: xml
        :linenos:

        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
              metal:use-macro="context/main_template/macros/master"
              i18n:domain="ploneconf.site">
        <body>
          <metal:content-core fill-slot="content-core">
            <h3 tal:content="structure view/w/level/render">
              Level
            </h3>

            <div tal:content="structure view/w/text/render">
              Text
            </div>

            <div class="newsImageContainer">
              <a tal:attributes="href context/url">
                <img tal:condition="python:getattr(context, 'logo', None)"
                     tal:attributes="src string:${context/absolute_url}/@@images/logo/preview" />
              </a>
            </div>

            <div>
              <a tal:attributes="href context/url">
                Website
              </a>

              <img tal:condition="python:getattr(context, 'advertisement', None)"
                   tal:attributes="src string:${context/absolute_url}/@@images/advertisement/preview" />

              <div tal:condition="python: 'notes' in view.w"
                   tal:content="structure view/w/notes/render">
                Notes
              </div>

            </div>
          </metal:content-core>
        </body>
        </html>

    Note how we handle the field with special permissions: :samp:`tal:condition="python: 'notes' in view.w"` checks if the convenience-dictionary :py:data:`w` (provided by the base class :py:class:`DefaultView`) holds the widget for the field ``notes``.
    If the current user does not have the permission :py:mod:`cmf.ManagePortal` it will be omitted from the dictionary and get an error since ``notes`` would not be a key in :py:data:`w`. By first checking if it's missing we work around that.


The viewlet
-----------

Instead of writing a view you will have to display the sponsors at the bottom of the website in a viewlet.

Register the viewlet in :file:`browser/configure.zcml`

.. code-block:: xml
    :linenos:

    <browser:viewlet
        name="sponsorsviewlet"
        manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
        for="*"
        layer="..interfaces.IPloneconfSiteLayer"
        class=".viewlets.SponsorsViewlet"
        template="templates/sponsors_viewlet.pt"
        permission="zope2.View"
        />

Add the viewlet class in :file:`browser/viewlets.py`

.. code-block:: python
    :linenos:
    :emphasize-lines: 2-3, 5, 7-9, 19-63

    # -*- coding: utf-8 -*-
    from collections import OrderedDict
    from plone import api
    from plone.app.layout.viewlets.common import ViewletBase
    from plone.memoize import ram
    from ploneconf.site.behaviors.featured import IFeatured
    from ploneconf.site.content.sponsor import LevelVocabulary
    from random import shuffle
    from time import time


    class FeaturedViewlet(ViewletBase):

        def is_featured(self):
            adapted = IFeatured(self.context)
            return adapted.featured


    class SponsorsViewlet(ViewletBase):

        @ram.cache(lambda *args: time() // (60 * 60))
        def _sponsors(self):
            results = []
            for brain in api.content.find(portal_type='sponsor'):
                obj = brain.getObject()
                scales = api.content.get_view(
                    name='images',
                    context=obj,
                    request=self.request)
                scale = scales.scale(
                    'logo',
                    width=200,
                    height=80,
                    direction='down')
                tag = scale.tag() if scale else None
                if not tag:
                    # only display sponsors with a logo
                    continue
                results.append({
                    'title': obj.title,
                    'description': obj.description,
                    'tag': tag,
                    'url': obj.url or obj.absolute_url(),
                    'level': obj.level
                })
            return results

        def sponsors(self):
            sponsors = self._sponsors()
            if not sponsors:
                return
            results = OrderedDict()
            levels = [i.value for i in LevelVocabulary]
            for level in levels:
                level_sponsors = []
                for sponsor in sponsors:
                    if level == sponsor['level']:
                        level_sponsors.append(sponsor)
                if not level_sponsors:
                    continue
                shuffle(level_sponsors)
                results[level] = level_sponsors
            return results

* :py:meth:`_sponsors` returns a list of dictionaries containing all necessary info about sponsors.
* We create the complete `img` tag using a custom scale (200x80) using the view ``images`` from :py:mod:`plone.namedfile.` This actually scales the logos and saves them as new blobs.
* In :py:meth:`sponsors` we return an ordered dictionary of randomized lists of dicts (containing the information on sponsors). The order is by sponsor-level since we want the platinum sponsors on top and the bronze sponsors at the bottom. The randomization is for fairness among equal sponsors.

:py:meth:`_sponsors` is cached for an hour using `plone.memoize <https://docs.plone.org/manage/deploying/performance/decorators.html#timeout-caches>`_. This way we don't need to keep all sponsor objects in memory all the time. But we'd have to wait for up to an hour until changes will be visible.

Instead we should cache until one of the sponsors is modified by using a callable :py:func:`_sponsors_cachekey` that returns a number that changes when a sponsor is modified.

  ..  code-block:: python

      ...
      def _sponsors_cachekey(method, self):
          brains = api.content.find(portal_type='sponsor')
          cachekey = sum([int(i.modified) for i in brains])
          return cachekey

      @ram.cache(_sponsors_cachekey)
      def _sponsors(self):
          catalog = api.portal.get_tool('portal_catalog')
      ...

.. seealso::

    * `Guide to Caching <https://docs.plone.org/manage/deploying/caching/index.html>`_
    * `Cache decorators <https://docs.plone.org/manage/deploying/performance/decorators.html>`_
    * `Image Scaling <https://docs.plone.org/develop/plone/images/content.html#creating-scales>`_


The template for the viewlet
----------------------------

Add the template :file:`browser/templates/sponsors_viewlet.pt`

.. code-block:: xml
    :linenos:

    <div metal:define-macro="portal_sponsorbox"
         i18n:domain="ploneconf.site">
        <div id="portal-sponsorbox" class="container"
             tal:define="sponsors view/sponsors;"
             tal:condition="sponsors">
            <div class="row">
                <h2>We ❤ our sponsors</h2>
            </div>
            <div tal:repeat="level sponsors"
                 tal:attributes="id python:'level-' + level"
                 class="row">
                <h3 tal:content="python: level.capitalize()">
                    Gold
                </h3>
                <tal:images tal:define="items python:sponsors[level];"
                            tal:repeat="item items">
                    <div class="sponsor">
                        <a href=""
                           tal:attributes="href python:item['url'];
                                           title python:item['title'];">
                            <img tal:replace="structure python:item['tag']" />
                        </a>
                    </div>
                </tal:images>
            </div>
        </div>
    </div>

You can now add some CSS in :file:`browser/static/ploneconf.css` to make it look OK.

..  code-block:: css

    .sponsor {
        display: inline-block;
        margin: 0 1em 1em 0;
    }

    .sponsor:hover {
        box-shadow: 0 0 8px #000;
        -moz-box-shadow: 0 0 8px #000;
        -webkit-box-shadow: 0 0 8px #000;
    }


Result:

.. figure:: _static/dexterity_3_sponsor_schema.png
    :scale: 50%
    :alt: The result of the newly created content type.

    The result of the newly created content type.


Exercise 2
++++++++++

Turn the content type Speaker from :ref:`Exercise 2 of the first chapter on Dexterity <dexterity1-excercises-label>` into a Python-based type.

When we're done, it should have the following fields:

* title
* email
* homepage
* biography
* company
* twitter_name
* irc_name
* image

Do *not* use the :py:class:`IBasic` or :py:class:`IDublinCore` behavior to add title and description. Instead add your own field ``title`` and give it the title *Name*.

..  admonition:: Solution
    :class: toggle

    ..  code-block:: python
        :linenos:

        # -*- coding: utf-8 -*-
        from plone.app.textfield import RichText
        from plone.app.vocabularies.catalog import CatalogSource
        from plone.autoform import directives
        from plone.namedfile import field as namedfile
        from plone.supermodel import model
        from ploneconf.site import _
        from z3c.relationfield.schema import RelationChoice
        from z3c.relationfield.schema import RelationList
        from zope import schema


        class ISpeaker(model.Schema):
            """Dexterity-Schema for Speaker
            """

            title = schema.TextLine(
                title=_(u'Name'),
            )

            email = schema.TextLine(
                title=_(u'E-Mail'),
                required=False,
            )

            homepage = schema.URI(
                title=_(u'Homepage'),
                required=False,
            )

            biography = RichText(
                title=_(u'Biography'),
                required=False,
            )

            company = schema.TextLine(
                title=_(u'Company'),
                required=False,
            )

            twitter_name = schema.TextLine(
                title=_(u'Twitter-Name'),
                required=False,
            )

            irc_name = schema.TextLine(
                title=_(u'IRC-Name'),
                required=False,
            )

            image = namedfile.NamedBlobImage(
                title=_(u'Image'),
                required=False,
            )

    Register the type in :file:`profiles/default/types.xml`

    .. code-block:: xml
        :linenos:
        :emphasize-lines: 6

        <?xml version="1.0"?>
        <object name="portal_types" meta_type="Plone Types Tool">
         <property name="title">Controls the available contenttypes in your portal</property>
         <object name="talk" meta_type="Dexterity FTI"/>
         <object name="sponsor" meta_type="Dexterity FTI"/>
         <object name="speaker" meta_type="Dexterity FTI"/>
         <!-- -*- more types can be added here -*- -->
        </object>

    The FTI goes in :file:`profiles/default/types/speaker.xml`. Again we use :py:class:`Item` as the base-class:

    .. code-block:: xml
        :linenos:

        <?xml version="1.0"?>
        <object name="speaker" meta_type="Dexterity FTI" i18n:domain="plone"
           xmlns:i18n="http://xml.zope.org/namespaces/i18n">
         <property name="title" i18n:translate="">Speaker</property>
         <property name="description" i18n:translate=""></property>
         <property name="icon_expr"></property>
         <property name="factory">speaker</property>
         <property name="add_view_expr">string:${folder_url}/++add++speaker</property>
         <property name="link_target"></property>
         <property name="immediate_view">view</property>
         <property name="global_allow">True</property>
         <property name="filter_content_types">True</property>
         <property name="allowed_content_types"/>
         <property name="allow_discussion">False</property>
         <property name="default_view">view</property>
         <property name="view_methods">
          <element value="view"/>
         </property>
         <property name="default_view_fallback">False</property>
         <property name="add_permission">cmf.AddPortalContent</property>
         <property name="klass">plone.dexterity.content.Item</property>
         <property name="schema">ploneconf.site.content.speaker.ISpeaker</property>
         <property name="model_source"></property>
         <property name="model_file"></property>
         <property name="behaviors">
          <element value="plone.namefromtitle"/>
         </property>
         <property name="schema_policy">dexterity</property>
         <alias from="(Default)" to="(dynamic view)"/>
         <alias from="edit" to="@@edit"/>
         <alias from="sharing" to="@@sharing"/>
         <alias from="view" to="(selected layout)"/>
         <action title="View" action_id="view" category="object" condition_expr=""
            description="" icon_expr="" link_target="" url_expr="string:${object_url}"
            visible="True">
          <permission value="View"/>
         </action>
         <action title="Edit" action_id="edit" category="object" condition_expr=""
            description="" icon_expr="" link_target=""
            url_expr="string:${object_url}/edit" visible="True">
          <permission value="Modify portal content"/>
         </action>
        </object>

    After reinstalling the package the new type is usable.


Exercise 3
++++++++++

This is more of a Python exercise. The gold and bronze sponsors should also have a bigger logo than the others. Scale the sponsors' logos to the following sizes without using CSS.

* Platinum: 500x200
* Gold: 350x150
* Silver: 200x80
* Bronze: 150x60


..  admonition:: Solution
    :class: toggle

    ..  code-block:: python
        :linenos:
        :emphasize-lines: 10-15, 41, 44-45

        # -*- coding: utf-8 -*-
        from collections import OrderedDict
        from plone import api
        from plone.app.layout.viewlets.common import ViewletBase
        from plone.memoize import ram
        from ploneconf.site.behaviors.social import ISocial
        from ploneconf.site.content.sponsor import LevelVocabulary
        from random import shuffle

        LEVEL_SIZE_MAPPING = {
            'platinum': (500, 200),
            'gold': (350, 150),
            'silver': (200, 80),
            'bronze': (150, 60),
        }


        class SocialViewlet(ViewletBase):

            def lanyrd_link(self):
                adapted = ISocial(self.context)
                return adapted.lanyrd


        class SponsorsViewlet(ViewletBase):

            def _sponsors_cachekey(method, self):
                brains = api.content.find(portal_type='sponsor')
                cachekey = sum([int(i.modified) for i in brains])
                return cachekey

            @ram.cache(_sponsors_cachekey)
            def _sponsors(self):
                results = []
                for brain in api.content.find(portal_type='sponsor'):
                    obj = brain.getObject()
                    scales = api.content.get_view(
                        name='images',
                        context=obj,
                        request=self.request)
                    width, height = LEVEL_SIZE_MAPPING[obj.level]
                    scale = scales.scale(
                        'logo',
                        width=width,
                        height=height,
                        direction='down')
                    tag = scale.tag() if scale else None
                    if not tag:
                        # only display sponsors with a logo
                        continue
                    results.append({
                        'title': obj.title,
                        'description': obj.description,
                        'tag': tag,
                        'url': obj.url or obj.absolute_url(),
                        'level': obj.level
                    })
                return results

            def sponsors(self):
                sponsors = self._sponsors()
                if not sponsors:
                    return
                results = OrderedDict()
                levels = [i.value for i in LevelVocabulary]
                for level in levels:
                    level_sponsors = []
                    for sponsor in sponsors:
                        if level == sponsor['level']:
                            level_sponsors.append(sponsor)
                    if not level_sponsors:
                        continue
                    shuffle(level_sponsors)
                    results[level] = level_sponsors
                return results

