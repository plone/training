---
myst:
  html_meta:
    "description": "Plone from an integrators view"
    "property=og:description": "Plone from an integrators view"
    "property=og:title": "The Features of Plone"
    "keywords": "Plone, content type, user, group, workflow, content rule, history"
---

(features-label)=

# The Features of Plone

Now we create a Plone instance and take a look at all the features you can use as an integrator.
Developers get a glimpse on the features that can be modified easily.

(features-start-stop-label)=

## Starting and stopping Zope

We control Plone with `make`. Start your Zope instance with:

```shell
make start
```

The Zope instance starts up with `Ready to handle requests`.
Later on the instance can be stopped by {kbd}`ctrl c`.

A standard installation listens on port 8080, so let's have a look at <http://localhost:8080>

```{figure} _static/features_plone_running.png
:alt: Zope instance is up and running, ready to create a Plone instance.

Zope instance is up and running, ready to create a Plone instance.
```


(features-create-plonesite-label)=

## Creating a Plone site

We now have a running Zope with a database, but no content.

Push the button {guilabel}`Create a new Plone site`.
Log in with `admin` and password `secret`.
The initial login is defined in file `instance.yaml`.
You should change your password in production sites via `http://localhost:8080/acl_users/users/manage_users`.

If you ever have the need to create an emergency user, create one with:

```shell
venv/bin/addzopeuser masterofdesaster mypassworD£xyz2 -c ./instance/etc/zope.conf
```

```{figure} _static/features_create_site_form.png
:alt: Create a Plone site

Create a Plone site
```

You will be automatically redirected to the new site.

This is how the front page should look like:

```{figure} _static/frontpage_plone.png
:alt: The front page of your site

The front page of your site
```


## Starting and stopping the frontend

Start the frontend of your new Plone site by switching to directory `frontend` and enter:

```shell
make start
```

Opening `http://localhost:3000`, you are facing the front page of your Plone site.

```{figure} _static/frontpage_volto.png
```

You can stop the frontend any time using {kbd}`ctrl c`.

While developing it's not necessary to restart the frontend unless you're adding a new file.

Login to your new site with `admin` and password `secret`.

```{figure} _static/frontpage_volto_logged_in.png
```


### Change ports

#### backend

If you want Plone to listen on port 9080 instead of the default 8080, open the file {file}`backend/instance.yml` in your favorite editor.

```yaml
wsgi_listen: localhost:8080
```

Change the address to `localhost:9080` and restart your instance.

You will also have to tell the frontend that the backend is now running on a different port!

You need to change the environment variable `RAZZLE_DEV_PROXY_API_PATH` to the base URL of the backend:

```shell
RAZZLE_DEV_PROXY_API_PATH=http://localhost:9080/Plone pnpm start
```

When your Plone instance isn't called `Plone` you can use the same approach:

```shell
RAZZLE_DEV_PROXY_API_PATH=http://localhost:8080/mysite pnpm start
```

#### frontend

Change the port of the frontend to 1234

By default the frontend will start on port 3000. You can change the port and/or host name for the frontend by specifying the environment variables `PORT` and/or `HOST`:

```shell
HOST=localhost PORT=1234 pnpm start
```


(features-walkthrough-label)=

## Walk through the user interface

These are the main elements of the user interface:

- {guilabel}`header`:

  - {guilabel}`logo`: with a link to the front page
  - {guilabel}`searchbox`: search
  - {guilabel}`navigation`: The global navigation

- {guilabel}`footer`: site actions, and colophon

- {guilabel}`toolbar`: a vertical bar on the left side of the browser window with editing options for the content

On the toolbar, we find options affecting the current context...

- {guilabel}`edit`
- {guilabel}`folder contents`
- {guilabel}`add`

There is a context menu with additional options:

- {guilabel}`review state`
- {guilabel}`history`
- {guilabel}`sharing`
- {guilabel}`url management`
- {guilabel}`links and references`

At the bottom of the toolbar is a silhouette-icon that holds a menu with the following links:

- {guilabel}`logout`
- {guilabel}`profile`
- {guilabel}`preferences`
- {guilabel}`site setup`

