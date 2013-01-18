
3. The features of Plone (45min) (Philip)
=========================================

 * Users
 * Walktrough of the UI
 * Content-Types
 * Pages and Folders
 * Content-Management
 * Collections
 * Content Rules, History,
 * Working Copys
 * User-Management, Roles und Groups
 * Workflows
 * Placeful Workflows


Users
-----

Now let us create our first user within Plone. So far we used the admin-user (admin:admin) configured in the buildout. He is often called "zope-root". This user is not managed in Plone but only in by Zope. Therefore he's missing some features like email and fullname and he won't be able to some of plone's features. But he has all possible permissions.

You can add zope-users also via the terminal by entering::

  $ ./bin/instance adduser rescueuser secretpassword

This way you can access databases you get from customers wehere you have no Plone-user.

Now click on the name "admin" in the top right corner and then on "Site setup". This is Plone's control panel. You can access it by browsing to http://localhost:8080/plone-control_panel

Click on "Users and Groups" and add a user. We use pbauer or pgerken as usernames. If you'd have configured a mail-server, Plone can send you a mail with a link to a form where you can chose a password. We set a password here because we didn't configure a smtp-server.

Make this user with your name an admin.

Create another user called testuser. Make him a normal user.

*Firefox --noremote ist ein Weg, um mit unterschiedlichen Nutzern gleichzeitig auf einer Webseite angemeldet zu sein*

Now let's see the site in 3 different browser logged-in in three different roles:

* as anonymous
* as editor
* as admin


Walktrough of the UI
--------------------

Let's see what is there...

* portal-top: logo, search, global-navigation (viewlets)
* portal-columns: a container

  * portal-column-one: portlets
  * portal-column-content: the content and the editor
  * portal-column-two: portlets

* portal-footer: viewlets

These are also the css-classes of the respective div's. Get used to them if you want to do theming you'll need them.


Content-Types
-------------

Edit a page:

* Edit frontpage
* Title: "Plone Conference 2012, Arnhem"
* Description "Tutorial"
* Text "..."

Create a site-structure:

* Add folder "The Event" and in that ...

  * Folder "Talks"
  * Folder "Training"
  * Folder "Sprint"

* In /news: Add News Item "conf website online!" with image
* In /news: Add News Item "submit your talks!"
* In /events: Add Event "Deadline for talk-submission" Date: 10.10.2012

* Add Folder "Register"
* Delete "members"
* Add Folder "Intranet"


Explain default content-types:

* Document
* News Item
* Event
* File
* Image
* Link
* Folder
* Collection


Folders
-------

* Go to 'the-event'
* explain title/id/url
* explain /folder_contents
* change order
* bulk-actions
* dropdown "display"
* default_pages
* Add a page to 'the-event': "The Event" and make it the default-page


Collections
-----------

* add a new collection: all content that has pending as wf_state.
* explain http://localhost:8080/Plone/events/aggregator/edit
* old vs. new collections (in 4.2. new collections are the default)
* mention collection-portets


Content Rules
-------------

* Create new rule "a new talk is in town"!
* New content in folder "Talks" -> Send Mail to reviewers.


History
-------

explain


Manage members and groups
-------------------------

* add/edit/delete Users
* roles
* groups

  * Add group: orga
  * add group: speaker


Workflows
---------

* screenshots?
* Show plone.app.workflowmanager


Working copy
------------

* enable addon
* explain


Placeful workflows
------------------

* enable addon
* explain

