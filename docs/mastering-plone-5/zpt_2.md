---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-zpt2-label)=

# Customizing Existing Templates

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout zpt
```

Code for the end of this chapter:

```shell
git checkout zpt_2
```

{doc}`code`
````

In this part you will:

- Customize existing templates

Topics covered:

- packages (omelette)
- z3c.jbot
- date formatting and the moment pattern
- listings
- skins

To dive deeper into real Plone data we now look at some existing templates and customize them.

(plone5-zpt2-news-label)=

## The view for News Items

We want to show the date a News Item is published.
This way people can see at a glance if they are looking at current or old news.

To do this you will first customize the template that is used to render News Items.

We use {py:mod}`z3c.jbot` for overriding templates.
The package already has the necessary configuration in {file}`browser/configure.zcml`.

Find the file {file}`newsitem.pt` in {file}`packages/plone/app/contenttypes/browser/templates/`
(in vagrant this directory is in {file}`/home/vagrant/packages`, otherwise it is in your buildout directory).

The file looks like this:

```html
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    xmlns:metal="http://xml.zope.org/namespaces/metal"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    lang="en"
    metal:use-macro="context/main_template/macros/master"
    i18n:domain="plone">
<body>

<metal:content-core fill-slot="content-core">
<metal:content-core define-macro="content-core"
                    tal:define="toc context/table_of_contents|nothing;">
  <div id="parent-fieldname-text"
      tal:condition="context/text"
      tal:content="structure python:context.text.output_relative_to(view.context)"
      tal:attributes="class python: toc and 'pat-autotoc' or ''" />
</metal:content-core>
</metal:content-core>

</body>
</html>
```

```{note}
- Like almost all Plone templates, it uses `metal:use-macro="context/main_template/macros/master"` to use the main_template
- This template fills the same slot `content-core` as the template you created in the last chapter. This means the heading and description are displayed by the `main_template`.
- The image and image caption that is provided by the behavior is not part of the template. Instead a Viewlet is used to display it.
```

Copy that file into the folder {file}`browser/overrides/` of your package. If you use vagrant you'd have to use

```shell
cp /home/vagrant/packages/plone/app/contenttypes/browser/templates/newsitem.pt /vagrant/buildout/src/ploneconf.site/src/ploneconf/site/browser/overrides/
```

- Rename the new file from {file}`newsitem.pt` to {file}`plone.app.contenttypes.browser.templates.newsitem.pt`. {py:mod}`z3c.jbot` allows you to override templates by putting a file inside a special directory with a *canonical name* (i.e. the path of the file separated by `.` plus the original filename).
- Restart Plone

Now Plone will use the new file to override the original one.

Edit the new file {file}`plone.app.contenttypes.browser.templates.newsitem.pt` and insert the following before the `<div id="parent-fieldname-text"`...:

```html
<p tal:content="python: context.Date()">
    The current Date
</p>
```

Since we use Plone 5 and Chameleon we could also write:

```html
<p>
    ${python: context.Date()}
</p>
```

- Open an existing news item in the browser

This will show something like: `2015-02-21T12:01:31+01:00`.
Not very user friendly.
Let's extend the code and use one of many helpers Plone offers.

```html
<p>
    ${python: plone_view.toLocalizedTime(context.Date())}
</p>
```

This will render `Feb 21, 2015`.

- `plone_view` is the BrowserView {py:class}`Products.CMFPlone.browser.ploneview.Plone` and it is defined in the `main_template` ({file}`Products/CMFPlone/browser/templates/main_template.pt`) of Plone 5 like this `plone_view context/@@plone;` and thus always available.
- The method {py:meth}`toLocalizedTime` runs a date object through Plone's `translation_service` and returns the Date in the current locales format, thus transforming `2015-02-21T12:01:31+01:00` to `Feb 21, 2015`.

The same in a slightly different style:

```html
<p tal:define="toLocalizedTime nocall:context/@@plone/toLocalizedTime;
               date python:context.Date()"
   tal:content="python:toLocalizedTime(date)">
        The current Date in its local short format
