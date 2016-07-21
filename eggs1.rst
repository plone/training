Creating addons to customize Plone
==================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/12_eggs1/ src/ploneconf.site

In this part you will:

* Create a custom python distribution ``ploneconf.site`` to hold all the code
* Modify buildout to install that distribution


Topics covered:

* mr.bob and bobtemplates.plone
* the structure of eggs


Creating the distribution
-------------------------

Our own code has to be organized as a python distribution, also called *egg*. An egg is a zip file or a directory that follows certain conventions. We are going to use `bobtemplates.plone <https://pypi.python.org/pypi/bobtemplates.plone>`_ to create a skeleton project. We only need to fill in the blanks.

We create and enter the ``src`` directory (*src* is short for *sources*) and call a script called ``mrbob`` from our buildout's bin directory:

.. code-block:: bash

    $ mkdir src      # (if src does not exist already)
    $ cd src
    $ ../bin/mrbob -O ploneconf.site bobtemplates:plone_addon

We have to answer some questions about the add-on. We will press :kbd:`Enter` (i.e. choosing the default value) for all questions except 3 (where you enter your github username if you have one) and 5 (Plone version), where we enter :kbd:`4.3.10`.

..  code-block:: bash

    --> What kind of package would you like to create? Choose between 'Basic', 'Dexterity', and 'Theme'. [Basic]:

    --> Author's name [Philip Bauer]:

    --> Author's email [bauer@starzel.de]:

    --> Author's github username: fulv

    --> Package description [An add-on for Plone]:

    --> Plone version [4.3.9]: 4.3.10

    Generated file structure at /vagrant/buildout/src/ploneconf.site

.. only:: not presentation

    If this is your first egg, this is a very special moment. We are going to create the egg with a script that generates a lot of necessary files. They all are necessary, but sometimes in a subtle way. It takes a while to understand their full meaning. Only last year I learned and understood why I should have a ``MANIFEST.in`` file. You can get along without one, but trust me, you get along better with a proper manifest file.


.. _eggs1-inspect-label:

Inspecting the distribution
---------------------------

In ``src`` there is now a new folder ``ploneconf.site`` and in there is the new distribution. Let's have a look at some of the files:

bootstrap-buildout.py, buildout.cfg, travis.cfg, .travis.yml, .coveragerc
    You can ignore these files for now. They are here to create a buildout only for this egg to make testing it easier. Once we start writing tests for this distribution we will have another look at them.

README.rst, CHANGES.rst, CONTRIBUTORS.rst, docs/
    The documentation, changelog, the list of contributors and the license of your egg goes in here.

setup.py
    This file configures the distribution, its name, dependencies and some metadata like the author's name and email address. The dependencies listed here are automatically downloaded when running buildout.

src/ploneconf/site/
    The distribution itself lives inside a special folder structure. That seems confusing but is necessary for good testability. Our distribution contains a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_ called *ploneconf.site* and because of this there is a folder ``ploneconf`` with a ``__init__.py`` and in there another folder ``site`` and in there finally is our code.
    From the buildout's perspective our code is in ``<your buildout directory>/src/ploneconf.site/src/ploneconf/site/<real code>``


.. note::

    Unless discussing the buildout we will from now on silently omit these folders when describing files and assume that ``<your buildout directory>/src/ploneconf.site/src/ploneconf/site/`` is the root of our distribution!


configure.zcml (src/ploneconf/site/configure.zcml)
    The phone book of the distribution. By reading it you can find out which functionality is registered though the component architecture.

setuphandlers.py (src/ploneconf/site/setuphandlers.py)
    This holds code that is automatically run when installing and uninstalling our add-on.

interfaces.py (src/ploneconf/site/interfaces.py)
    Here a browserlayer is defined in a straightforward python class. We will need it later.

testing.py
    This holds the setup for running tests.

tests/
    This holds the tests.

browser/
    This directory is a python package (because it has a ``__init__.py``) and will by convention hold most things that are visible in the browser.

browser/configure.zcml
    The phonebook of the browser package. Here views, resources and overrides are registered.

browser/overrides/
    This add-on is already configured to allow overriding existing default Plone templates.

browser/static/
    A directory that holds static resources (images/css/js). The files in here will be accessible through URLs like ``++resource++ploneconf.site/myawesome.css``

profiles/default/
    This folder contains the GenericSetup profile. During the training we will put some xml files here that hold configuration for the site.

profiles/default/metadata.xml
    Version number and dependencies that are auto-installed when installing our add-on.

..    profiles/uninstall/
      This folder holds another GenericSetup profile. The steps in here are executed on uninstalling.


Including the egg in Plone
--------------------------

Before we can use our new addon we have to tell Plone about it. Edit ``buildout.cfg`` and uncomment ``ploneconf.site`` in the `eggs` and `sources` sections:

.. code-block:: cfg
    :emphasize-lines: 4, 11

    eggs =
        Plone
        ...
        ploneconf.site
    #    starzel.votable_behavior

    ...

    [sources]
    collective.behavior.banner = git https://github.com/collective/collective.behavior.banner.git pushurl=git@github.com:collective/collective.behavior.banner.git rev=af2dc1f21b23270e4b8583cf04eb8e962ade4c4d
    ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site
    # starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git

