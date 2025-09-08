---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Theme Package VI: Using TinyMCE Templates

TinyMCE has a *templates* plugin which provides an easy way to create complex content in TinyMCE.

You can use that to help users to add complex content structures like predefined tables or content.

The users then need to customize this content to their needs.

## Create Your Own TinyMCE Templates

We already have a folder named {file}`tinymce-templates` in our theme folder.
`bobtemplates.plone` already created an example template for us, but we will add another one.

To create our first template we will add a new file named {file}`content-box.html` in this folder:

```{code-block} console
:emphasize-lines: 3

tree src/ploneconf/theme/theme/tinymce-templates
src/ploneconf/theme/theme/tinymce-templates
├── content-box.html
└── image-grid-2x2.html

0 directories, 2 files
```

In the file {file}`content-box.html` we add the following HTML template content:

```html
<div class="mceTmpl">
  <div class="row">
    <div class="box">
      <div class="col-lg-12">
        <hr>
        <h2 class="intro-text text-center">Build a website
          <strong>worth visiting</strong>
        </h2>
        <hr>
        <hr class="visible-xs">
        <p>The boxes used in this template are nested between a normal Bootstrap row and the start of your column layout. The boxes will be full-width boxes, so if you want to make them smaller then you will need to customize.</p>
        <p>A huge thanks to <a href="http://join.deathtothestockphoto.com/" target="_blank">Death to the Stock Photo</a> for allowing us to use the beautiful photos that make this template really come to life. When using this template, make sure your photos are decent. Also make sure that the file size on your photos is kept to a minumum to keep load times to a minimum.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc placerat diam quis nisl vestibulum dignissim. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.</p>
      </div>
    </div>
  </div>
</div>
```

This is the template content we will get in TinyMCE when we use this template.

In the next section we will see how we activate that template in our theme.

## Activate TinyMCE Templates Plugin

```{note}
The activation of the TinyMCE template plugin is already provided by `bobtemplates.plone`.
The only thing we have to do is to add our template to the registry in the file {file}`ploneconf.theme/src/ploneconf/theme/profiles/default/registry.xml`,
like described below.
```

If the plugin is not already activated, you can activate it using the `plone.custom_plugins` record:

```{code-block} xml
:emphasize-lines: 16-27

<?xml version="1.0"?>
<registry>
  <record name="plone.templates" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="templates">
    <field type="plone.registry.field.Text">
      <default></default>
      <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="help_tinymce_templates">Enter the list of templates in json format http://www.tinymce.com/wiki.php/Plugin:template</description>
      <required>False</required>
      <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="label_tinymce_templates">Templates</title>
    </field>
    <value>[
      {"title": "Image Grid 2x2", "url": "++theme++ploneconf-theme/tinymce-templates/image-grid-2x2.html"}
      ]
    </value>
  </record>

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
</registry>
```

In the next step we have to register our newly created TinyMCE template so we can use it in our Plone website.

To add the registration, we have to extend the `plone.templates` record:

```{code-block} xml
:emphasize-lines: 11-12

<?xml version="1.0"?>
<registry>
  <record name="plone.templates" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="templates">
    <field type="plone.registry.field.Text">
      <default></default>
      <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="help_tinymce_templates">Enter the list of templates in json format http://www.tinymce.com/wiki.php/Plugin:template</description>
      <required>False</required>
      <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="label_tinymce_templates">Templates</title>
    </field>
    <value>[
      {"title": "Image Grid 2x2", "url": "++theme++ploneconf-theme/tinymce-templates/image-grid-2x2.html"},
      {"title": "Content box", "url": "++theme++ploneconf-theme/tinymce-templates/content-box.html"}
      ]
    </value>
  </record>

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
</registry>
```

```{note}
After adding this code to the file {file}`registry.xml`, we need to restart Plone and uninstall/install our theme package add-on.
```

````{hint}
You can also add the template TTW (Trough-The-Web) in the TinyMCE control panel by updating the following snippet
(*Plugins and Toolbar* tab, *Templates* setting):

```json
[
  {
    "title": "Image Grid 2x2",
    "url": "++theme++ploneconf-theme/tinymce-templates/image-grid-2x2.html"
  },
  {
    "title": "Content box",
    "url": "++theme++ploneconf-theme/tinymce-templates/content-box.html"
  }
]
```
````

Remember to activate the plugin TTW (Through-The-Web) as well in the *Plugins and Toolbar* tab, *Custom plugins* setting:

> ```text
> template|+plone+static/components/tinymce-builded/js/tinymce/plugins/template
> ```

## Use TinyMCE Templates For Content Creation

We can add template-based content from the *Insert* menu > *Insert template*:

```{image} _static/theming-tinymce-insert-template.jpg
:align: center
```

Now we can choose one of the existing TinyMCE templates:

```{image} _static/theming-tinymce-choose-template.jpg
:align: center
```

After we have chosen our template and then clicked on *OK*, we have our template-based content in the editor:

```{image} _static/theming-tinymce-insert-template-result.jpg
:align: center
```

We can now customize it or use more templates to create more content.
