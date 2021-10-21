---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Create a Theme from scratch

We’re going to create a theme for Plone 6 Classic UI that is built from scratch. There are no dependencies except Bootstrap.

This package will allow you to change and extend the look of Plone to your needs. You will develop on the filesystem. You can add your package to any code repository e.g. GitHub and re-use it on different Plone sites.

**Use Case**
- Your own theme package
- You'll create a theme for Plone Classic UI
- You'll use Bootstrap as basis
- You'll compile your own CSS

**What you will learn**
- How to prepare your development setup
- How to create your theme package using plonecli
- How to add a theme to your package using plonecli
- What are the important parts of your theme
- How to add and compile your styles


# Requirements

Check out the requirements of the theming training. You have to bring a linux based laptop (Ubuntu, macOS) with code editor of your choice (we recommend VS Code) and with Plone installed as described in training instructions. It is extremely important that you join the class with a working Plone installation. You need npm(package manager) to build your CSS/JavaScript.


# Create an add-on package

We're going to create an add-on package for our theme. We'll use plonecli for the next steps. It uses mr.bob and it's templates. There is a template to create our add-on. There are templates to add the theme to the package in the following steps.

The package contains the theme and is developed on the filesystem. Development and compilation are done locally.

Create a add-on package for your theme using plonecli in the current folder:

```{code-block} shell
$ plonecli create addon plonetheme.munich
```

```{note}
Check the output on your console. Lines starting with **RUN** shows you the actual command that is fired in the background.

RUN: mrbob bobtemplates.plone:addon -O ./plonetheme.training
```

You're going to be asked some questions. It's good to go with defaults for now. Since there is work in progress, Plone version `5.2.2` will result in Plone 6.0. Don't bother with that.

```{note}
--> Package description [An add-on for Plone]: 

--> Plone version [5.2.2]: 

--> Python version for virtualenv [python3]: 

--> Do you want me to activate VS Code support? (y/n) [y]: 
```

```{note}
plonecli asks you to create or update a local git repository after some steps. Yes is a good option.
```

# Create theme

In the next steps we're going to add a theme to our package. We'll use plonecli for that again. We will use the template `theme_basic` here.

## Step into package directory

```{code-block} shell
$ cd plonetheme.munich
```

## Add theme using theme_barceloneta template

Run the command inside your package:

```{code-block} shell
$ plonecli add theme_basic
```

There are different theme templates available. As shown in the prevous chapter `theme_barceloneta` is built on top of the Barceloneta Theme. Our `theme_basic` is a more generic approach:

* No dependencies to Barceloneta
* Since there is no rules.xml Diazo is disabled
* All templates are served without modification
* Markup in Plone Classic UI is mostly Boostrap
* You have to take care of some aspects e.g. columns


# Build Instance

Get your instance up and running. The build command of plonecli will run a couple of commands for you. Green bars shows you what actual command has been fired.

* It creates a python3 virtualenv
* It installs all dependencies using pip
* It will bootstrap the buildout of the Zope applicaton server
* It will run the actual buildout

Start the build process by running `plonecli build` in your terminal

```{code-block} shell
$ plonecli build
```

## Output

The output on our console should contain the following steps:

```{code-block} shell
RUN: python3 -m venv venv

RUN: ./venv/bin/pip install -r requirements.txt --upgrade

RUN: ./venv/bin/buildout bootstrap

RUN: ./venv/bin/buildout
```

If everything works as expected next step is to start up your instance for the first time.


# Startup

We recommend to swith to your SDK here. If you're using Visual Studio Code you can open a terminal `Terminal > New Terminal` and run the folloing commands inside your editor. This helps you to keep track of windows and processes.

Start your instance for the very first time:

```{code-block} shell
./bin/instance fg
```

```{note}
The command starts an instance of the Zope application server in foreground. This turns on the debug mode automatically. If everything starts as expected you should see something like that on your console:

2078-12-24 19:37:49,830 INFO [waitress:485][MainThread] Serving on http://0.0.0.0:8080/

```

## Login

Open your browser and navigate to Zope's management interface:

http://localhost:8080/manage

This will ask you for login credentials:

* Username: admin
* Password: admin

TODO: Screenshot


# Add your first Plone Site

Since your're logged in now you can add a Plone instance:

http://localhost:8080/

Scroll down to your package and activate the checkbox next to it. This will create new Plone site and install our add-on. Since the theme is part of the add-on it has been activated automatically.

