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

% TODO Short appetizer on all the fancy features.

Now we start a Plone instance and take a look at all the features you can use as an integrator.
Developers will get a glimps on the features that can be modified easily.

(features-start-stop-label)=

## Starting and Stopping Plone

We control Plone with `make`. Start your Plone instance with:

```shell
$ make start
```

The Plone instance starts up with `Ready to handle requests`.
Later on the instance can be stopped by {kbd}`ctrl + c`.

A standard installation listens on port 8080, so lets have a look at <http://localhost:8080>

```{figure} _static/features_plone_running.png
```

As you can see, there is no Plone site yet.

(features-create-plonesite-label)=

## Creating a Plone Site

We now have a running Zope with a database, but no content.

Push the botton {guilabel}`Create a new Plone site`.
If the site is asking you to login, log in with `admin` and password `secret` (they are taken from the file `instance.yaml`).

```{image} _static/features_create_site_form.png
```

You will be automatically redirected to the new site.

This is how the front page should look like:

```{image} _static/frontpage_plone.png
```


## Starting and Stopping the frontend

Start the frontend of your new Plone site by switching to directory `frontend` and enter:

```shell
yarn start
```

Opening `http://localhost:3000`, you will see the front page of your Plone site in Volto.

```{figure} _static/frontpage_volto.png
```

You can stop the frontend any time using {kbd}`ctrl + c`.

While developing it is not necessary to restart the frontend unless you are adding a new file.


### Exercises

#### Exercise 1

Now let's say you want Plone to listen on port 9080 instead of the default 8080.
Open the file `backend/instance.yml` in your favorite editor.
How could you do this?

````{admonition} Solution
:class: toggle

```yaml
wsgi_listen: localhost:9080
```

Change the address to `localhost:9080` and restart your instance.

You will also have to tell the frontend that the backend is now running on a different port!

You need to change the environment variable `RAZZLE_DEV_PROXY_API_PATH` to the base url of the backend:

```shell
RAZZLE_DEV_PROXY_API_PATH=http://localhost:9080/Plone yarn start
```

When your Plone instance is not called `Plone` you can use the same approach:

```shell
RAZZLE_DEV_PROXY_API_PATH=http://localhost:8080/mysite yarn start
```

````


#### Exercise 2

Change the port of the frontend to 1234

````{admonition} Solution
:class: toggle

By default the frontend will start on port 3000. You can change the port and/or hostname for the frontend by specifying the environment variables `PORT` and/or `HOST`:

```shell
HOST=localhost PORT=1234 yarn start
```
````


(features-walkthrough-label)=

## Walkthrough of the UI

Let's see what is there...

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

There is a menu with three dots that holds additional options:

- {guilabel}`review state`
- {guilabel}`history`
- {guilabel}`sharing`
- {guilabel}`url management`

At the bottom of the toolbar is a silhouette-icon that holds a menu with the following links:

- {guilabel}`logout`
- {guilabel}`profile`
- {guilabel}`preferences`
- {guilabel}`site setup`

Some toolbar options only show when appropriate.
For example, {guilabel}`edit` is only shown if the current user has the permission to edit.


(features-mailserver-label)=

## Configure a Mailserver

```{only} not presentation
For production level deployments you have to configure a mailserver.
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
- Click somewhere in the text, press return and see the block beeing splitted.
- Save the page.

If you have already content in your instance, you may want to delete it.
Go to `/contents` by clicking the folder icon in the toolbar.
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

The view of the newly created site structure.
```

Additional to these conference pages we also want some news and events.
We want a registration page and an a protected section for the conference team.

- Add a page "News"
- In `/news`: Add a News Item "Conference Website online!" with some image
- In `/news`: Add a News Item "Submit your talks!"
- Add a page "Events"
- In `/events`: Add an Event "Deadline for talk submission" Date: 2025/08/10
- Add a page "Registration"
- Add a page "Intranet"

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
  Pages are folderish, they can contain other content.
  This means you can use them to structure your site.

  ```{figure} _static/features_add_a_page.png
  ```

File

: A file like a pdf, video or Word document.

  ```{figure} _static/features_add_a_file.png
  ```

Image

: Like file but png, jpeg or other image types.
  The Image content typ has an image field.
  Values of the image field are saved in multiple scales to be accessible easily when rendering.

  ```{figure} _static/features_add_a_image.png
  ```

Event

: These are basically pages with start and end dates and some additional fields for whole day or recurring events.

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


(features-containers-label)=

## Containers

Go to "News".

Earlier we created this page with its title "News".
Therfore this page has the id "news" which we can see as part of its url.

A page is folderish.
To see its contained items, we change to '/contents' by clicking the folder icon.

We can change the order of the two contained items by dragging and dropping.

We can modify their title and id, publish them, etc.. in one step by selecting them and applying a bulk action.

A page has per default the view displaying the blocks of the page.
As for all content types, you as a developer can provide multiple views or replace the default view.
This is useful for adding components that should be shown independent of how an editor creates a page.

Per default the page does not show its contained items but just the title and the blocks an editor creates.
The contained items can be shown by creating a listing block.
A listing block without any criterias lists the contained items.

```{image} _static/contents.png
```


(features-content-rules-label)=

## Content Rules

Content rules allow to subscribe actions to events.
We can access the UI by switching to the site setup.
Select the menu in the left bottom of your page.
In site setup we select the content rules panel.

Each content rule created here is a contract on a section of this site or just a section to apply an event subscriber.
The content rule therefore defines an action that subscribes to an event.

### Exercise

Create a new rule "Notify moderators on new news items".
Apply this rule to content type "News Item".
Apply this rule globally by switching to your site root and following menu "rules".

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
Administrators are users assigned to the role "Manager" which is assigned all permissions.

The current user "admin" is not listed in the user control panel as it is not a Plone user, but a Zope user.
This user is registered in the Zope instance, a level above our dedicated Plone site.
Our dedicated Plone site emerges as http://localhost:3000/ but indeed is one Plone site of multiple Plone sites in a Zope instance.

For a deeper insight, visit the backend via the "management interface".

```{figure} _static/zmi_access.png
:alt: ZMI Zope management interface

ZMI Zope management interface
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


(features-seealso-label)=

## See also

- [Plone documentation](https://6.docs.plone.org/)  
- ["Working with content" on 5.docs.plone.org](https://5.docs.plone.org/working-with-content/index.html)
