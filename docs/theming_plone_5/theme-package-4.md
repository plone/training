---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Theme Package IV: Creating And Customizing Plone Templates

In the previous sections we {doc}`created our custom theme <theme-package-2>` and {doc}`customized it using CSS <theme-package-3>`.
But sometimes CSS isn't enough, sometimes we have to adjust the HTML markup.

If we don't want to use Diazo rules and {term}`XSLT` for it, there is another way: customizing templates.

In this section we will show you how you can customize existing templates and create new ones specific for your theme.

## Overriding A Plone Template

A large part of the Plone UI is provided by *BrowserView* and *Viewlet* templates.

You can see all viewlets and their managers (sortable containers) when you view the URL `./@@manage-viewlets`.

```{note}
To override them from the ZMI, you can go to `./portal_view_customizations`.
But this is very limited and does not work for all views.
```

To override them from your theme product, the best way is to use `z3c.jbot` (Just a Bunch of Templates).

Since jbot is already included in the `bobtemplates.plone` theme skeleton via `plone.app.themingplugins`,
you can start using it immediately by adding all the templates you want to override in the {file}`src/ploneconf/theme/theme/template-overrides` directory.

In order for jbot to match the override to the template which is being overridden,
the name of the *new* template needs to include the complete path to the original template as a prefix (with every `/` replaced by a `.`).

For instance, to override the {file}`path_bar.pt` template (the breadcrumbs) from `plone.app.layout`, knowing that this template is found in a sub folder named `viewlets`, you need to name the overriding template {file}`plone.app.layout.viewlets.path_bar.pt`.

```{hint}
Clicking the template in ZMI > portal_view_customizations is a handy way to find the template path. You can also copy the original template's code here.
```

When a new override has been added, the Plone instance needs to be restarted.
After this, a page reload is enough to see any changes to the template.

### Example: Overriding The Event Item Template

The path to the original template is {file}`plone/app/event/browser/event_view.pt`,
the full dotted name for our replacement template should be: {file}`plone.app.event.browser.event_view.pt`.

Create a new file with this dotted name into the {file}`template-overrides` folder.

Let's say we want to move the full text of the event item to appear before the event details block.
To do this, we copy over the original template code and change the order of the two blocks:

```{code-block} xml
:emphasize-lines: 22-24

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="plone.app.event">
  <body>

    <metal:content-core fill-slot="content-core">
      <metal:block define-macro="content-core">
        <tal:def tal:define="data nocall:view/data">
          <div class="event clearfix" itemscope="itemscope" itemtype="http://data-vocabulary.org/Event">
            <ul class="hiddenStructure">
              <li><a itemprop="url" class="url" href="" tal:attributes="href data/url" tal:content="data/url">url</a></li>
              <li itemprop="summary" class="summary" tal:content="data/title">title</li>
              <li itemprop="startDate" class="dtstart" tal:content="data/start/isoformat">start</li>
              <li itemprop="endDate" class="dtend" tal:content="data/end/isoformat">end</li>
              <li itemprop="description" class="description" tal:content="data/description">description</li>
            </ul>

            <div id="parent-fieldname-text" tal:condition="data/text">
              <tal:text content="structure data/text" />
            </div>

            <tal:eventsummary replace="structure context/@@event_summary" />
          </div>
        </tal:def>
      </metal:block>
    </metal:content-core>
  </body>
</html>
```

You can now restart Plone and view an event to see the effect.

```{hint}
If your buildout is using `omelette`, you can find the original template in {file}`buildout/parts/omelette/plone/app/event/browser`.
```

## Creating A New Plone Template

(create-dynamic-slider-content-in-plone)=

### Create Dynamic Slider Content In Plone

To render our dynamic content for the slider we need a custom view in Plone.
There are various ways to create views.

For now, we will use a very simple template-only-view via `jbot` and `themingplugins`.
The `bobtemplates.plone` skeleton includes already everything you need.

The only thing we need to do, is to add a template file in the {file}`theme/views` folder.
Here we create a template file named {file}`slider-images.pt`.

And we already have this file as an example.

The only thing we need to do is to rename the file {file}`slider-images.pt.example` to {file}`slider-images.pt`.

```console
tree src/ploneconf/theme/theme/views/
src/ploneconf/theme/theme/views/
└── slider-images.pt.example

0 directories, 1 file
```

The template code looks like this:

```xml
<div id="carousel-example-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators hidden-xs">
    <li tal:repeat="item context/keys"
        data-target="#carousel-example-generic"
        data-slide-to="${python:repeat.item.index}"
        class="${python: repeat.item.start and 'active' or ''}"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div tal:repeat="item context/values"
         class="item ${python: repeat.item.start and 'active' or ''}">
      <img tal:define="scales item/@@images"
           tal:replace="structure python: scales.tag('image', scale='large', css_class='img-responsive img-full')" />
    </div>
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
    <span class="icon-prev"></span>
  </a>
  <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
    <span class="icon-next"></span>
  </a>
</div>
```

This is all that's required to create a very simple template-only view.
You can test the view after restarting your Plone instance.

For the view to show up, it needs some images to display.
To supply the images, we have to create a folder in Plone named `slider-images` and add some images there.

```{note}
We will show you later how to {ref}`create initial content for the theme <creating-initial-content-for-the-theme>`
```

Now we can browse to the View on this folder by visiting: <http://localhost:8080/Plone/slider-images/@@slider-images>.
This will render the markup required to render the slider.

### Use The Dynamic Slider Content From Plone

Now that we have our `slider-images` view which renders our HTML markup for the slider, we need to replace that with the static markup in our template.

For that we use Diazo's ability to load the content from other URLs, using the `href` attribute in our {file}`rules.xml`.

We also make use of the `css:if-content` attribute to make sure it is only on the front page:

```{code-block} xml
:emphasize-lines: 2-7

<!-- Front Page Slider -->
<replace
    css:theme="#carousel-example-generic"
    css:content="#carousel-example-generic"
    href="/slider-images/@@slider-images"
    css:if-content=".section-front-page"
    />
<drop
    css:theme="#front-page-slider"
    css:if-not-content=".section-front-page"
    />
```