This tells Buildout to add the egg ``ploneconf.site``. Since it is also in the `sources`-section Buildout will not try to download it from pypi but will expect it in ``src/ploneconf.site``. *fs* allows you to add packages on the file system without a version control system, or with an unsupported one.

Now run buildout to reconfigure Plone with the updated configuration:

.. code-block:: bash

    $ ./bin/buildout

After restarting Plone with ``./bin/instance fg`` the new addon `ploneconf.site` is available for install like PloneFormGen or Plone True Gallery.

We will not install it now since we did not add any of our own code or configuration yet. Let's do that.

Return to Dexterity: moving content types into code
---------------------------------------------------

Remember the *Talks* content type that we created through-the-web with Dexterity? Let's move that new content type into our add-on package so that it may be installed in other sites without TTW manipulation.

Steps:

* Return to the Dexterity control panel
* Export the Type Profile and save the file
* Delete the Type from the site before installing it from the file system
* Extract the files from the exported tar-file and add them to our addon-package in ``ploneconf/site/profiles/default/``

The file ``ploneconf/site/profiles/default/types.xml`` tells plone that there is a new content type defined in file ``talk.xml``.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <property name="title">Controls the available content types in your portal</property>
     <object name="talk" meta_type="Dexterity FTI"/>
     <!-- -*- more types can be added here -*- -->
    </object>

Upon installing, Plone reads the file ``ploneconf/site/profiles/default/types/talk.xml`` and registers a new type in ``portal_types`` (you can find this tool in the ZMI) with the information taken from that file.

.. code-block:: xml
  :linenos:

    <?xml version="1.0"?>
    <object name="talk" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <property name="title" i18n:translate="">Talk</property>
     <property name="description" i18n:translate="">None</property>
     <property name="icon_expr">string:${portal_url}/document_icon.png</property>
     <property name="factory">talk</property>
     <property name="add_view_expr">string:${folder_url}/++add++talk</property>
     <property name="link_target"></property>
     <property name="immediate_view">view</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types"/>
     <property name="allow_discussion">False</property>
     <property name="default_view">view</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     <property name="default_view_fallback">False</property>
     <property name="add_permission">cmf.AddPortalContent</property>
     <property name="klass">plone.dexterity.content.Container</property>
     <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
     </property>
     <property name="schema"></property>
     <property
        name="model_source">&lt;model xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns="http://namespaces.plone.org/supermodel/schema"&gt;
        &lt;schema&gt;
          &lt;field name="type_of_talk" type="zope.schema.Choice"&gt;
            &lt;description/&gt;
            &lt;title&gt;Type of talk&lt;/title&gt;
            &lt;values&gt;
              &lt;element&gt;Talk&lt;/element&gt;
              &lt;element&gt;Training&lt;/element&gt;
              &lt;element&gt;Keynote&lt;/element&gt;
            &lt;/values&gt;
          &lt;/field&gt;
          &lt;field name="details" type="plone.app.textfield.RichText"&gt;
            &lt;description&gt;Add a short description of the talk (max. 2000 characters)&lt;/description&gt;
            &lt;max_length&gt;2000&lt;/max_length&gt;
            &lt;title&gt;Details&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="audience" type="zope.schema.Set"&gt;
            &lt;description/&gt;
            &lt;title&gt;Audience&lt;/title&gt;
            &lt;value_type type="zope.schema.Choice"&gt;
              &lt;values&gt;
                &lt;element&gt;Beginner&lt;/element&gt;
                &lt;element&gt;Advanced&lt;/element&gt;
                &lt;element&gt;Professionals&lt;/element&gt;
              &lt;/values&gt;
            &lt;/value_type&gt;
          &lt;/field&gt;
          &lt;field name="speaker" type="zope.schema.TextLine"&gt;
            &lt;description&gt;Name (or names) of the speaker&lt;/description&gt;
            &lt;title&gt;Speaker&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="email" type="zope.schema.TextLine"&gt;
            &lt;description&gt;Adress of the speaker&lt;/description&gt;
            &lt;title&gt;Email&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="image" type="plone.namedfile.field.NamedBlobImage"&gt;
            &lt;description/&gt;
            &lt;required&gt;False&lt;/required&gt;
            &lt;title&gt;Image&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="speaker_biography" type="plone.app.textfield.RichText"&gt;
            &lt;description/&gt;
            &lt;max_length&gt;1000&lt;/max_length&gt;
            &lt;required&gt;False&lt;/required&gt;
            &lt;title&gt;Speaker Biography&lt;/title&gt;
          &lt;/field&gt;
        &lt;/schema&gt;
      &lt;/model&gt;</property>
     <property name="model_file"></property>
     <property name="schema_policy">dexterity</property>
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     <action title="View" action_id="view" category="object" condition_expr=""
        description="" icon_expr="" link_target="" url_expr="string:${object_url}"
        visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        description="" icon_expr="" link_target=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

Now our package has some real contents. So, we'll need to reinstall it (if installed before).

* Restart Plone.
* Re-install ploneconf.site (deactivate and activate).
* Go to the ZMI and look at the definition of the new type in ``portal_types``.
* Test the type by adding an object or editing one of the old ones.
* Look at how the talks are presented in the browser.