Some toolbar options only show when appropriate.
For example, {guilabel}`edit` is only shown if the current user has the permission to edit the current page.


(features-mailserver-label)=

## Configure a mail server

```{only} not presentation
For production level deployments you have to configure a mail server.
Later in the training we will create some content rules that send emails when new content is put on our site.

For the training you don't have to configure a working mailserver since the Plone add-on `Products.PrintingMailHost` is installed which will redirect all emails to the console.
```

- Server: {samp}`localhost`
- Username: leave blank
- Password: leave blank
- Site 'From' name: Your name
- Site 'From' address: Your email address

```{only} not presentation
Click on `Save and send test e-mail`. You will see the mail content in the console output of your instance. Plone will not
actually send the email to the receivers address unless your remove or deactivate [Products.PrintingMailHost](https://pypi.org/project/Products.PrintingMailHost/).
```


## The site structure

We are creating the following structure:

```text
Root (front page)
├── Training
├── Schedule
├── Location
├── Sponsors
├── Sprint
└── Contact
```

Below we'll add appropriate content.

Edit the front page:

- Change the title to `Plone Conference 2050, Solis Lacus, Mars`.
- Remove the text blocks below the title by selecting all and deleting them.
- Add some dummy text.
- Click somewhere in the text, press return and see the block being splitted.
- Save the page.

If there is existing content in your instance, you might consider removing it. 
Navigate to `/contents` by clicking the folder icon in the toolbar. 
Select all objects and delete them.

Create a site structure:

- Add a Page "Training"
- Add a Page "Schedule"
- Add a Page "Location"
- Add a Page "Sponsors"
- Add a Page "Sprint"
- Add a Page "Contact"


```{figure} _static/features_site_structure.png
:alt: The view of the newly created site structure.

The view of the newly created site structure
```

Additional to these conference pages we also want some news and events.
We want a registration page and a protected section for the conference team.

- Add a page "News"
- In `/news`: Add a News Item "Conference Website online!" with some image
- In `/news`: Add a News Item "Submit your talks!"
- Add a page "Events"
- In `/events`: Add an Event "Deadline for talk submission" Date: 2025/08/10
- Add a page "Registration"
- Add a page "Intranet"


(features-content-types-label)=

## Default content types

The most used default Plone content types are Page, News item, and Event.

### Page

A Page is the most flexible content type.
You can use the editor to create, edit and arrange blocks on a page.
You can choose from blocks for text, an image, a video, a list of existing content and many more.
Pages are folderish, they can contain other content.
This means you can use pages to structure your site.

```{figure} _static/features_add_a_page.png
```

### News Item

Basically a page with an image and an image caption to be used for press releases and such.

```{figure} _static/features_add_a_news_item.png
```

### Event

Basically a page with start and end dates and some additional fields for whole day or recurring events.

```{figure} _static/features_add_a_event.png
```

### Other available content types

There are more content types per default available: file, image, link.

### Content editing

For more information on how to edit content, see the training {doc}`/content-editing/index`.


(features-containers-label)=

## folderish content

Go to "News".

Earlier we created this page with its title "News".
Therefore this page has the id "news" which we can see as part of its url `http://localhost:3000/news`.

A page is folderish.
To inspect its contained items, we change to `/contents` by clicking the folder icon.

We can change the order of the two contained items by dragging and dropping.

We can modify their title and id, publish them, etc.. in one step by selecting them and applying a bulk action.

```{figure} _static/contents.png
:alt: page contents

`/contents`
```

A page has per default the view displaying the blocks of the page.
As for all content types, you as a developer can provide multiple views or replace the default view.
This is useful for adding components that should be shown, regardless of how an editor assembles a page with blocks.

By default, the page doesn't show its contained items but only the title and blocks created by an editor.
To reveal contained items, you can create a listing block.
If you use a listing block without any specific criteria, it lists all contained items.


```{figure} _static/listingblock.png
:alt: listing block

listing contained content items with a listing block
```


(features-content-rules-label)=

## Content Rules

