---
myst:
  html_meta:
    "description": "Utilities for programming with Plone"
    "property=og:description": "Utilities for programming with Plone"
    "property=og:title": "Programming Plone"
    "keywords": "utilities, tools, techniques, programming, API"
---

(api-label)=

# Programming Plone

```{card} Backend chapter

In this part you will:

- Learn about the recommended ways to do something in backend code in Plone.
- Learn to debug

Tools and techniques covered:

- {py:mod}`plone.api`
- Portal tools
- Debugging
```


(api-api-label)=

## plone.api

The most important tool nowadays for plone developers is the add-on {doc}`plone6docs:plone.api/index` that covers 20% of the tasks any Plone developer does 80% of the time. If you are not sure how to handle a certain task, be sure to first check if `plone.api` has a solution for you.

The API is divided in five sections. Here is one example from each:

- `Content:` {ref}`plone6docs:content-create-example`
- `Portal:` {ref}`plone6docs:portal-send-email-example`
- `Groups:` {ref}`plone6docs:group-grant-roles-example`
- `Users:` {ref}`plone6docs:user-get-roles-example`
- `Environment:` {ref}`plone6docs:env-adopt-roles-example`

{py:mod}`plone.api` is a great tool for integrators and developers that is included when you install Plone, though for technical reasons it is not used by the code of Plone itself.

In existing code you'll often encounter methods that don't mean anything to you. You'll have to use the source to find out what they do.

Some of these methods are replaced by {py:mod}`plone.api`:

- {py:meth}`Products.CMFCore.utils.getToolByName` -> {py:meth}`api.portal.get_tool`
- {py:meth}`zope.component.getMultiAdapter` -> {py:meth}`api.content.get_view`

(api-portal-tools-label)=

## portal tools

Some parts of Plone are very complex modules in themselves (e.g. the versioning machinery of {py:mod}`Products.CMFEditions`).
Most of them have an API of themselves that you will have to look up when you need to implement a feature that is not covered by {py:mod}`plone.api`.

Here are a few examples:

portal_catalog

: {py:meth}`unrestrictedSearchResults()` returns search results without checking if the current user has the permission to access the objects.

: {py:meth}`uniqueValuesFor()` returns all entries in an index

portal_setup

: {py:meth}`runAllExportSteps()` generates a tarball containing artifacts from all export steps.

Products.CMFPlone.utils

: {py:meth}`is_product_installed()` checks if a product is installed.

Usually the best way to learn about the API of a tool is to look in the {file}`interfaces.py` in the respective package and read the `docstrings`. But sometimes the only way to figure out which features a tool offers is to read its code.

To use a tool, you usually first get the tool with {py:mod}`plone.api` and then invoke the method.

Here is an example where we get the tool `portal_membership` and use one of its methods to logout a user:

```python
mt = api.portal.get_tool('portal_membership')
mt.logoutUser(request)
```

```{note}
The code for {py:meth}`logoutUser()` is in {py:meth}`Products.PlonePAS.tools.membership.MembershipTool.logoutUser`. Many tools that are used in Plone are actually subclasses of tools from the package {py:mod}`Products.CMFCore`. For example `portal_membership` is subclassing and extending the same tool from {py:class}`Products.CMFCore.MembershipTool.MembershipTool`. That can make it hard to know which options a tool has. There is an ongoing effort by the Plone Community to consolidate tools to make it easier to work with them as a developer.
```

(api-debugging-label)=

## Debugging

Here are some tools and techniques we often use when developing and debugging.
We use some of them in various situations during the training.

tracebacks and the log

: The log (and the console when running in foreground) collects all log messages Plone prints.
When an exception occurs, Plone throws a traceback.
Most of the time the traceback is everything you need to find out what is going wrong.
Also adding your own information to the log is very simple.
: ```python
  import logging

  logger = logging.getLogger(__name__)

  def do_vote(user, vote):
      logger.info(f"User {user} voted with {vote}")
  ```

pdb

: The `Python` debugger `pdb` is the single most important tool for us when programming.
Just add `import pdb; pdb.set_trace()` in your code and debug away!
The code execution stops at the line you added `import pdb; pdb.set_trace()`.
Switch to your terminal and step through your code.


pdbpp

: A great drop-in replacement for pdb with tab completion, syntax highlighting, better tracebacks, introspection and more. And the best feature ever: The command {command}`ll` prints the whole current method.

ipdb

: Another enhanced pdb with the power of IPython, e.g. tab completion, syntax highlighting, better tracebacks and introspection. It also works nicely with {py:mod}`Products.PDBDebugMode`. Needs to be invoked with `import ipdb; ipdb.set_trace()`.

Products.PDBDebugMode

