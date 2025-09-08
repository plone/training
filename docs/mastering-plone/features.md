---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(features-label)=

# The Features of Plone

```{seealso}
[Plone documentation **docs.plone.org**](https://6.docs.plone.org/)

[Chapter "Working with content" on docs.plone.org](https://5.docs.plone.org/working-with-content/index.html)
```


(features-start-stop-label)=

## Starting and Stopping Plone

We control Plone with a makefile:

```shell
$ make start
```

You can stop it by pressing {kbd}`ctrl + c`.

On a decent laptop it should take under 10 seconds untill you see the output ``Ready to handle requests``

A standard installation listens on port 8080, so lets have a look at <http://localhost:8080>

```{figure} _static/features_plone_running.png
```

As you can see, there is no Plone site yet!

(features-create-plonesite-label)=

## Creating a Plone Site

We now have a running Zope with a database but no content.
But luckily there is a button to create a Plone site.

Click on the link {guilabel}`Create a new Plone site`.
If the site asks you to login, use login `admin` and password `secret` (they are taken from the file `instance.yaml`).

```{figure} _static/features_create_site_form.png
```

You will be automatically redirected to the new site.

This is how the frontpage should look like:

```{figure} _static/frontpage_plone.png
```

```{note}
Plone has many message boxes.
They contain important information.
Read them and make sure you understand them!
```

## Starting and Stopping the frontend

To start the frontend that will use your new plone site go to the folder `frontend` and enter:

```shell
$ yarn start
```

If you open <http://localhost:3000> you will see the front page of the Plone site in Volto.

```{figure} _static/frontpage_volto.png
```

You can stop the frontend anytime using {kbd}`ctrl + c`.

While developing it is not necessary to restart the frontend unless you are adding a new file.

### Exercises

#### Exercise 1

Open the file `backend/instance/etc/zope.ini` in your favorite editor.
Now let's say you want Plone to listen on port 9080 instead of the default 8080.
How could you do this?

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```ini
[server:main]
use = egg:waitress#main
listen = localhost:8080
threads = 4
clear_untrusted_proxy_headers = false
max_request_body_size = 1073741824
```

Change the address to `localhost:9080` and restart your instance.

You will also have to tell the frontend that the backend is now running on a different port!

You need to change the environment variable `RAZZLE_DEV_PROXY_API_PATH` to the base-url of the backend:

```shell
$ RAZZLE_DEV_PROXY_API_PATH=http://localhost:9080/Plone yarn start
```

When your Plone instance is not called `Plone` you can use the same approach:

```shell
$ RAZZLE_DEV_PROXY_API_PATH=http://localhost:8080/mysite yarn start
```


````

#### Exercise 2

Knowing that `venv/bin/zconsole debug instance/etc/zope.conf` basically offers you a Python prompt, how would you start to explore Plone?

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Use `locals()` or `locals().keys()` to see Python objects available in Plone

You will get notified that `app` is automatically bound to your Zope application, so you can use dictionary-access or attribute-access as explained in {doc}`what_is_plone` to inspect the application:
```

#### Exercise 3

The `app` object you encountered in the previous exercise can be seen as the root of Plone. Once again using Python, can you find your newly created Plone site?

`````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

`app.__dict__.keys()` will show `app`'s attribute names - there is one called `Plone`, this is your Plone site object. Use `app.Plone` to access and further explore it.

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
>>> app.Plone.keys()
['portal_setup', 'MailHost', 'caching_policy_manager', 'content_type_registry', 'error_log', 'plone_utils', 'portal_actions', 'portal_catalog', 'portal_controlpanel', 'portal_diff', 'portal_groupdata', 'portal_groups', 'portal_memberdata', 'portal_membership', 'portal_migration', 'portal_password_reset', 'portal_properties', 'portal_quickinstaller', 'portal_registration', 'portal_skins', 'portal_types', 'portal_uidannotation', 'portal_uidgenerator', 'portal_uidhandler', 'portal_url', 'portal_view_customizations', 'portal_workflow', 'translation_service', 'portal_form_controller', 'mimetypes_registry', 'portal_transforms', 'portal_archivist', 'portal_historiesstorage', 'portal_historyidhandler', 'portal_modifier', 'portal_purgepolicy', 'portal_referencefactories', 'portal_repository', 'acl_users', 'portal_resources', 'portal_registry', 'HTTPCache', 'RAMCache', 'ResourceRegistryCache', 'training', 'schedule', 'location', 'sponsors', 'sprint']
>>> app['Plone']['news']
<Folder at /Plone/news>
```


````{note}
Plone and its objects are stored in an object database, the ZODB. You can use `bin/instance debug` as a database client (in the same way e.g. `psql` is a client for PostgreSQL). Instead
of a special query language (like SQL) you simply use Python to access and manipulate ZODB objects. Don't worry if you accidentally change objects in `bin/instance debug` - you would have to commit
your changes explicitly to make them permanent. The Python code to do so is:

```pycon
>>> import transaction
>>> transaction.commit()
```

You have been warned.
````
`````