Content rules allow to subscribe actions to events.
We can access the UI by switching to the site setup.
Select the menu in the left bottom of your page.
In the site setup we select the content rules panel.

Each content rule created here is a contract on the site as a whole or just a section to apply an event subscriber to.
The content rule therefore defines an action that subscribes to an event.

### Exercise

The goal of this exercise is to implement a content rule that will notify a moderator of a new news item.

From within the site setup menu, click "Content Rules". This will open a window containing the content rules and several options to filter the rules by event trigger. For now, there are no rules yet, but we will create one now.
Click the button "Add content rule" and enter the title "Notify moderators on new news items".
Select the triggering event "Object added to this container". Later on, we will apply the rule to a specific container.
Enable the "Enabled" check box to make sure the rule will run when applied.
Click Save to save the new content rule and return to the content rules overview.

At this point, we have to configure the rule and tell it to send an e-mail to a moderator when a news item has been added to the container.
Click "Configure" and start by selecting the "Content type" condition.
Click the "Add" button below the content type, select "News Item" and click the right arrow.
Select "Send email" in the Action selection field.
Click the "Add" button below the action selection field and fill out the form. Make sure the mandatory fields (subject, Email recipients, Message) have content and click the right arrow to save the changes.

The rule has been created, but has not been applied to a container yet. Let's do that now.
Click the left arrow button in the top left corner three times to return to the site.
If you want to apply the rule to all news items globally for your site, go to your home page, click the context menu button (three dots in the sidebar) and click "Rules".
From the "Available content rules" dropdown list, select the rule you created earlier and click "Add".

Verify that your rule works by creating a new news item.
See your backend log or your mail for a notification.
Did you receive a notification?


```{figure} _static/features_add_rule_1.png
:alt: Create a new content rule for an event.

Create a new content rule for an event.
```

```{figure} _static/features_add_rule_2.png
:alt: Configure the content rule with conditions and actions.

Configure the content rule with conditions and actions.
```

```{figure} _static/features_add_rule_3.png
:alt: Assign your rule to a page (with or without sub pages) or globally.

Assign your rule to a page (with or without sub pages) or globally.
```


(features-history-label)=

## History

The history not only lists who edited and published an item, but allows users with the appropriate permission to inspect and even revert changes.

```{figure} _static/history_0.png
:alt: Access history.

Access history.
```

```{figure} _static/history_1.png
:alt: View history.

View history.
```

```{figure} _static/history_2.png
:alt: Inspect history.

Inspect history.
```


(features-manage-members-label)=

(features-users-label)=

## Users and groups

In short, a user who wants to modify a Plone site needs to be registered and be given the appropriate permissions.

The Plone security is based on **roles and permissions**.
Every transaction (create page, publish page, … ) is protected by a permission.
A permission is assigned to roles.

Users can be assigned a role directly or by joining a group with the respective role.

### Excursion

We are facing our site as an administrator.
Administrators are users assigned the role "Manager" which is assigned all permissions.

The current user "admin" is not listed in the user control panel as it is not a Plone user, but a Zope user.
This user is registered in the Zope instance, a level above our dedicated Plone site.
Our dedicated Plone site emerges as http://localhost:3000/ but indeed is one Plone site of multiple Plone sites in a Zope instance.

For a deeper insight, visit the backend via the "management interface".

```{figure} _static/zmi_access.png
:alt: ZMI Zope management interface

Link to ZMI Zope management interface at `http://localhost:8080/`
```

### Exercise

Create a user "Urs Herbst" who can add and edit content, even review (publish content), but has no administrator rights.  
The roles should not be assigned directly to the user, but via a group "editors".

Add a group "Jury", create and add user "Lisa Sommer" to it.

(features-groups-label)=

### Groups and users

It is recommended to assign roles to users via group memberships.
Inspect group memberships at its control panel.

```{figure} _static/groupmemberships.png
:alt: Groups memberships

