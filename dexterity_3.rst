.. _dexterity3-label:

Dexterity Types III: Python
===========================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/29_dexterity_3/ src/ploneconf.site


Without sponsors a conference would be hard to finance plus it is a good opportunity for Plone-companies to advertise their services.

In this part we will:

* create the content-type *sponsor* that has a python-schema
* create a viewlet that shows the sponsors logo sorted by sponsoring-level


The topics we cover are:

* python-schemata for dexterity
* schema directives
* field-permissions
* image-scales
* caching

First we create the schema for the new type. Instead of xml we use python now. Create a new folder ``content`` with a empty ``__init__.py`` in it. Now add a new file ``content/sponsor.py``.

.. code-block:: python
    :linenos:

    from plone.app.textfield import RichText
    from plone.autoform import directives
    from plone.namedfile import field as namedfile
    from plone.supermodel.directives import fieldset
    from plone.supermodel import model
    from z3c.form.browser.radio import RadioFieldWidget
    from zope import schema
    from zope.schema.vocabulary import SimpleVocabulary
    from zope.schema.vocabulary import SimpleTerm

    from ploneconf.site import MessageFactory as _


    LevelVocabulary = SimpleVocabulary(
        [SimpleTerm(value=u'platinum', title=_(u'Platinum Sponsor')),
         SimpleTerm(value=u'gold', title=_(u'Gold Sponsor')),
         SimpleTerm(value=u'silver', title=_(u'Silver Sponsor')),
         SimpleTerm(value=u'bronze', title=_(u'Bronze Sponsor'))]
        )


    class ISponsor(model.Schema):
        """Dexterity-Schema for Sponsors
        """

        directives.widget(level=RadioFieldWidget)
        level = schema.Choice(
            title=_(u"Sponsoring Level"),
            vocabulary=LevelVocabulary,
            required=True
        )

        text = RichText(
            title=_(u"Text"),
            required=False
        )

        url = schema.URI(
            title=_(u"Link"),
            required=False
        )

        fieldset('Images', fields=['logo', 'advertisment'])
        logo = namedfile.NamedBlobImage(
            title=_(u"Logo"),
            required=False,
        )

        advertisment = namedfile.NamedBlobImage(
            title=_(u"Advertisment (Gold-sponsors and above)"),
            required=False,
        )

        directives.read_permission(notes="cmf.ManagePortal")
        directives.write_permission(notes="cmf.ManagePortal")
        notes = RichText(
            title=_(u"Secret Notes (only for site-admins)"),
            required=False
        )

Some things are notable here:

* The fields in the schema are mostly from ``zope.schema``. A reference of available fields is at http://docs.plone.org/external/plone.app.dexterity/docs/reference/fields.html
* In ``directives.widget(level=RadioFieldWidget)`` we change the default widget for a Choice-field from a dropdown to radioboxes. A incomplete reference of available widgets is at http://docs.plone.org/external/plone.app.dexterity/docs/reference/widgets.html
* ``LevelVocabulary`` is used to create the options used in the field ``level``. This way we could easily translate the displayed value.
* ``fieldset('Images', fields=['logo', 'advertisment'])`` moves the two image-fields to another tab.
* ``directives.read_permission(...)`` sets the read- and write-permission for the field ``note`` to users who can add new members. Usually this permission is only granted to Site-Administrators and Managers. We use it to store information that should not be publicly visible. Please note that ``obj.note`` is still accessible in templates and python. Only using the widget (like we do in the view later) checks for the permission.
* We use no grok here

Second we create the FTI for new type in ``profiles/default/types/sponsor.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 27

    <?xml version="1.0"?>
    <object name="sponsor" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <property name="title" i18n:translate="">Sponsor</property>
     <property name="description" i18n:translate="">None</property>
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
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
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

Then we register the FTI in ``profiles/default/types.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 5

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <property name="title">Controls the available content types in your portal</property>
     <object name="talk" meta_type="Dexterity FTI"/>
     <object name="sponsor" meta_type="Dexterity FTI"/>
     <!-- -*- more types can be added here -*- -->
    </object>

After reinstalling our package we can create the new type. We use the default-view provided by dexterity for testing since we will only display the sponsors in a viewlet and not in their own page.

But we could tweak the default-view with some css to make it less ugly. Add the following to ``resources/ploneconf.css``

.. code-block:: css

    .template-view.portaltype-sponsor .named-image-widget img {
        width: 100%;
        height: auto;
    }

    .template-view.portaltype-sponsor fieldset#folder-listing {
        display: none;
    }

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

              <img tal:condition="python:getattr(context, 'advertisment', None)"
                   tal:attributes="src string:${context/absolute_url}/@@images/advertisment/preview" />

              <div tal:condition="python: 'notes' in view.w"
                   tal:content="structure view/w/notes/render">
                Notes
              </div>

            </div>
          </metal:content-core>
        </body>
        </html>

    Note how we handle the field with special permissions: ``tal:condition="python: 'notes' in view.w"`` checks if the convenience-dictionary ``w`` provided by the base-class ``DefaultView`` holds the widget for the field ``note``. If the current user does not have the permission ``cmf.ManagePortal`` it will be omited from the dictionary and get an error since ``notes`` would not be a key in ``w``. By first checking if it's missing we work around that.