</p>
```

Here we first get the Plone view and then the method {py:meth}`toLocalizedTime`
and we use `nocall` to prevent the method {py:meth}`toLocalizedTime` from being called, since we want to make it available for later use.

We could also leave the formatting to the frontend.
Plone 5 comes with the [moment pattern](https://plone.github.io/mockup/dev/#pattern/moment)
that uses the library [moment.js](https://plone.github.io/mockup/dev/#pattern/moment) to format dates in the browser with JavaScript.

Try the relative calendar format:

```html
<p class="pat-moment"
   data-pat-moment="format:calendar">
    ${python: context.Date()}
</p>
```

Now we should see the date in a user friendly format like `Today at 12:01 PM`.

Experiment with other formats such as `calendar` and `LT`.

(plone5-zpt2-summary-label)=

## The Summary View

We use the view "Summary View" to list news releases.
They should also have the date.

The template associated with that view is {file}`listing_summary.pt`.

Let's look for the template:

```
plone/app/contenttypes/browser/templates/listing_summary.pt
```

The file looks like this:

```html
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    xmlns:metal="http://xml.zope.org/namespaces/metal"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    lang="en"
    metal:use-macro="context/main_template/macros/master"
    i18n:domain="plone">
<body>

<metal:content-core fill-slot="content-core">
<metal:block use-macro="context/@@listing_view/macros/content-core">

  <metal:entries fill-slot="entries">
    <metal:block use-macro="context/@@listing_view/macros/entries"
        tal:define="portal context/@@plone_portal_state/portal;
                    image_scale portal/@@image_scale">
      <metal:entry fill-slot="entry">

        <article class="tileItem">
          <h2 class="tileHeadline" metal:define-macro="listitem">
            <a class="summary url"
                tal:attributes="href item_link;
                                title item_type"
                tal:content="item_title">
              Item Title
            </a>
          </h2>

          <div metal:use-macro="context/@@listing_view/macros/document_byline"></div>

          <div tal:define="thumb_url python:item_url + '/@@images/image/' + thumb_scale_summary;"
               tal:condition="python: item_has_image and thumb_scale_summary"
               tal:attributes="class python: 'tileImage' if item_description else 'tileImageNoFloat'">
            <a tal:attributes="href item_link">
              <img tal:replace="structure python:image_scale.tag(item, 'image', scale=thumb_scale_summary, css_class='thumb-' + thumb_scale_summary)" />

            </a>
          </div>

          <div class="tileBody" tal:condition="item_description">
            <span class="description" tal:content="item_description">
              description
            </span>
          </div>

          <div class="tileFooter">
            <a tal:attributes="href item_link"
                i18n:translate="read_more">
              Read More&hellip;
            </a>
          </div>

          <div class="visualClear"><!-- --></div>

        </article>

      </metal:entry>
    </metal:block>
  </metal:entries>

</metal:block>
</metal:content-core>

</body>
</html>
```

Note the following:

- Unlike {file}`newsitem.pt` the file does not display data from a context but obviously pre-defined variables like `item`, `item_link`, `item_type` or `item_description`.
- It reuses multiple macros of a view  `context/@@listing_view`.
- The variables are most likely defined in the macro `entries` of that view.

Copy it to {file}`browser/overrides/` and rename it to {file}`plone.app.contenttypes.browser.templates.listing_summary.pt`.

Add the following after line 28:

```html
<p tal:condition="python: item_type == 'News Item'">
  ${python:plone_view.toLocalizedTime(item.Date())}
