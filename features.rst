The Features of Plone
=====================

In-depth user-manual: http://plone.org/documentation/manual/plone-4-user-manual

See also: http://docs.plone.org/working-with-content/index.html

Starting and Stopping Plone
---------------------------

We control Plone with a small script called "instance"::

    $ ./bin/instance fg

This starts Plone in foreground mode so that we can see what it is doing by monitoring console messages. This is an important development method. Note that when Plone is started in foreground mode, it is also automatically in development mode. Development mode gives better feedback, but is much slower, particularly on Windows.

You can stop it by pressing :kbd:`ctrl + c`.

The :program:`instance`-script offers the following options::

    $ ./bin/instance fg
    $ ./bin/instance start
    $ ./bin/instance stop
    $ ./bin/instance -O Plone debug
    $ ./bin/instance -O Plone run myscript.py
    4 ./bin/instance adduser

.. only:: not presentation

    Depending on your computer, it might take up to a minute until Zope will tell you that its ready to serve requests. On a decent laptop it should be running in under 15 seconds.

    A standard installation listens on port 8080, so lets have a look at our Zope site by visiting http://localhost:8080

    As you can see, there is no Plone yet!

    We have a running Zope with a database but no content. But luckily there is a button to create a Plone site. Click on that button (login: admin:admin). This opens a form to create a Plone site. Use :samp:`Plone` as the site id.

    You now have the option to select some addons before you create the site. Since we will use Dexterity from the beginning we select ``Dexterity-based Plone Default Types``. This way even the initial content on our page will be built with dexterity by the addon ``plone.app.contenttypes`` which will be the default in Plone 5.

    You will be automatically redirected to the new site.

.. only:: presentation

    * By default Plone listens on port 8080. Look at http://localhost:8080
    * No Plone yet! Create a new Plone site.
    * Use :samp:`Plone` (the default) as the site id.
    * Select ``Dexterity-based Plone Default Types`` from the addons **before** you click *Create Plone-Site* to install ``plone.app.contenttypes``.

.. note::

    Plone has many message-boxes. They contain important information. Read them and make sure you understand them!



Users
-----

.. only:: not presentation

    Let's create our first users within Plone. So far we used the admin-user (admin:admin) configured in the buildout. This user is often called "zope-root" and is not managed in Plone but only in by Zope. Therefore the user's missing some features like email and fullname and  won't be able to use some of plone's features. But the user has all possible permissions. As with the root user of a server, it's a bad practice to make unnecessary use of zope-root. Use it to create Plone sites and their initial users, but not much else.

    You can also add zope-users also via the terminal by entering::

        $ ./bin/instance adduser <someusername> <supersecretpassword>

    That way you can access databases you get from customers where you have no Plone-user.

    To add a new user in Plone, click on the name :guilabel:`admin` in the top right corner and then on :guilabel:`Site setup`. This is Plone's control panel. You can also access it by browsing to http://localhost:8080/Plone/plone_control_panel

    Click on :guilabel:`Users and Groups` and add a user. If you'd have configured a mail server, Plone could send you a mail with a link to a form where you can choose a password. We set a password here because we haven't yet configure a mail server.

    Make this user with your name an administrator.

    Then create another user called ``testuser``. Make this one a normal user. You can use this user to see how Plone looks and behaves to users that have no admin-permission.

    Now let's see the site in 3 different browsers with in three different roles:

        * as anonymous
        * as editor
        * as admin

.. only:: presentation

    Create some Plone users:

    #. :guilabel:`admin` > :guilabel:`Site setup` > :guilabel:`Users and Groups`
    #. Add user <yourname> (groups: Administrators)
    #. Add another user "tester" (groups: None)
    #. Add another user "editor" (groups: None)
    #. Add another user "reviewer" (groups: Reviewers)
    #. Add another user "jurymember" (groups: None)

    Logout as admin by klicking 'Logout' and following the instructions.

    Login to the site with your user now.


Configure a Mailserver
----------------------


.. only:: not presentation

    We have to configure a mailserver since later we will create some content-actions that send emails when new content is put on our site.

* Server: :samp:`mail.gocept.net`
* Username: :samp:`training@neww.de`
* Password: :samp:`training2014`

Please do not abuse this. We'll disable this account after the training.


Walkthrough of the UI
---------------------

