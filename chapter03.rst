
3. The features of Plone (45min) (Philip)
=========================================

For trainings we do most of this part using only keywords. You can find a in-depth user-manual at http://plone.org/documentation/manual/plone-4-user-manual


Users
-----

Let's create our first user within Plone. So far we used the admin-user (admin:admin) configured in the buildout. He is often called "zope-root". This user is not managed in Plone but only in by Zope. Therefore he's missing some features like email and fullname and he won't be able to use some of plone's features. But he has all possible permissions.

You can add zope-users also via the terminal by entering::

  $ ./bin/instance adduser <someusername> <supersecretpassword>

That way you can access databases you get from customers where you have no Plone-user.

To add a new user click on the name "admin" in the top right corner and then on "Site setup". This is Plone's control panel. You can also access it by browsing to http://localhost:8080/plone_control_panel

Click on "Users and Groups" and add a user. If you'd have configured a Mailserver, Plone could send you a mail with a link to a form where you can choose a password. We set a password here because we didn't configure a Mailserver.

Make this user with your name an administrator.

Then create another user called testuser. Make him a normal user. You can use this user to see how Plone loks and behaves to users that have no admin-permission.

Now let's see the site in 3 different browsers with in three different roles:

* as anonymous
* as editor
* as admin


Configure a Mailserver
----------------------

We should configure a mailserver since later create some content-actions that send emails when new content is put on our site.


Walktrough of the UI
--------------------

Let's see what is there...

* portal-top:

  * personaltools: name, logout etc.
  * logo: with a link to the frontpage
  * search
  * global-navigation

* portal-columns: a container holding:

  * portal-column-one: portlets (configurable boxes with tool like navigation, news etc.)
  * portal-column-content: the content and the editor
  * portal-column-two: portlets

* portal-footer: viewlets

These are also the css-classes of the respective div's. If you want to do theming you'll need them.


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
* In /events: Add Event "Deadline for talk-submission" Date: 10.10.2013

* Add Folder "Register"
* Delete "members"
* Add Folder "Intranet"


The default content-types:

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
* explain the default collection for events at http://localhost:8080/Plone/events/aggregator/edit
* old vs. new collections (from Plone 4.2 on the new collections are the default)
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

