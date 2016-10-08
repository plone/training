.. _user-content-label:

User Generated Content
======================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/11_user_generated_content_p5/ src/ploneconf.site


How do prospective speakers submit talks? We let them register on the site and grant right to create talks. For this we go back to changing the site through-the-web.

In this chapter we:

* allow self-registration
* constrain types on the talk folder
* grant local roles
* create a custom workflow for talks


.. _user-content-self-reg-label:

Self-registration
-----------------

* Go to the Security control panel at http://localhost:8080/Plone/@@security-controlpanel and Enable self-registration
* Leave "Enable User Folders" off unless you want a community site.


.. _user-content-constrain-types-label:

Constrain types
---------------

* On the talk folder select `Restrictions… <http://localhost:8080/Plone/the-event/talks/folder_constraintypes_form>`_ from the *Add new* menu. Only allow to add talks.


.. _user-content-local-roles-label:

Grant local roles
-----------------

* Go to *Sharing* and grant the role *Can add* to the group logged-in users. Now every user can add content in this folder (and only this folder).

Now all logged-in users can create and submit talks in this folder with the permission of the default workflow.


.. _user-content-custom-workflow-label:

A custom workflow for talks
---------------------------

We still need to fix a problem: Authenticated users can see all talks, even the ones of other users in the private state. Since we don't want this we will create a modified workflow for talks. The new workflow will only let them see and edit talks they created themselves and not the ones of other users.

* Go to the ZMI > :guilabel:`portal_workflow`
* See how talks have the same workflow as most content, namely :guilabel:`(Default)`
* Go to the tab :guilabel:`Contents`, check the box next to :guilabel:`simple_publication_workflow`, click :guilabel:`copy` and :guilabel:`paste`.
* Rename the new workflow from *copy_of_simple_publication_workflow* to *talks_workflow*.
* Edit the workflow by clicking on it: Change the Title to *Talks Workflow*.
* Click on the tab :guilabel:`States` and click on :guilabel:`private` to edit this state. In the next view select the tab :guilabel:`Permissions`.
* Find the table column for the role :guilabel:`Contributor` and remove the permissions for :guilabel:`Access contents information` and :guilabel:`View`. Note that the :guilabel:`Owner` (i.e. the Creator) still has some permissions.
* Do the same for the state :guilabel:`pending`
* Go back to :file:`portal_workflow` and set the new workflow :file:`talks_workflow` for talks. Click :file:`Change` and then :file:`Update security settings`.

.. note::

    The add-on `plone.app.workflowmanager <https://pypi.python.org/pypi/plone.app.workflowmanager>`_ provides a much nicer user-interface for this. The problem is you need a big screen for it and it can be pretty confusing as well.

Done.


.. _user-content-fs-label:

Move the changes to the file system
-----------------------------------

We don't want to do these steps for every new conference by hand so we move the changes into our package.

Import/Export the Workflow
**************************

* export the GenericSetup step *Workflow Tool* in http://localhost:8080/Plone/portal_setup/manage_exportSteps.
* drop the file :file:`workflows.xml` into :file:`profiles/default`.
* drop :file:`workflows/talks_workflow/definition.xml` in :file:`profiles/default/workflows/talks_workflow/definition.xml`. The others are just definitions of the default-workflows and we only want things in our package that changes Plone.


Enable self-registration
************************

To enable self-registration add the following to :file:`profiles/default/registry.xml`:

..  code-block:: xml

    <record name="plone.enable_self_reg" interface="Products.CMFPlone.interfaces.controlpanel.ISecuritySchema" field="enable_self_reg">
      <value>True</value>
    </record>

.. note::

   Before Plone 5 this had to be done in python in a setuphandler (see below) since there was not yet an exportable setting for this.


Grant local roles
*****************

Since the granting of local roles applies only to a certain folder in the site we would not always write code for it but do it by hand. But for testability and repeatability (there is a conference every year!) we should create the initial content structure automatically.

So let's make sure some initial content is created and configured on installing the package.

To run arbitrary code during the installation of a package we use a special import step, a `setuphandler <http://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py>`_