</p>
```

After you restart the instance and look at the new folder again you'll see the dates. {py:mod}`z3c.jbot` needs a restart to pick up the new file.
When you only change a existing override you don't have to restart.

The addition renders the date of the respective objects that the template iterates over
(hence `item` instead of `context` since `context` would be either a collection aggregating the news items or a folder containing a news item).

The date is only displayed if the variable `item_type` is `News Item`.

Let's take a closer look at that template. How does it know that `item_type` is the name of the content type?

The first step to uncovering that secret is line 14 of {file}`listing_summary.pt`:

```html
<metal:block use-macro="context/@@listing_view/macros/entries">
```

`use-macro` tells Plone to reuse the macro `entries` from the view `listing_view`.
That view is defined in {file}`packages/plone/app/contenttypes/browser/configure.zcml`.

It uses the template {file}`plone/app/contenttypes/browser/templates/listing.pt`.
That makes overriding that much easier.

That template {file}`listing.pt` defines the slot `entries` like this:

```xml
<metal:listingmacro define-macro="listing">
  <tal:results define="batch view/batch;
                       thumb_scale_list view/get_thumb_scale_list;
                       thumb_scale_table view/get_thumb_scale_table;
                       thumb_scale_summary view/get_thumb_scale_summary;
                       img_class python:'thumb-%s pull-right' % thumb_scale_list;
                       showicons view/show_icons">
    <tal:listing condition="batch">
      <div class="entries" metal:define-slot="entries"
          tal:define="portal context/@@plone_portal_state/portal;
                      image_scale portal/@@image_scale">
        <tal:repeat repeat="item batch" metal:define-macro="entries">
          <tal:block tal:define="obj item/getObject;
              item_url item/getURL;
              item_id item/getId;
              item_title item/Title;
              item_description item/Description;
              item_type item/PortalType;
              item_modified item/ModificationDate;
              item_created item/CreationDate;
              item_wf_state item/review_state;
              item_wf_state_class python:'state-' + view.normalizeString(item_wf_state);
              item_creator item/Creator;
              item_link python:item_type in view.use_view_action and item_url+'/view' or item_url;
              item_is_event python:view.is_event(obj);
              item_has_image python:item.getIcon;
              item_type_class python:('contenttype-' + view.normalizeString(item_type)) if showicons else '' ;
              ">