#### Exercise 4

Change the port of the frontend to 1234

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

By default the frontend will start on port 3000. You can change the port and/or hostname for the frontend by specifying the environment variables `PORT` and/or `HOST`:

> \$ HOST=localhost PORT=1234 yarn start
```

(features-walkthrough-label)=

## Walkthrough of the UI

Let's see what is there...

- {guilabel}`header`:

  - {guilabel}`logo`: with a link to the front page
  - {guilabel}`searchbox`: search (with live-search)

- {guilabel}`navigation`: The global navigation

- {guilabel}`portal-footer`: portlets for the footer, site actions, and colophon

- {guilabel}`toolbar`: a vertical bar on the left side of the browser window with editing options for the content

On the edit bar, we find options affecting the current context...

- {guilabel}`edit`
- {guilabel}`folder contents`
- {guilabel}`add`

There is a menu with three dots that holds additional options:

- {guilabel}`state`
- {guilabel}`view`
- {guilabel}`history`
- {guilabel}`sharing`

At the bottom of the toolbar is a silhouette-icon that holds a menu with the following links:

- {guilabel}`logout`
- {guilabel}`profile`
- {guilabel}`preferences`
- {guilabel}`site-setup`

Some edit bar options only show when appropriate;
for example, {guilabel}`folder contents` and {guilabel}`add` are only shown for Folders.

(features-users-label)=

## Users

````{only} not presentation
Let's create our first users within Plone.
So far we used the admin user (admin:admin) configured in the buildout.
This user is often called "Zope root" and is not managed in Plone but only by Zope.
Therefore the user is missing some features like email and full name and won't be able to use some of Plone's features.
But the user has all possible permissions.
As with the root user of a server, it's bad practice to make unnecessary use of Zope root.
Use it to create Plone sites and their initial users, but not much else.

You can also add Zope users via the terminal by entering:

```
$ ./bin/instance adduser <someusername> <supersecretpassword>
```

That way you can access databases you get from customers where you have no Plone user.

To add a new user in Plone, click on the user icon at the bottom of the left vertical bar and then on {guilabel}`Site setup`.
This is Plone's control panel.
You can also access it by browsing to <http://localhost:8080/Plone/@@overview-controlpanel>

```{figure} _static/features_control_panel.png
```

Click on {guilabel}`Users and Groups` and add a user.
If we had configured a mail server, Plone could send you a mail with a link to a form where you can choose a password.
(Or, if you have Products.PrintingMailHost in your buildout, you can see the email scrolling by in the console, just the way it would be sent out.)
We set a password here because we haven't yet configured a mail server.

Make this user with your name an administrator.

```{figure} _static/features_add_user_form.png
```

Then create another user called `testuser`.
Make this one a normal user.
You can use this user to see how Plone looks and behaves to users that have no admin permissions.

Now let's see the site in 3 different browsers with three different roles:

> - as anonymous
> - as editor
> - as admin
````

```{only} presentation
Create some Plone users:

1. {guilabel}`admin` > {guilabel}`Site setup` > {guilabel}`Users and Groups`
2. Add user \<yourname> (groups: Administrators)
3. Add another user "tester" (groups: None)
4. Add another user "editor" (groups: None)
5. Add another user "reviewer" (groups: Reviewers)
6. Add another user "jurymember" (groups: None)