: An add-on that has two killer features.

  **Post-mortem debugging**: throws you in a pdb whenever an exception occurs. This way you can find out what is going wrong.

  **pdb view**: simply adding `/pdb` to a url drops you in a pdb session with the current context as {py:obj}`self.context`. From there you can do just about anything.

Interactive debugger

: Start your instance in debug mode with  
  ```shell
  venv/bin/zconsole debug instance/etc/zope.conf
  ```
  You have an interactive debugger at your fingertips.
  `app.Plone` is your Plone instance object which you can inspect on the command line.
: To list the ids of the objects in a folderish object:
  ```shell
  >>> app.Plone.talks.keys()
  ['whats-new-in-python-3.10', 'plone-7', 'zope', 'betty-white', 'new-years-day', 'journey-band']
  ```
: To list the items of a folderish object:
  ```shell
  >>> from zope.component.hooks import setSite
  >>> setSite(app.Plone)
  >>> app.Plone.talks.contentItems()
  [('whats-new-in-python-3.10', <Talk at /Plone/talks/whats-new-in-python-3.10>), ('plone-7', <Talk at /Plone/talks/plone-7>), ('zope', <Talk at /Plone/talks/zope>), ('betty-white', <Talk at /Plone/talks/betty-white>), ('new-years-day', <Talk at /Plone/talks/new-years-day>), ('journey-band', <Talk at /Plone/talks/journey-band>)]
  ```
: Setting the site with `setSite` is necessary because the root object when starting the interactive debugger is `app`, which can contain more than just one Plone instance object.
We choose our Plone instance with id `Plone`.
With setting the site to operate on, we have access to the Zope component registry.
The component registry is needed for methods like `contentItems` which look up utilities and other components like in this case the `ITypesTool.`
: Stop the interactive shell with {kbd}`ctrl d`.

plone.app.debugtoolbar

: An add-on that allows you to inspect nearly everything. It even has an interactive console, a tester for TALES-expressions and includs a reload-feature like {py:mod}`plone.reload`.

plone.reload

: An add-on that allows to reload code that you changed without restarting the site.
Open http://localhost:8080/@@reload in your browser for `plone.reload`s UI.
It is also used by {py:mod}`plone.app.debugtoolbar`.

Products.PrintingMailHost

: An add-on that prevents Plone from sending mails. Instead, they are logged.

`verbose-security = on`

: An option for the recipe {py:mod}`plone.recipe.zope2instance` that logs the detailed reasons why a user might not be authorized to see something.

Sentry