...
```

Here the `item_type` is defined as `item_type item/PortalType`.
Let's dig a little deeper and find out what `item` and  `PortalType` are.

`tal:repeat="item batch"` tells the template to iterate over an iterable `batch` which is defined as `batch view/batch`.

`view` is always the BrowserView for which the template is registered.
In our case this is either {py:class}`plone.app.contenttypes.browser.collection.CollectionView` if you called that view on a collection,
or {py:class}`plone.app.contenttypes.browser.folder.FolderView` for folders.

You might remember that both are defined in {file}`configure.zcml`

Luckily the first is a class that inherits from the second:

```python
class CollectionView(FolderView):
```

{py:meth}`batch` is a method in {py:class}`FolderView` that turns {py:obj}`results` into batches. {py:obj}`results` exists in both classes.
This means, in case the item we are looking at is a collection, the method {py:meth}`results` of {py:class}`CollectionView`,
will be used; and in case it's a folder, the one in {py:class}`FolderView`.

`batch` is a list of items.

The way it is created is actually pretty complicated and makes use of a couple of packages to create
a filtered (through {py:mod}`plone.app.querystring`) list of optimized representations (through {py:mod}`plone.app.contentlisting`) of items.

For now it is enough to know that `item` represents one of the items in the list of News Items.

The template {file}`listing_summary.pt` is extraordinary in its heavy use of nested macros.

Most of the templates you will write are much simpler and easier to read.

It can be hard to understand templates as complicated as these, but there is help to be found if you know Python: use {py:mod}`pdb` to debug templates line by line.

Add the following to line 29 just before our additions:

```
<?python import pdb; pdb.set_trace() ?>
```

When you reload the page and look at the terminal you see you have the pdb console and
can inspect the template at its current state by looking at the variable `econtext`.

You can now simply look up what `` item ` and `PortalType `` are:

```python
(pdb) pp econtext
[...]
'context': <Collection at /Plone/news/aggregator>,
'context_state': <Products.Five.metaclass.ContextState object at 0x10b7f50d0>,
'default': <object object at 0x100294c50>,
'dummy': None,
'here': <Collection at /Plone/news/aggregator>,
'isRTL': False,
'item': <plone.app.contentlisting.catalog.CatalogContentListingObject instance at /Plone/news/hot-news>,
'item_created': '2016-10-08T15:04:17+02:00',
'item_creator': 'admin',
[...]
(pdb) item = econtext['item']
(pdb) item
<plone.app.contentlisting.catalog.CatalogContentListingObject instance at /Plone/news/hot-news>
```

As discovered above, `item` is a instance of {py:class}`plone.app.contentlisting.catalog.CatalogContentListingObject`.

It has several methods and properties:

```python
(pdb) pp dir(item)
[...]
'Language',
'ModificationDate',
'PortalType',
'Publisher',
'ReviewStateClass',
'Rights',
[...]
```

`PortalType` is a method that returns the name of the item's content type.

```python
(pdb) item.PortalType()
'News Item'
```

(plone5-zpt2-finding-label)=

## Finding the right template

We changed the display of the listing of news items at <http://localhost:8080/Plone/news>.

How do we know which template to customize?

If you don't know which template is used by the page you're looking at, you can:

1. make an educated guess
2. use {py:mod}`plone.app.debugtoolbar`
3. or start a debug session

1) We could check the HTML and look for a structure in the content area that looks unique.

   We could also look for the CSS class of the body

   > ```html
   > <body class="template-summary_view portaltype-collection site-Plone section-news subsection-aggregator icons-on userrole-anonymous" dir="ltr">
   > ```

   The class `template-summary_view` tells us that the name of the view (but not necessarily the name of the template) is `summary_view`. So we could search all {file}`*.zcml`-Files for `name="summary_view"` or search all templates called {file}`summary_view.pt` and probably find the view and also the corresponding template. But only probably because it would not tell us if the template is already being overridden.

   A foolproof way to verify your guess is to modify the template and reload the page. If your modification shows up you must have found the correct file.

2) The safest method is using {py:mod}`plone.app.debugtoolbar`.
   We already have it in our buildout and only need to install it.
   It adds a "Debug" dropdown menu on top of the page.

   The section "Published" shows the complete path to the template that is used to render the page you are seeing.

   Install it now and find information about the current template in the section **Published**.

3) The debug session to find the template is a little more complicated. Since we have {py:mod}`Products.PDBDebugMode` in our buildout we can call the Browser View `pdb` on our page by appending `/pdb` to the url. We cannot put a `pdb` in the templates since we do not know (yet) which template to put the `pdb` in.

   The object that the URL points to is by default {py:obj}`self.context`.
   But the first problem is that the URL we're seeing is not the URL of the collection we want to modify.
   This is because the collection is the default page of the folder `news`.

   ```python
   >>> self.context
   <Folder at /Plone/news>
   >>> obj = self.context.aggregator
   >>> obj
   <Collection at /Plone/news/aggregator>
   >>> context_state = obj.restrictedTraverse('@@plone_context_state')
   >>> template_id = context_state.view_template_id()
   >>> template_id
   'summary_view'
   >>> view = obj.restrictedTraverse('summary_view')
   >>> view
   <Products.Five.metaclass.SimpleViewClass from /Users/philip/.cache/buildout/eggs/plone.app.contenttypes-1.1b2-py2.7.egg/plone/app/contenttypes/browser/templates/summary_view.pt object at 0x10b00cd90>
   >>> view.index.filename
   u'/Users/philip/workspace/training_without_vagrant/src/ploneconf.site/ploneconf/site/browser/template_overrides/plone.app.contenttypes.browser.templates.summary_view.pt'
   ```

   Now we see that we already customized the template using `z3c.jbot`.

   Here is a small method that could be used in a view or viewlet to display that path:

   ```python
   def get_template_path(self):
       context_state = api.content.get_view(
           'plone_context_state', self.context, self.request)
       view_template_id = context_state.view_template_id()
       view = self.context.restrictedTraverse(view_template_id)
       return view.index.filename
   ```

(plone5-zpt2-skins-label)=

## skin templates

```{only} not presentation
Why don't we always only use templates?
Because we might want to do something more complicated than get an attribute from the context and render its value in some HTML tag.

There is a deprecated technology called 'skin templates' that allows you to simply add some page template (e.g. 'old_style_template.pt')
to a certain folder in the ZMI or your egg and you can access it in the browser by opening
a URL like <http://localhost:8080/Plone/old_style_template> and it will be rendered.

But we don't use it and you too should not, even though these skin templates are still all over Plone.

Since we use {py:mod}`plone.app.contenttypes` we do not encounter many skin templates when dealing with content any more.
But more often than not you'll have to customize an old site that still uses skin templates.
```

Skin templates and Python scripts in `portal_skins` are deprecated because:

- they use restricted Python
- they have no nice way to attach Python code to them
- they are always callable for everything (they can't easily be bound to an interface)

## Summary

- Overriding templates with {py:mod}`z3c.jbot` is easy.
- Understanding templates can be hard.
- Use plone.app.debugtoolbar and pdb; they are there to help you.
- Skin templates are deprecated; you will probably only encounter them when you work on Plone 4 or older add-ons and client code.