Group memberships
```


(features-workflows-label)=

## Workflows

A workflow is a set of states and transactions.
Each content type is assigned a workflow.
A content type instance like a page is in a state, for example published.
The state can be changed.
Which workflow states a content type instance can be switched to is determined by the workflow transactions.

Have a look at one of the news items we created earlier.
The state is "private" and can be changed to "published" by selecting the "publish" transaction.

The state of a content type instance determines if a user can view, edit or is allowed to execute other modifications like moving or even changing the workflow.

The workflows can be inspected and modified at http://localhost:8080/Plone/portal_workflow/.
It is recommended to configure the workflows for a project programmatically in an add-on instead of doing this through the web UI.
But for getting to know workflows, their states and transactions, and their permission mappings, this address in the ZMI (Zope management interface) is a good place to start.
If you are interested in inspecting the effects on changes it is recommended to copy a default workflow, apply it to for example pages and do changes in this workflow.
Afterwards these changes can be reverted by reapplying the former default workflow.

For programmatically changes, a modified default workflow can be exported and included in an add-on.

Important for the understanding of workflows is the mapping of roles to permissions per workflow state.
This is one crucial integrational component that makes Plone a secure CMS.
Each content type instance like a page is in a workflow state.
Access and modifications of this instance is defined by the role/permission mapping of this workflow state.
As each user, including the anonymous, has a set of roles, the circle is closed and each user has access and or can modify a content type instance or not, according to their roles.

```{seealso}
- {doc}`user_generated_content`
- Training {doc}`training2024:workflow/index`
- Plone 5 Documentation {doc}`plone5docs:working-with-content/collaboration-and-workflow/index`
```


(features-placeful-wf-label)=

### Placeful workflows

```{warning}
Placeful workflows are not yet configurable in Volto.
Workflow settings that are configured in Plone backend are applied though.
```

You may need to have different workflows in different parts of a site.
For example, we created an intranet page.
Since this is intended for our conference organizers — but not the public — the simple workflow we use for the rest of the site is not appropriate for a protected intranet.

Plone's `Workflow Policy Support` package gives you the ability to set different workflows in different sections of a site.
Typically, you use it to set a special workflow on a page determining the page and its sub pages.
Since it has effect in a "place" in a site, this mechanism is often called "Placeful Workflow".

`Placeful Workflow` ships with Plone but needs to be activated via the add-on configuration page.
Once it is added, a {guilabel}`Policy` option appears in the state menu to allow setting a placeful workflow policy.

For more information see training {doc}`training2024:workflow/placeful-workflow`.


(features-publishing-date-label)=

## Publishing date and expiration date

The visibility of a content type instance like a page is not only ascertained by the workflow state.
The publishing can be scheduled by setting the publishing date.

Edit the front page of your site to display published news by adding a listing block with the approriate criteria.  
By publishing one of your news items, it will appear on the front page.

As soon as you change the publishing date to a future date, the news item will no longer be shown on the front page until the date is reached.


(features-sharing-label)=

## Sharing

Apart from publishing a page or any other content type instance, and making it visible for all users that are allowed to view published content, we can make it visible to only a group of users.
The sharing UI can be accessed via the context menu.

The sharing feature is not restricted to visibility.
You can even make a page, with or without sub pages, editable only by a group of users.


(features-url-management-label)=

## URL management

Plone has an integrated mechanism to remember URLs that where modified.
A moved page is still available via the former URL.

Additional to this behavior, a page can be explicitly made available under further URLs.

You can find the UI for adding alternative URLs following the context menu {guilabel}`...`.


(features-wc-label)=

## Working copy

```{warning}
The working copy feature is not yet implemented in Volto UI.
```

Published content, even in an intranet setting, can pose a special problem for editing.
It may need to be reviewed before changes are made available.
In fact, the original author may not even have permission to change the document without review.
Or, you may need to make a partial edit.
In either case, it may be undesirable for changes to be immediately visible.

Plone's working copy support solves this problem by adding a check-out/check-in function for content — available via the actions menu.
A content item may be checked out, worked on, then checked back in.
Or it may get abandoned if the changes aren't acceptable.
The new content is not visible unless checked back in.

While it's shipped with Plone, working copy support is not a common need.
So, if you need it, activate it via the add-on packages configuration page.
Unless activated, check-in/check-out options are not visible.


% TODO section about the discussion/commenting feature
