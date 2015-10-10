=======================
Using TinyMCE templates
=======================

Activate TinyMCE templates plugin
=================================

.. code-block:: xml

   <record name="plone.custom_plugins" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="custom_plugins">
       <field type="plone.registry.field.List">
         <default/>
         <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="">Enter a list of custom plugins which will be loaded in the editor. Format is pluginname|location, one per line.</description>
         <required>False</required>
         <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="">Custom plugins</title>
         <value_type type="plone.registry.field.TextLine"/>
       </field>
       <value>
         <element>template|+plone+static/components/tinymce-builded/js/tinymce/plugins/template</element>
       </value>
   </record>

Create your own TinyMCE templates
=================================

.. code-block:: xml

   <record name="plone.templates" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="templates">
     <field type="plone.registry.field.Text">
       <default></default>
       <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="help_tinymce_templates">Enter the list of templates in json format                 http://www.tinymce.com/wiki.php/Plugin:template</description>
       <required>False</required>
       <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="label_tinymce_templates">Templates</title>
     </field>
     <value>[ &#13;
     {&#13;
         "title": "Content box", &#13;
         "url": "++theme++plonetheme.tango/tinymce_templates/content-box.html"}&#13;
   ]</value>
   </record>