Let's see what is there...

* :guilabel:`portal-top`:

  * :guilabel:`personaltools`: name, logout etc.
  * :guilabel:`logo`: with a link to the frontpage
  * :guilabel:`search`
  * :guilabel:`global`-navigation

* :guilabel:`portal-columns`: a container holding:

  * :guilabel:`portal-column-one`: portlets (configurable boxes with tool like navigation, news etc.)
  * :guilabel:`portal-column-content`: the content and the editor
  * :guilabel: `edit bar`: editing options for the content
  * :guilabel:`portal-column-two`: portlets

* :guilabel:`portal-footer`: viewlets

.. only:: not presentation

    These are also the css-classes of the respective div's. If you want to do theming you'll need them.

On the edit bar, we find options affecting the current context...

* :guilabel:`folder contents`
* :guilabel:`view`
* :guilabel:`edit`
* :guilabel:`rules`
* :guilabel:`sharing`
* :guilabel:`display`
* :guilabel:`add`
* :guilabel:`status`

Some edit bar options only show when appropriate; for example,``folder content`` and ``add`` are only shown for Folders. ``rules`` is currently invisible because we have no content rules available.

Content-Types
-------------

Edit a page:

* :guilabel:`Edit front-page`
* :guilabel:`Title` :samp:`Plone Conference 2014, Bristol`
* :guilabel:`Description` :samp:`Tutorial`
* :guilabel:`Text` :samp:`...`

Create a site-structure:

* Add folder "The Event" and in that ...

  * Folder "Talks"
  * Folder "Training"
  * Folder "Sprint"

* In /news: Add News Item "Conference Website online!" with some image
* In /news: Add News Item "Submit your talks!"
* In /events: Add Event "Deadline for talk-submission" Date: 10.10.2014

* Add Folder "Register"
* Delete Folder "Members" (Users)
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

.. note::

    Please keep in mind that we use `plone.app.contenttypes <http://docs.plone.org/external/plone.app.contenttypes/docs/README.html>`_ for the training. Therefore the types are based on Dexterity and slightly different from the types that you will find in a default-Plone 4.3.x-site.


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
* The future: ``wildcard.foldercontents``


Collections
-----------

* add a new collection: "all content that has pending as wf_state".
* explain the default collection for events at http://localhost:8080/Plone/events/aggregator/edit
* explain Topics
* mention collection-portlets
* multi-path-querys
* constrains, e.g. ``/Plone/folder::1``


Content Rules
-------------

* Create new rule "a new talk is in town"!
* New content in folder "Talks" -> Send Mail to reviewers.


History
-------

Show and explain; mention versioning and its relation to types.


Manage members and groups
-------------------------

* add/edit/delete Users
* roles
* groups

  * Add group "Editors" and add the user 'editor' to it
  * Add group: ``orga``
  * add group: ``jury`` and add user 'jurymember' to it.


Workflows
---------

Take a look at the ``state`` drop-down on the edit bar on the homepage. Now, navigate to one of the folders just added. The homepage has the status ``published`` and the new content is ``private``.

Let's look at the state transitions available for each type. We can make a published item private and a private item published. We can also submit an item for review.

Each of these states connects roles to permissions.

* In ``published`` state, the content is available to anonymous visitors;
* In ``private`` state, the content is only viewable by the author (owner) and users who have the ``can view`` role for the content.

A workflow state is an association between a role and one or more permissions. Moving from one state to another is a ``transition``. Transitions (like ``submit for review``) may have actions — like the execution of a content role or script — associated with them.

A complete set of workflow states and transitions make up a ``workflow``. Plone allows you to select among several pre-configured workflows that are appropriate for different types of sites. Individual content types may their own workflow. Or, and this is particularly interesting, no workflow. In that case, which initially applies to file and image uploads, the content object inherits the workflow of its container.

.. note::

    An oddity in the all of the standard Plone workflows: a content item may be viewable even if its container is not. Making a container private does **not** automatically make its contents private.

Read more at: http://docs.plone.org/working-with-content/collaboration-and-workflow/index.html

Working copy
------------

* Explain add-on and its use case
* Note that it is not yet available for Dexterity Content Types.


Placeful workflows
------------------

* Explain add-on and its use case
* Note that it is not yet available for Dexterity Content Types.

