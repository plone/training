User generated content
======================

How do prospective speakers submit talks? We let registered users create talks. For this we go back to changing the site through-the-web.

In this chapter we:

* allow self-registration
* constrain types on the talk-folder
* create a custom workflow for talks
* grant local roles


Self-registration
-----------------

* Go to the Security-controlpanel at http://localhost:8080/Plone/@@security-controlpanel and Enable self-registration
* Leave "Enable User Folders" off unless you want a community-site.


A custom workflow for talks
---------------------------

Let's be secretive and let submitters only see their own talks.

* Go to the ZMI > portal_workflow
* See how talks have the same workflow as most content ``(Default)``
* Go to the tab *Contents*, check the box next to ``simple_publication_workflow``, click ``copy`` and ``paste``.
* Rename the new workflow from *copy_of_simple_publication_workflow* to *talk_workflow*.
* Edit the workflow by clicking on it: Change the Title to *Talks Workflow*.
* Click on the tab *States* and click on *private* to edit this state. In the next view select the tab *Permissions*.
* Find the talbe-column for the role *Contributor* and remove the permissions for ``Access contents information`` and ``View``. Note that the *Owner* (i.e. the Creator) still has some permissions.
* Do the same for the state *pending*
* Go back to *portal_workflow* and set the new workflow ``talks_workflow`` for talks. Click *Change* and then *Update security settings*.

.. note::

    The addon `plone.app.workflowmanager <https://pypi.python.org/pypi/plone.app.workflowmanager>`_ provides a much nicer user-interface for this. The problem is you need a big screen for it and it can be pretty confusing as well.


Grant local roles
-----------------

* Go to *Sharing* and grant the role *Can add* to the group logged-in users. Now every user can add content in this folder (and only this folder).
* In the talk-folder select `Restrictions… <http://localhost:8081/Plone/talks/folder_constraintypes_form>`_ from the *Add new* menu. Only allow to add talks.

Done.


Move the changes to the file-system
-----------------------------------

Workflow
********

* export the GenericSetup step *Workflow Tool* in http://localhost:8080/Plone/portal_setup/manage_exportSteps.
* drop the file ``workflows.xml`` into ``profiles/default``.
* drop ``workflows/talks_workflow/definition.xml`` in ``profiles/default/workflows/talks_workflow/definition.xml``. The others are just definitions of the default-workflows and we only want things in our package that changes Plone.

Self-registration
*****************

This has to happen in python in a custom `setuphandler.py <http://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py>`_ since there is not yet a exportable setting for this.

Register a import-step in``configure.zcml``. It will be automatically run when (re-)installing the addon.

.. code-block:: xml
    :linenos:

    <genericsetup:importStep
      name="ploneconf.site"
      title="ploneconf.site special import handlers"
      description=""
      handler="ploneconf.site.setuphandlers.setupVarious">
        <depends name="typeinfo"/>
    </genericsetup:importStep>

Note that the setuphandler has a dependency on `typeinfo` because it will only allow the creation of talks. For this the type already has to exist.

Create a new file ``setuphandlers.py``

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    from plone.app.controlpanel.security import ISecuritySchema
    from plone import api

    import logging

    PROFILE_ID = 'profile-ploneconf.site:default'
    logger = logging.getLogger('ploneconf.site')


    def setupVarious(context):

        # Ordinarily, GenericSetup handlers check for the existence of XML files.
        # Here, we are not parsing an XML file, but we use this text file as a
        # flag to check that we actually meant for this import step to be run.
        # The file is found in profiles/default.

        if context.readDataFile('ploneconf.site_various.txt') is None:
            return

        site = api.portal.get()
        set_up_security(site)


    def set_up_security(site):
        secSchema = ISecuritySchema(site)
        secSchema.set_enable_self_reg(True)


Add the marker-file ``profile/default/ploneconf.site_various.txt`` used in line 15::

    The ploneconf.site_various step is run if this file is present in the profile

Grant local roles
*****************

Since this applies only to a certain folder in the site we would normally not write code for it.

But we can easily add a method to the setuphandler that creates the folder and sets up some setting for it.

Here is an example:

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    from plone.app.controlpanel.security import ISecuritySchema
    from plone import api
    from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
    from plone.app.dexterity.behaviors import constrains

    import logging

    PROFILE_ID = 'profile-ploneconf.site:default'
    logger = logging.getLogger('ploneconf.site')


    def setupVarious(context):

        # Ordinarily, GenericSetup handlers check for the existence of XML files.
        # Here, we are not parsing an XML file, but we use this text file as a
        # flag to check that we actually meant for this import step to be run.
        # The file is found in profiles/default.

        if context.readDataFile('ploneconf.site_various.txt') is None:
            return

        site = api.portal.get()
        set_up_security(site)
        set_up_content(site)


    def set_up_security(site):
        secSchema = ISecuritySchema(site)
        secSchema.set_enable_self_reg(True)


    def set_up_content(site):
        """Create and configure some initial content"""
        if 'talks' in site:
            return
        talks = api.content.create(
            container=site,
            type='Folder',
            id='talks',
            title='Talks')
        api.content.transition(talks, 'publish')
        api.group.grant_roles(
            groupname='AuthenticatedUsers',
            roles=['Contributor'],
            obj=talks)
        # Enable constraining
        behavior = ISelectableConstrainTypes(talks)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['talk'])
        behavior.setImmediatelyAddableTypes(['talk'])
        logger.info("Created and configured %s" % talks.absolute_url())