Logout as admin by clicking 'Logout' and following the instructions.

Login to the site with your user now.
```

(features-mailserver-label)=

## Configure a Mailserver

```{only} not presentation
For production-level deployments you have to configure a mailserver.
Later in the training we will create some content rules that send emails when new content is put on our site.

For the training you don't have to configure a working mailserver since the Plone-Add-on `Products.PrintingMailHost` is installed which will redirect all emails to the console.
```

- Server: {samp}`localhost`
- Username: leave blank
- Password: leave blank
- Site 'From' name: Your name
- Site 'From' address: Your email address

```{only} not presentation
Click on `Save and send test e-mail`. You will see the mail content in the console output of your instance. Plone will not
actually send the email to the receivers address unless your remove `Products.PrintingMailHost`.
```

## The site structure

First delete all existing content from the site since we won't use it!

- Click on the folder-icon in the toolbar while on the frontpage
- Select all displayed content items
- Click on the trash icon to delete them

Now we have a clean slate and can start creating the structure we want:

```text
Root (Frontpage)
├── Training
├── Schedule
├── Location
├── Sponsors
├── Sprint
└── Contact
```

Below we'll add appropriate content.

Edit the front page:

- Change the title to `Plone Conference 2050, Solis Lacus, Mars`
- Add some dummy text
- Save the page

Create a site structure:

- Add a Page "Training"
- Add a Page "Schedule"
- Add a Page "Location"
- Add a Page "Sponsors"
- Add a Page "Sprint"
- Add a Page "Contact"

```{figure} _static/features_site_structure.png
:alt: The view of the newly created site structure.

The view of the newly created site structure.
```

```{eval-rst}
.. TODO::

    * Create folder news or do not delete in former section
    * screenshot below of the navigation bar
```

- In `/news`: Add a News Item "Conference Website online!" with some image
- In `/news`: Add a News Item "Submit your talks!"
- In `/events`: Add an Event "Deadline for talk submission" Date: 2025/08/10
- Add a Folder "Register"
- Add a Folder "Intranet"

```{figure} _static/features_new_navigation.png
:alt: The view of the extended navigation bar.

The view of the extended navigation bar.
```

(features-content-types-label)=

## Default content types

The default Plone content types are:

Page

: A Page is the most flexible content type.
  You can use the editor to create, edit and arrange blocks on a page.
  You can choose from blocks for Text, Image, Video, List of existing content and many more.
  Pages - like folders - can also contain other content. This means you can use them to structure your site. In Plone 6 Classic pages are not *folderish*!

  ```{figure} _static/features_add_a_page.png
  ```

Folder

: Folders are used to structure content like in a file-system.
  They can display a listing of its content.
  Pages can also contain other content.
  When you use Volto you usually don't use folders to create a structure since pages are also folders.
  For some cases (e.g. lists of documents) using folders can be usefull though.

  ```{figure} _static/features_add_a_folder.png
  ```

File

: A file like a pdf, video or Word document.

  ```{figure} _static/features_add_a_file.png
  ```

Image

: Like files but png, jpeg or other image types

  ```{figure} _static/features_add_a_image.png
  ```

Event

: These are basically pages with start and end dates and some additional fields for

  ```{figure} _static/features_add_a_event.png
  ```

Link

: A link to an internal or external target.

  ```{figure} _static/features_add_a_link.png
  ```

News Item

: Basically a page with an image and an image caption to be used for press releases an such.

  ```{figure} _static/features_add_a_news_item.png
  ```

Collection

: Collections are virtual lists of items found by doing a specialized search.
  With Volto you usually do not use them anymore. Instead you use a page with one or more listing blocks.

  ```{figure} _static/features_pending_collection.png
  :alt: Editing a collection
  ```

(features-containers-label)=

## Containers

- Go to 'schedule'
- explain the difference between title, ID, and URL
- explain `/contents`
- change the order of items
- explain bulk actions
- Display Menu
- Explain default pages (in classic Plone)
- Explain Folderish Pages (in Plone6 and Volto)

(features-content-rules-label)=

## Content Rules

```{warning}
Content-rules can not be configured in Volto yet. See <https://github.com/plone/volto/issues/10>. You need to use the backend to configure content rules.
```

- Create new rule "a new talk is in town"!
- New content in folder "Talks" -> Send Mail to reviewers.

```{figure} _static/features_add_rule_1.png
:alt: Add a rule through the web.