Our package already has such an import step registered in :file:`configure.zcml`. It will be automatically run when (re-)installing the add-on.

..  code-block:: xml
    :linenos:

    <genericsetup:importStep
        name="ploneconf.site-postInstall"
        title="ploneconf.site post_install import step"
        description="Post install import step from ploneconf.site"
        handler=".setuphandlers.post_install">
    </genericsetup:importStep>

.. note::

    All GenericSetup import steps, including this one, are run for **every add-on product** when they are installed. To make sure that it is only run during installation of your package the code checks for a marker text file :file:`ploneconfsite_default.txt`.

This step makes sure the method :py:meth:`post_install` in :file:`setuphandlers.py` is executed on installation.

..  code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-
    from Products.CMFPlone.interfaces import constrains
    from plone import api

    import logging

    PROFILE_ID = 'profile-ploneconf.site:default'
    logger = logging.getLogger(__name__)


    def isNotCurrentProfile(context):
        return context.readDataFile('ploneconfsite_default.txt') is None


    def post_install(context):
        """Post install script"""
        if isNotCurrentProfile(context):
            return
        # Do something during the installation of this package
        portal = api.portal.get()
        set_up_content(portal)


    def set_up_content(portal):
        """Create and configure some initial content"""
        # Abort if there is already a folder 'talks'
        if 'talks' in portal:
            logger.info('An item called "talks" already exists')
            return
        talks = api.content.create(
            container=portal,
            type='Folder',
            id='talks',
            title='Talks')
        api.content.transition(talks, 'publish')

        # Allow logged-in users to create content
        api.group.grant_roles(
            groupname='AuthenticatedUsers',
            roles=['Contributor'],
            obj=talks)

        # Constrain addable types to talk
        behavior = constrains.ISelectableConstrainTypes(talks)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['talk'])
        behavior.setImmediatelyAddableTypes(['talk'])
        logger.info('Created and configured %s' % talks.absolute_url())

Once we reinstall our package a folder 'talks' is created with the appropriate local roles and constraints.

Remember that we wrote similar code to create the folder *The Event* in :ref:`dexterity2-upgrades-label`. We should probably add it also to setuphandlers to make sure a sane structure gets created when we create a new site by hand or in tests.

You'd usually create a list of dictionaries containing the type, parent and title plus optionally layout, workflow state etc. to create an initial structure. In some projects it could also make sense to have a separate profile besides ``default`` which might be called ``content`` that creates an initial structure and maybe another ``testing`` that creates dummy content (talks, speakers etc) for tests.

..  note::

    You can also export and later import content using the GenericSetup step *Content* (:py:meth:`Products.CMFCore.exportimport.content.exportSiteStructure`) although you cannot set all types of properties (workflow state, layout) and the syntax is a little special.


Exercise 1
++++++++++

Create a profile ``content`` that runs its own method in :file:`setuphandlers.py`. Note that you need a different marker text file to make sure your code is only run when installing the profile ``content``.

