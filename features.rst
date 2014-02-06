The Features of Plone
=====================

In-depth user-manual: http://plone.org/documentation/manual/plone-4-user-manual


Starting and Stopping Plone
---------------------------

We control Plone with a small script called "instance"::

    $ ./bin/instance fg

This starts Plone and we can see what it is doing.

You can stop it by pressing :kbd:`ctrl + c`.

The :program:`instance`-script offers the following options::

    $ ./bin/instance fg
    $ ./bin/instance start
    $ ./bin/instance stop
    $ ./bin/instance debug -O Plone

.. only:: manual

    Depending on your computer, it might take up to a minute until Zope will tell you that its ready to serve requests. On a decent laptop it shound be running in under 15 seconds.

    A standard installation listens on port 8080, so lets have a look at our Zope site by visiting http://localhost:8080

    As you can see, there is no Plone yet!
    We have a running Zope with a database but no content. But luckily there is a button to create a Zope site.
    Click on that button. This opens a form to create a Plone site. Use :samp:`Plone` as the site id.

.. only:: presentation

    Plone listens on port 8080. Look at http://localhost:8080

    No Plone yet! Create a Plone site.

    Use :samp:`Plone` (the default) as the site id.

.. note::

    Plone has many message-boxes. They contain important information. Read them and make sure you understand them!



Users
-----

.. only:: manual

    Let's create our first users within Plone. So far we used the admin-user (admin:admin) configured in the buildout. He is often called "zope-root". This user is not managed in Plone but only in by Zope. Therefore he's missing some features like email and fullname and he won't be able to use some of plone's features. But he has all possible permissions. It is also unsecure to use this user. Basically, his password can be seen easily within each request.

    You can also add zope-users also via the terminal by entering::

        $ ./bin/instance adduser <someusername> <supersecretpassword>

    That way you can access databases you get from customers where you have no Plone-user.

    To add a new user click on the name :guilabel:`admin` in the top right corner and then on :guilabel:`Site setup`. This is Plone's control panel. You can also access it by browsing to http://localhost:8080/plone_control_panel

    Click on :guilabel:`Users and Groups` and add a user. If you'd have configured a Mailserver, Plone could send you a mail with a link to a form where you can choose a password. We set a password here because we didn't configure a Mailserver.

    Make this user with your name an administrator.

    Then create another user called testuser. Make him a normal user. You can use this user to see how Plone loks and behaves to users that have no admin-permission.

    Now let's see the site in 3 different browsers with in three different roles:

        * as anonymous
        * as editor
        * as admin

.. only:: presentation::

    Create some Plone users:

    #. :guilabel:`admin` > :guilabel:`Site setup` > :guilabel:`Users and Groups`
    #. Add user <yourname> (groups: Administrators)
    #. Add another user "testuser" (groups: Nothing)

    Access the site with each user now.


Configure a Mailserver
----------------------


.. only:: manual

    We have to configure a mailserver since later we will create some content-actions that send emails when new content is put on our site.

* Server: :samp:`mail.gocept.net`
* Username: :samp:`training@neww.de`
* Password: :samp:`training2013`

Please do not abuse this. We'll diable this account after the training.


Walktrough of the UI
--------------------

Let's see what is there...

* :guilabel:`portal-top`:

  * :guilabel:`personaltools`: name, logout etc.
  * :guilabel:`logo`: with a link to the frontpage
  * :guilabel:`search`
  * :guilabel:`global`-navigation

* :guilabel:`portal-columns`: a container holding:

  * :guilabel:`portal-column-one`: portlets (configurable boxes with tool like navigation, news etc.)
  * :guilabel:`portal-column-content`: the content and the editor
  * :guilabel:`portal-column-two`: portlets

* :guilabel:`portal-footer`: viewlets

.. only:: manual

    These are also the css-classes of the respective div's. If you want to do theming you'll need them.


Content-Types
-------------

Edit a page:

* :guilabel:`Edit frontpage`
* :guilabel:`Title` :samp:`Plone Conference 2013, Brazil`
* :guilabel:`Description` :samp:`Tutorial`
* :guilabel:`Text` :samp:`...`

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

show and explain


Manage members and groups
-------------------------

* add/edit/delete Users
* roles
* groups

  * Add group: ``orga``
  * add group: ``speaker`


Workflows
---------

Read more at: http://developer.plone.org/content/workflow.html

Working copy
------------

* enable addon
* explain


Placeful workflows
------------------

* enable addon
* explain