You see some basic styling because a precompiled theme.css has been shipped with the template. Bevor we start theming we're going to add a copy of the main template to our theme package.


# Override Main Template

Copy the page template from `parts/omelette/Products/CMFPlone/browser/templates/main_template.pt` to `src/plonetheme/munich/browser/templates/main_template.pt`.

Copy the main template python file from `parts/omelette/Products/CMFPlone/browser/main_template.py` to `src/plonetheme/munich/browser/main_template.py`.

Register the template:

```{code-block} shell
  <browser:page
      for="*"
      name="main_template"
      class=".main_template.MainTemplate"
      permission="zope.Public"
      layer="plonetheme.munich.interfaces.IPlonethemeMunichLayer"
      />
```

In the next step we'll make use of Bootstrap's grid system and add some columns to our main template.

## Conflicts

If you try to register templates that already exists in Plone under the same name you'll get a `ConfigurationConflictError`. You can avoit this by adding a theme layer to your configuration as seen in the above example.

```{code-block} shell
zope.configuration.config.ConfigurationConflictError: Conflicting configuration actions
  For: ('view', (None, <InterfaceClass zope.publisher.interfaces.browser.IDefaultBrowserLayer>), 'main_template', <InterfaceClass zope.publisher.interfaces.browser.IBrowserRequest>)
    File "/Users/jdoe/.buildout/eggs/Products.CMFPlone-6.0.0a1.dev1-py3.7.egg/Products/CMFPlone/browser/configure.zcml", line 91.2-96.8
        <browser:page
            for="*"
            name="main_template"
            class=".main_template.MainTemplate"
            permission="zope.Public"
            />
    File "/Users/jdoe/Development/plonetheme.munich/src/plonetheme/munich/browser/configure.zcml", line 21.2-26.8
        <browser:page
            for="*"
            name="main_template"
            class=".main_template.MainTemplate"
            permission="zope.Public"
            />
 ``` 


# Add Columns

Le's make use of Bootstrap's layout system and add a `container`, a `row` and some `columns`. Theck out the [Bootstrap documentation] if your're nof familiar with that.