Instead of writing a view you will have to display the sponsors at the bottom of the website in a viewlet.

Register the viewlet in ``browser/configure.zcml``

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

Add the viewlet-class in ``browser/viewlets.py``

.. code-block:: python
    :linenos:

    from collections import OrderedDict
    from plone import api
    from plone.app.layout.viewlets.common import ViewletBase
    from plone.memoize import ram
    from ploneconf.site.behaviors.social import ISocial
    from ploneconf.site.content.sponsor import LevelVocabulary
    from random import shuffle
    from time import time


    class SocialViewlet(ViewletBase):

        def lanyrd_link(self):
            adapted = ISocial(self.context)
            return adapted.lanyrd


    class SponsorsViewlet(ViewletBase):

        @ram.cache(lambda *args: time() // (60 * 60))  # cache for 1 hour
        def _sponsors(self):
            """Return a list of dicts with info from sponsors.
            """
            catalog = api.portal.get_tool('portal_catalog')
            brains = catalog(portal_type='sponsor')
            results = []
            for brain in brains:
                obj = brain.getObject()
                # Get the view '@@images'
                scales = api.content.get_view(
                    name='images',
                    context=obj,
                    request=self.request)
                # Scale the logo to a fixed size
                scale = scales.scale(
                    'logo',
                    width=200,
                    height=80,
                    direction='down')
                # Create the complete img-tag from the the scale-object
                tag = scale.tag() if scale else ''
                if not tag:
                    # only display sponsors with a logo
                    continue
                # Create a dict with the necessary info
                results.append(dict(
                    title=brain.Title,
                    description=brain.Description,
                    tag=tag,
                    url=obj.url or obj.absolute_url(),
                    level=obj.level
                ))
            return results

        def sponsors(self):
            # Get the list of dicts from the method above
            sponsors = self._sponsors()
            if not sponsors:
                return
            # Make sure the results are ordered
            results = OrderedDict()
            # Get all sponsoring-levels in the right order
            levels = [i.value for i in LevelVocabulary]
            for level in levels:
                level_sponsors = []
                # Add sponsors to a list level_sponsors if the level is right
                for sponsor in sponsors:
                    if level == sponsor['level']:
                        level_sponsors.append(sponsor)
                if not level_sponsors:
                    continue
                # Randomly order the sponsors in level_sponsors
                shuffle(level_sponsors)
                # {'gold': [sponsor, ...], ...} where sponsor is a dict
                results[level] = level_sponsors
            return results


* ``_sponsors`` returns a list of dictionaries containing all necessary info about sponsors.
* ``_sponsors`` is cached for an hour using `plone.memoize <http://docs.plone.org/manage/deploying/testing_tuning/performance/decorators.html#timeout-caches>`_. This way we don't need to keep all sponsor-objects in memory all the time. We could also cache until one of the sponsors is modified:

  .. code-block:: python

    ...
    def _sponsors_cachekey(method, self):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='sponsor')
        cachekey = sum([int(i.modified) for i in brains])
        return cachekey

    @ram.cache(_sponsors_cachekey)
    def _sponsors(self):
        catalog = api.portal.get_tool('portal_catalog')
    ...


* We create the complete img-tag using a custom scale (200x80) using the view ``images`` from plone.namedfile. This actually scales the logos and saves them as new blobs.
* In ``sponsors`` we return a ordered dictionary of randomized lists of dicts (containing the information on sponsors).

.. seealso::

    http://docs.plone.org/develop/plone/images/content.html#image-scales-plone-4

Add the template ``browser/templates/sponsors_viewlet.pt``

.. code-block:: xml
    :linenos:

    <div metal:define-macro="portal_sponsorbox"
         i18n:domain="ploneconf.site">
        <div id="portal-sponsorbox"
             tal:define="sponsors view/sponsors;">
            <div tal:repeat="level sponsors"
                 tal:attributes="id python:'level-' + level"
                 tal:condition="sponsors">
                <h3 tal:content="python: level.capitalize()">
                    Level
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
                <div class="visualClear"><!-- --></div>
            </div>
        </div>
    </div>

Now add some css to make it look ok. Edit ``resources/ploneconf.css``

..  code-block:: css

    .sponsor {
        float: left;
        margin: 0 1em 1em 0;
    }

    .sponsor:hover {
        box-shadow: 0 0 8px #000000;
        -moz-box-shadow: 0 0 8px #000000;
        -webkit-box-shadow: 0 0 8px #000000;
    }