: [Sentry](https://github.com/getsentry/sentry) is an error logging application you can host yourself.
It aggregates tracebacks from many sources and (here comes the killer feature) even the values of variables in the traceback. We use it in all our production sites.


```{seealso}
- ["What You Need To Know About Python Debugging" by Philip Bauer](https://www.youtube-nocookie.com/embed/_OB6VlYKZkU?privacy_mode=1)
- ["PDB Like a Pro" by Philip Bauer](https://www.youtube-nocookie.com/embed/yOG36Ae_TJ0?privacy_mode=1)
```


## Exercise 1

Knowing that `venv/bin/zconsole debug instance/etc/zope.conf` basically offers you a Python prompt to inspect your Plone instance, how would you start to explore Plone?

```{admonition} Solution
:class: toggle

Use `locals()` or `locals().keys()` to see Python objects available in Plone

You will get notified that `app` is automatically bound to your Zope application, so you can use dictionary-access or attribute-access as explained in {doc}`what_is_plone` to inspect the application:
```

## Exercise 2

The `app` object you encountered in the previous exercise can be seen as the root of Plone. Once again using Python, can you find your newly created Plone site?

`````{admonition} Solution
:class: toggle

`app.keys()` will show `app`'s attribute names - there is one called `Plone`, this is your Plone site object. Use `app.Plone` to access and further explore it.

```pycon
>>> app
<Application at >
>>> app.keys()
['browser_id_manager', 'session_data_manager', 'error_log', 'temp_folder', 'virtual_hosting', 'index_html', 'Plone', 'acl_users']
>>> portal = app["Plone"]
>>> from zope.component.hooks import setSite
>>> setSite(portal)
>>> portal
<PloneSite at /Plone>
>>> portal.keys()
['portal_setup', 'MailHost', 'caching_policy_manager', 'content_type_registry', 'error_log', 'plone_utils', 'portal_actions', 'portal_catalog', 'portal_controlpanel', 'portal_diff', 'portal_groupdata', 'portal_groups', 'portal_memberdata', 'portal_membership', 'portal_migration', 'portal_password_reset', 'portal_properties', 'portal_registration', 'portal_skins', 'portal_types', 'portal_uidannotation', 'portal_uidgenerator', 'portal_uidhandler', 'portal_url', 'portal_view_customizations', 'portal_workflow', 'translation_service', 'mimetypes_registry', 'portal_transforms', 'portal_archivist', 'portal_historiesstorage', 'portal_historyidhandler', 'portal_modifier', 'portal_purgepolicy', 'portal_referencefactories', 'portal_repository', 'acl_users', 'portal_resources', 'portal_registry', 'HTTPCache', 'RAMCache', 'ResourceRegistryCache', 'talks', 'sponsors']
>>> app['Plone']['talks']
<Folder at /Plone/talks>
>>> app.Plone.talks
<FolderishDocument at /Plone/talks>
```


````{note}
Plone and its objects are stored in an object database, the {term}`ZODB`.
You can use `venv/bin/zconsole debug instance/etc/zope.conf` as a database client (in the same way e.g. `psql` is a client for PostgreSQL).
Instead of a special query language (like SQL) you simply use Python to access and manipulate ZODB objects.
Don't worry if you accidentally change objects - you would have to commit your changes explicitly to make them permanent.

The Python code to do so is:

```pycon
>>> import transaction
>>> transaction.commit()
```

You have been warned.
````
`````




## Exercise 3

- Create a new BrowserView callable as `/@@demo_content` in a new file {file}`demo.py`.
- The view should create five talks each time it is called.
- Use the documentation at {doc}`plone6docs:plone.api/content` to find out how to create new talks.
- Use `plone.api.content.transition` to publish all new talks. Find the documentation for this method.
- Only managers should be able to use the view (the permission is called `cmf.ManagePortal`).
- Display a message about the results (see {ref}`plone6docs:portal-show-message-example`).
- For extra credits use the library [requests](https://requests.readthedocs.io/en/latest/) and [Wikipedia](https://www.mediawiki.org/wiki/Wikimedia_REST_API) to populate the talks with content.
- Use the utility methods `cropText` from `Producs.CMFPlone` to crop the title after 20 characters.
  Use the documentation at {doc}`plone6docs:backend/global-utils` to find an overview of `plone_view` helpers.

```{note}
- Do not try everything at once, work in small iterations, restart your Plone instance to check your results frequently.
- Use `pdb` during development to experiment.
```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Add this to {file}`browser/configure.zcml`:

```{code-block} xml
:linenos:

<browser:page
  name="create_demo_talks"
  for="*"
  class=".demo.DemoContent"
  permission="cmf.ManagePortal"
  />
```

This is {file}`browser/demo.py`:

```{code-block} python
:linenos:

from Products.Five import BrowserView
from plone import api

from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

import json
import logging
import requests

logger = logging.getLogger(__name__)


class DemoContent(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        self.create_talks()
        return self.request.response.redirect(portal.absolute_url())

    def create_talks(self, amount=3):
        """Create some talks"""

        alsoProvides(self.request, IDisableCSRFProtection)
        plone_view = api.content.get_view("plone", self.context, self.request)
        wiki_content = self.get_wikipedia_content_of_the_day()
        for data in wiki_content[:amount]:
            talk = api.content.create(
                container=self.context,
                type="talk",
                title=plone_view.cropText(data["titles"]["normalized"], length=20),
                description=data["description"],
                type_of_talk="talk",
            )
            api.content.transition(talk, to_state="published")
            logger.info(f"Created talk {talk.absolute_url()}")
        api.portal.show_message(f"Created {amount} talks!", self.request)

    def get_wikipedia_content_of_the_day(self):
        wiki = requests.get(
            "https://en.wikipedia.org/api/rest_v1/feed/featured/2022/01/02"
        )
        return json.loads(wiki.text)["mostread"]["articles"]
```

Some notes:

- Since calling view is a GET and not a POST we need {py:meth}`alsoProvides(self.request, IDisableCSRFProtection)` to allow write-on-read without Plone complaining.
  Alternatively we could create a simple form and create the content on submit.

- {ref}`plone6docs:content-transition-example` has two modes of operation:
  The documented one is `api.content.transition(obj=foo, transition='bar')`.
  That mode tries to execute that specific transition.
  But sometimes it is better to use `to_state` which tries to to find a way to get from the current state to the target state.
  Follow the link to the method description in documentation to find more information on `transition`.

- To use methods like `cropText` from another browser view, you can get the view for your context with `api.content.get_view("view_name", self.context, self.request)`

- Here the description of the talk is set. To add text, you need to create an instance of `RichTextValue` and set it as an attribute:

  ```python
  from plone.app.textfield.value import RichTextValue
  talk.details = RichTextValue(data["extract"], 'text/plain', 'text/html',)
  ```
````