```{code-block} html
<metal:page define-macro="master">
<tal:doctype tal:replace="structure string:&lt;!DOCTYPE html&gt;" />

<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      tal:define="portal_state python:context.restrictedTraverse('@@plone_portal_state');
          context_state python:context.restrictedTraverse('@@plone_context_state');
          plone_view python:context.restrictedTraverse('@@plone');
          icons python:context.restrictedTraverse('@@iconresolver');
          plone_layout python:context.restrictedTraverse('@@plone_layout');
          lang python:portal_state.language();
          view nocall:view | nocall: plone_view;
          dummy python: plone_layout.mark_view(view);
          portal_url python:portal_state.portal_url();
          checkPermission python:context.restrictedTraverse('portal_membership').checkPermission;
          site_properties python:context.restrictedTraverse('portal_properties').site_properties;
          ajax_include_head python:request.get('ajax_include_head', False);
          ajax_load python:False;"
      i18n:domain="plone"
      tal:attributes="lang lang;">

    <metal:cache tal:replace="structure provider:plone.httpheaders" />

  <head>
    <meta charset="utf-8" />
    <div tal:replace="structure provider:plone.htmlhead" />
    <metal:topslot define-slot="top_slot" />
    <metal:headslot define-slot="head_slot" />
    <metal:styleslot define-slot="style_slot" />
    <div tal:replace="structure provider:plone.scripts" />
    <metal:javascriptslot define-slot="javascript_head_slot" />
    <link tal:replace="structure provider:plone.htmlhead.links" />
    <meta name="generator" content="Plone - http://plone.com" />
  </head>

  <body tal:define="isRTL portal_state/is_rtl;
                    sl python:plone_layout.have_portlets('plone.leftcolumn', view);
                    sr python:plone_layout.have_portlets('plone.rightcolumn', view);
                    body_class python:plone_layout.bodyClass(template, view);"
        tal:attributes="class body_class;
                        dir python:isRTL and 'rtl' or 'ltr';
                        python:plone_view.patterns_settings()"
        id="visual-portal-wrapper">

    <div tal:replace="structure provider:plone.toolbar" />

    <header id="portal-top" i18n:domain="plone">
      <div tal:replace="structure provider:plone.portaltop" />
    </header>

    <div id="portal-mainnavigation" tal:content="structure provider:plone.mainnavigation">
      The main navigation
    </div>

    <section id="global_statusmessage">
      <tal:message tal:content="structure provider:plone.globalstatusmessage"/>
      <div metal:define-slot="global_statusmessage"></div>
    </section>

    <div id="viewlet-above-content" tal:content="structure provider:plone.abovecontent" />

    <div class="container">
      <div class="row">

        <div class="col-lg-8">

          <article id="portal-column-content">

            <metal:block define-slot="content">

            <metal:content metal:define-macro="content">

              <metal:slot define-slot="body">

                <article id="content">

                  <metal:bodytext define-slot="main">

                    <header>

                      <div id="viewlet-above-content-title" tal:content="structure provider:plone.abovecontenttitle" />

                      <metal:title define-slot="content-title">
                        <h1 tal:replace="structure context/@@title" />
                      </metal:title>

                      <div id="viewlet-below-content-title" tal:content="structure provider:plone.belowcontenttitle" />

                      <metal:description define-slot="content-description">
                        <p tal:replace="structure context/@@description" />
                      </metal:description>

                      <div id="viewlet-below-content-description" tal:content="structure provider:plone.belowcontentdescription" />

                    </header>

                    <div id="viewlet-above-content-body" tal:content="structure provider:plone.abovecontentbody" />

                    <div id="content-core">
                      <metal:text define-slot="content-core" tal:content="nothing">
                        Page body text
                      </metal:text>
                    </div>

                    <div id="viewlet-below-content-body" tal:content="structure provider:plone.belowcontentbody" />

                  </metal:bodytext>
                  <footer>
                    <div id="viewlet-below-content" tal:content="structure provider:plone.belowcontent" />
                  </footer>
                </article>
              </metal:slot>
            </metal:content>

            </metal:block>
          </article>

        </div>

        <div class="col-lg-4">

          <aside id="portal-column-one" metal:define-slot="column_one_slot" tal:condition="sl">
            <metal:portlets define-slot="portlets_one_slot">
              <tal:block replace="structure provider:plone.leftcolumn" />
            </metal:portlets>
          </aside>

          <aside id="portal-column-two" metal:define-slot="column_two_slot" tal:condition="sr">
            <metal:portlets define-slot="portlets_two_slot">
              <tal:block replace="structure provider:plone.rightcolumn" />
            </metal:portlets>
          </aside>

        </div>

      </div>
    </div>

    <footer id="portal-footer-wrapper" i18n:domain="plone">
      <div tal:replace="structure provider:plone.portalfooter" />
    </footer>

  </body>
</html>

</metal:page>
```

This is an example of the main template at the point of time when the documentation has been written. We recommend to copy over the main template from your actual code or grab it from GitHub to get the newest version:

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/templates/main_template.pt

```{note}
It's possible to archive this with mixins as well. Check out Barceloneta's [grid.scss] for this.
```


# Build Process

No we have everything in place to start theming. Let's start with compiling our actual CSS from the given SASS files.

## Install dependencies

Step into the theme folder of your package:

```{code-block} shell
$ cd ./src/plonetheme/munich/theme
```

Run `npm install` to add dependencies from package.json::

```{code-block} shell
$ npm install
```

## Compile resources

Run `npm run build` to add dependencies from package.json::

```{code-block} shell
$ npm run build
```

This will compile your `scss/theme.scss` into `css/theme.css`. A minified
version will be created as well. Check out the scripts section from
`package.json` so see what happens exactly.

## Watch for changes

Run `npm run watch` to automatically compile when a file has been changed::

```{code-block} shell
$ npm run watch
```    

With `npm run watch` you start the build process automatically when you save a file.


# Happy Theming

We can start theming finally. Let's change some colors now.

## Change Colors

Go to scss/theme.scss

Change primary and secondary colors:

```{code-block} shell
$primary: #456990;
$secondary: #49BEAA;
```    

Watch will start the build process as soon as you save your file. Check out your console output. After it has been finished, go to your browser and reload the window.

TODO: Screenshot Changed Colors

```{note}
Open the developer tools of your browser and navigate to the network tab. Disabling the cache is your fiend.
```

[grid.scss]: https://github.com/plone/plonetheme.barceloneta/blob/master/scss/grid.scss
[Bootstrap documentation]: https://getbootstrap.com/docs/5.1/getting-started/introduction/