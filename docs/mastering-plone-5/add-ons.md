---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-add-ons-label)=

# Extend Plone With Add-On Packages

- There are more than 2,000 add-ons for Plone. We will cover only a handful today.
- Using them saves a lot of time
- The success of a project often depends on finding the right add-on
- Their use, usefulness, quality and complexity varies a lot

(plone5-add-ons-notable-label)=

## Some notable add-ons

[collective.easyform](https://pypi.org/project/collective.easyform)

: A form generator and the successor to [Products.PloneFormGen](https://5.docs.plone.org/develop/plone/forms/ploneformgen.html)

  ```{figure} _static/add_ons_easyform_1.png
  :alt: A simple form created with collective.easyform.
  :scale: 50%

  A simple form created with collective.easyform.
  ```

  ```{figure} _static/add_ons_easyform_2.png
  :alt: Editing a form field through the web.
  :scale: 50%

  Editing a form field through the web.
  ```

[plone.app.mosaic](https://github.com/plone/plone.app.mosaic)

: Layout solution to easily create complex layouts through the web.

[collective.geo](https://collectivegeo.readthedocs.io/en/latest/)

: Flexible bundle of add-ons to geo-reference content and display in maps

[collective.mailchimp](https://pypi.org/project/collective.mailchimp)

: Allows visitors to subscribe to mailchimp newsletters

[eea.facetednavigation](https://pypi.org/project/eea.facetednavigation/)

: Create faceted navigation and searches through the web.

[collective.lineage](https://pypi.org/project/collective.lineage)

: Microsites for Plone - makes subfolders appear to be autonomous Plone sites

[collective.behavior.banner](https://github.com/collective/collective.behavior.banner)

: Add decorative banners and sliders

[Rapido](https://rapidoplone.readthedocs.io/en/latest/)

: Allows developers with a little knowledge of HTML and a little knowledge of Python to implement custom elements and insert them anywhere they want.

[Plomino](https://github.com/plomino/Plomino)

: Powerful and flexible web-based application builder for Plone

[collective.disqus](https://pypi.org/project/collective.disqus/)

: Integrates the Disqus commenting platform API into Plone

(plone5-add-ons-find-label)=

## How to find add-ons

It can be very hard to find the right add-on for your requirements. Here are some tips:

- Make a list of required features. You'll almost never ﬁnd an add-on that exactly ﬁts your needs.

- Either adapt your requirements to what is available, invest the time & money to modify an existing add-ons to ﬁt your needs or create a new add-on that does exactly what you need.

- Then search using the follwing links below.

  - <https://plone.org/download/add-ons>
  - <https://pypi.org> >3400 Plone related packages - use the search form!
  - <https://github.com/collective> >1500 repos
  - <https://github.com/plone> >310 repos
  - Google (e.g. [Plone+Slider](https://www.google.com/?q=plone+slider))

- Once you have a shortlist test these add-ons. Here are the main issues you need to test before you install a add-on on a production site:

  - Test all required features. Read but do not trust the documentation
  - Check if the add-on runs on your required version and is currently maintained
  - Does it have i18n-support, i.e. is the user-interface translated to your language?
  - Does it uninstall cleanly?
    A tough one.
    See <https://lucafbb.blogspot.com/2013/05/how-to-make-your-plone-add-on-products.html> for the reason why.
  - Check for unwanted dependecies

Once you found an add-on you like you should ask the community if you made a good choice or if you missed something:

- Message Board: <https://community.plone.org>
- Chat: <https://plone.org/support/chat>

There is also a talk that discusses in depth how to find the right add-on: <https://www.youtube.com/watch?v=Sc6NkqaSjqw>

(plone5-add-ons-installing-label)=

## Installing Add-ons

Installation is a two-step process.

### Making the add-on packages available to Zope

First, we must make the add-on packages available to Zope. This means that Zope can import the code. Buildout is responsible for this.

Look at the {file}`buildout.cfg`.

```{note}
If you're using our Vagrant kit, the Plone configuration is available in a folder that is shared between the host and guest operating systems.
Look in your Vagrant install directory for the {file}`buildout` folder.
You may edit configuration files using your favorite text editor in the host operating system, then switch into your virtual machine to run buildout on the guest operating system.
```

In the section `[instance]` there is a variable called `eggs`, which has a list of *eggs* as a value. For example:

```
eggs =
    Plone
    collective.easyform
    plone.app.debugtoolbar
```

You add an egg by adding a new line containing the package name to the configuration.
You must write the egg name indented: this way, buildout understands that the current line is part of the last variable and not a new variable.

If you add new add-ons here you will have to run buildout and restart the site:

```shell
$ bin/buildout
$ bin/instance fg
```

Now the code is available from within Plone.

### Installing add-ons in your Plone Site

Your Plone site has not yet been told to use the add-on. For this, you have to activate the add-on in your Plone Site.

```{note}
Why the extra step of activating the add-on package? You may have multiple Plone sites in a single Zope installation. It's common to want to activate some add-ons in one site, others in another.
```

In your browser, go to Site Setup (shortcut: add `/@@overview-controlpanel` to the Plone site URL), and open the `Add-ons` Panel. You will see that you can install the add-ons there.

Install EasyForm (the human-readable name of {py:mod}`collective.easyform`) now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

- Configuring new actions
- Registering new contenttypes
- Registering css and js files
- Creating some content/configuration objects in your Plone site.

Let's have a look at what we just installed.

(plone5-add-ons-pfg-label)=

## collective.easyform

There are many ways to create forms in Plone:

- Pure: html and python in a BrowserView
- Framework: {py:mod}`z3c.form`
- TTW: {py:mod}`Products.PloneFormGen` and {py:mod}`collective.easyform`

The concept of {py:mod}`collective.easyform` is that you add a form, to which you add form fields as schema-fields exactly like the dexterity schema-editor. Fields are added, deleted, edited and moved just as with any other type of content. Form submissions may be automatically emailed and/or saved for download.

Let's build a registration form:

- Add an object of the new type 'EasyForm' in the site root. Call it "Registration"
- Save and view the result, a simple contact form that we may customize
- In the `Actions` Menu click on "Define form fields"
- Remove field "comments"
- Add fields for food preference (a choice field) and shirt size (also choice)
- In the `Actions` Menu click on "Define form actions"
- Add a new action and select "Save Data" as the type. This stores all entered data.
- Customize the mailer

```{note}
Need CAPTCHAs? Read the [instructions how to add add Recapcha-field to easyform](https://github.com/collective/collective.easyform#recaptcha-support)
```

(plone5-add-ons-ptg-label)=

## Add page layout management with {py:mod}`plone.app.mosaic`

To make it possible for your site editors to drag and drop different blocks of content onto a page, you can use the add-on plone.app.mosaic
<https://pypi.org/project/plone.app.mosaic/>

- Add `plone.app.mosaic` to the eggs section in the buildout
- Activate the Mosaic add-on
- Go to a page in your site and click on "Mosaic" in the `Display` menu in the toolbar
- Edit the page to select a Mosaic layout and try inserting some content blocks
- You can read more about the concepts and use of this add-on in the [Mosaic documentation](http://plone-app-mosaic.s3-website-us-east-1.amazonaws.com/latest/getting-started.html)

```{note}
The Mosaic editor takes some time to load so please be patient until you see the full edit view
```

(plone5-add-ons-i18n-label)=

## Internationalization

Plone can run the same site in many different languages.

We're not doing this with the conference site since the *lingua franca* of the Plone community is English.

We would use the built-in add-on <https://pypi.org/project/plone.app.multilingual> for this.

Building a multi-lingual site requires activating {py:mod}`plone.app.multilingual`, but no add-on is necessary to build a site in only one language. Just select a different site language when creating a Plone site, and all text in the user-interface will be switched to that language.

(plone5-add-ons-summary-label)=

## Summary

You are now able to customize and extend many parts of our website. You can even install extensions that add new functionality.

But:

- Can we submit talks now?
- Can we create lists with the most important properties of each talk?
- Can we allow a jury to vote on talks?

We often have to work with structured data.
Up to a degree we can do all this TTW, but at some point we run into barriers.
In the next part of the training, we'll teach you how to break through these barriers.