..  admonition:: Solution
    :class: toggle

    Register the profile and the upgrade step in :file:`configure.zcml`

    .. code-block:: xml

        <genericsetup:registerProfile
            name="content"
            title="PloneConf Site initial content"
            directory="profiles/content"
            description="Extension profile for PloneConf Talk to add initial content"
            provides="Products.GenericSetup.interfaces.EXTENSION"
            />

        <genericsetup:importStep
            name="ploneconf.site-content"
            title="ploneconf.site with initial content"
            description="Post install import step from ploneconf.site with initial content"
            handler=".setuphandlers.content">
            <depends name='typeinfo' />
        </genericsetup:importStep>

    Create the profile folder :file:`profiles/content` and drop a marker file :file:`ploneconfsite_content_marker.txt` in it.

    Also add a :file:`profiles/content/metadata.xml` so the default profile gets automatically installed when installing the content profile.

    ..  code-block:: xml

        <metadata>
          <version>1000</version>
          <dependencies>
            <dependency>profile-ploneconf.site:default</dependency>
          </dependencies>
        </metadata>


    Add the structure you wish to create as a list of dictionaries in :file:`setuphandlers.py`:

    ..  code-block:: python
        :linenos:

        STRUCTURE = [
            {
                'type': 'Folder',
                'title': u'The Event',
                'id': 'the-event',
                'description': u'Plone Conference 2020',
                'default_page': 'frontpage-for-the-event',
                'state': 'published',
                'children': [{
                    'type': 'Document',
                    'title': u'Frontpage for the-event',
                    'id': 'frontpage-for-the-event',
                    'state': 'published',
                    },
                    {
                    'type': 'Folder',
                    'title': u'Talks',
                    'id': 'talks',
                    'layout': 'talklistview',
                    'state': 'published',
                    },
                    {
                    'type': 'Folder',
                    'title': u'Training',
                    'id': 'training',
                    'state': 'published',
                    },
                    {
                    'type': 'Folder',
                    'title': u'Sprint',
                    'id': 'sprint',
                    'state': 'published',
                    },
                ]
            },
            {
                'type': 'Folder',
                'title': u'Talks',
                'id': 'talks',
                'description': u'Submit your talks here!',
                'state': 'published',
                'layout': '@@talklistview',
                'allowed_types': ['talk'],
                'local_roles': [{
                    'group': 'AuthenticatedUsers',
                    'roles': ['Contributor']
                }],
            },
            {
                'type': 'Folder',
                'title': u'News',
                'id': 'news',
                'description': u'News about the Plone Conference',
                'state': 'published',
                'children': [{
                    'type': 'News Item',
                    'title': u'Submit your talks!',
                    'id': 'submit-your-talks',
                    'description': u'Task submission is open',
                    'state': 'published', }
                ],
            },
            {
                'type': 'Folder',
                'title': u'Events',
                'id': 'events',
                'description': u'Dates to keep in mind',
                'state': 'published',
            },
        ]


    Add the method :py:meth:`content` to :file:`setuphandlers.py`. We pointed to that when registering the import step. And add some fancy logic to create the content from ``STRUCTURE``.

    ..  code-block:: python
        :linenos:

        from zope.lifecycleevent import modified


        def content(context):
            if context.readDataFile('ploneconfsite_content_marker.txt') is None:
                return

            portal = api.portal.get()
            for item in STRUCTURE:
                _create_content(item, portal)


        def _create_content(item_dict, container, force=False):
            if not force and container.get(item_dict['id'], None) is not None:
                return

            # Extract info that can't be passed to api.content.create
            layout = item_dict.pop('layout', None)
            default_page = item_dict.pop('default_page', None)
            allowed_types = item_dict.pop('allowed_types', None)
            local_roles = item_dict.pop('local_roles', [])
            children = item_dict.pop('children', [])
            state = item_dict.pop('state', None)

            new = api.content.create(
                container=container,
                safe_id=True,
                **item_dict
            )
            logger.info('Created {0} at {1}'.format(new.portal_type, new.absolute_url()))

            if layout is not None:
                new.setLayout(layout)
            if default_page is not None:
                new.setDefaultPage(default_page)
            if allowed_types is not None:
                _constrain(new, allowed_types)
            for local_role in local_roles:
                api.group.grant_roles(
                    groupname=local_role['group'],
                    roles=local_role['roles'],
                    obj=new)
            if state is not None:
                api.content.transition(new, to_state=state)

            modified(new)
            # call recursively for children
            for subitem in children:
                _create_content(subitem, new)

        def _constrain(context, allowed_types):
            behavior = constrains.ISelectableConstrainTypes(context)
            behavior.setConstrainTypesMode(constrains.ENABLED)
            behavior.setLocallyAllowedTypes(allowed_types)
            behavior.setImmediatelyAddableTypes(allowed_types)

    A huge benefit of this implementation is that you can add any object-attribute as a new item to :py:data:`item_dict`. :py:meth:`plone.api.content.create` will then set these on the new objects. This way you can also populate fields like :py:attr:`text` (using :py:class:`plone.app.textfield.RichTextValue`) or :py:attr:`image` (using :py:class:`plone.namedfile.file.NamedBlobImage`).