Add a rule through the web.
```

```{figure} _static/features_add_rule_2.png
:alt: Add an action to the rule.

Add an action to the rule.
```

```{figure} _static/features_add_rule_3.png
:alt: Add mail action.

Add mail action.
```

```{figure} _static/features_add_rule_4.png
:alt: Assign the newly created rule.

Assign the newly created rule.
```

(features-history-label)=

## History

Show and explain; mention versioning and its relation to types.

(features-manage-members-label)=

## Manage members and groups

- add/edit/delete Users

- roles

- groups

  - Add group "Editors" and add the user 'editor' to it
  - Add group: `orga`
  - Add group: `jury` and add user 'jurymember' to it.

(features-workflows-label)=

## Workflows

Take a look at the {guilabel}`state` drop down on the edit bar on the homepage.
Now, navigate to one of the folders just added.
The homepage has the status `published` and the new content is `private`.

Let's look at the state transitions available for each type.
We can make a published item private and a private item published.
We can also submit an item for review.

Each of these states connects roles to permissions.

- In `published` state, the content is available to anonymous visitors;
- In `private` state, the content is only viewable by the author (owner) and users who have the `can view` role for the content.

A *workflow state* is an association between a role and one or more permissions.
Moving from one state to another is a `transition`.
Transitions (like `submit for review`) may have actions — such as the execution of a content rule or script — associated with them.

A complete set of workflow states and transitions makes up a *workflow*.
Plone allows you to select among several pre-configured workflows that are appropriate for different types of sites.
Individual content types may have their own workflow.
Or, and this is particularly interesting, they may have no workflow.
In that case, which initially applies to file and image uploads, the content object inherits the workflow state of its container.

```{note}
An oddity in all of the standard Plone workflows: a content item may be viewable even if its container is not.
Making a container private does **not** automatically make its contents private.
```

```{seealso}
- Training {doc}`/workflow/index`
- Plone 5 Documentation [Collaboration and Workflow](https://5.docs.plone.org/working-with-content/collaboration-and-workflow/index.html)
```

(features-wc-label)=

## Working copy

```{warning}
Working copies can not be used in Volto yet.
```

Published content, even in an intranet setting, can pose a special problem for editing.
It may need to be reviewed before changes are made available.
In fact, the original author may not even have permission to change the document without review.
Or, you may need to make a partial edit.
In either case, it may be undesirable for changes to be immediately visible.

Plone's working copy support solves this problem by adding a check-out/check-in function for content — available on the actions menu.
A content item may be checked out, worked on, then checked back in.
Or it may be abandoned if the changes weren't acceptable.
Not until check in is the new content visible.

While it's shipped with Plone, working copy support is not a common need.
So, if you need it, you need to activate it via the add-on packages configuration page.
Unless activated, check-in/check-out options are not visible.

```{Note}
Working Copy Support has limited support for Dexterity content types. The limitation is that there are some outstanding issues with folderish items that contain many items.
See: [plone/Products.CMFPlone#665](https://github.com/plone/Products.CMFPlone/issues/665)
```

(features-placeful-wf-label)=

## Placeful workflows

```{warning}
Placeful workflows can not be configured in Volto yet. Workflow-settings that you configure in the classic frontend are working though.
```

You may need to have different workflows in different parts of a site.
For example, we created an intranet folder.
Since this is intended for use by our conference organizers — but not the public — the simple workflow we wish to use for the rest of the site will not be desirable.

Plone's `Workflow Policy Support` package gives you the ability to set different workflows in different sections of a site.
Typically, you use it to set a special workflow in a folder that will govern everything under that folder.
Since it has effect in a "place" in a site, this mechanism is often called "Placeful Workflow".

As with working-copy support, Placeful Workflow ships with Plone but needs to be activated via the add-on configuration page.
Once it's added, a {guilabel}`Policy` option will appear on the state menu to allow setting a placeful workflow policy.
