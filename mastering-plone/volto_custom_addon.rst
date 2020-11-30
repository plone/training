.. _volto_custom_addon-label:

Extending Volto With Custom Add-on Package
==========================================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  This chapter is about the React frontend Volto.

  Solve the same tasks in classic frontend in chapter :doc:`eggs1`


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout



As soon as you have repeating needs in Volto projects, you will want to move the code to an addon-on that can be applied to multiple projects. One of several ways to start with a new add-on is the Yeoman generator we already used to initiate a Volto app.

.. _volto_custom_addon-preparation-label:

If you haven't prepared Yeoman and the generator **recently**:

..  code-block:: bash

    npm install -g yo
    npm install -g @plone/generator-volto

Create a sandbox project

..  code-block:: bash

    yo @plone/volto sandbox-volto-custom-addon

You see a dialog like this

.. code-block:: bash
    :linenos:
    :emphasize-lines: 7,10

    yo @plone/volto sandbox-volto-custom-addon
    Getting latest Volto version
    Retrieving Volto's yarn.lock
    Using latest released Volto version: 9.0.0
    ? Project description A Volto-powered Plone frontend
    ? Would you like to add addons? true
    ? Addon name, plus extra loaders, like: volto-addon:loadExtra,loadAnotherExtra @greenthumb/volto-custom-addon
    ? Would you like to add another addon? false
    ? Would you like to add workspaces? true
    ? Workspace path, like: src/addons/volto-addon src/addons/greenthumb-volto-custom-addon
    ? Would you like to add another workspace? false

@greenthumb/volto-custom-addon is the scoped package name of your add-on.

Go to the app folder:

..  code-block:: bash

    cd sandbox-volto-custom-addon

You now have a Volto app configured for an add-on. An add-on is a Node package. It will live in the folder you specified: :file:`src/addons/greenthumb-volto-custom-addon`. So you need a package.json. As it should customize your Volto app, it needs also a way to manipulate the main configuration. As a starter you can create a repository from template https://github.com/rohberg/volto-addon-template.git.

.. figure:: _static/volto-addon-template.png
    :scale: 50%
    :alt: Voto add-on template

Your repo https://github.com/greenthumb/volto-custom-addon.git is the basis of your add-on. We are now integrating it in your Volto app.

Install mrs.developer to let the project know about the *source* of your add-on.

..  code-block:: bash

    yarn add mrs-developer -WD

The configuration file :file:`mrs.developer.json` instructs mrs.developer from where it has to pull the package. So, create mrs.developer.json and add:

..  code-block:: bash

    {
        "greenthumb-volto-custom-addon": {
            "package": "@greenthumb/volto-custom-addon",
            "url": "git@github.com:greenthumb/volto-custom-addon.git",
            "path": "src"
        }
    }

Run

..  code-block:: bash

    yarn develop

You see your add-on cloned to `src/addons/`.

Read more about `mrs.developer` [2]_ configuration options.

Change to add-on folder and replace *rohberg* -> *greenthumb* and replace *volto-addon-template* -> *volto-custom-addon*.


With mrs.developer set up to code your add-on, its just left to add the add-on as any add-on to your Volto project:

Update :file:`package.json`:

..  code-block:: bash


    "workspaces": [
      "src/addons/*"
    ],
    "addons": [
      …
      "@greenthumb/volto-custom-addon"
    ],

Install and start

..  code-block:: bash

    $ yarn
    $ yarn start

Troubleshooting: Did you :ref:`update the generator recently <volto_custom_addon-preparation-label>`?

.. _volto_custom_addon-final-label:

..  admonition:: Step to the next chapter and come back here for a release.

    We will create a new block type in the next chapter :doc:`volto_custom_addon2`. We will do this in an add-on to apply the feature to multiple projects.

.. NOTE:: Coming back here with the new block type, you can now release the new add-on to npm. @greenthumb is your space.


Enrich an existing project with your new released add-on
--------------------------------------------------------

You already released your add-on. Go on with :file:`package.json` and add your new add-on.

Update `package.json`:

..  code-block:: bash

    "addons": [
      …
      "@greenthumb/volto-custom-addon"
    ],
    "workspaces": [
      "src/addons/*"
    ],
    "dependencies": {
      …
      "@greenthumb/volto-custom-addon": "1.0.1"
    },

Modify versions as necessary.


Install new add-on and restart Volto:

..  code-block:: bash

    $ yarn
    $ yarn start


Create a new project with your new released add-on
---------------------------------------------------

..  code-block:: bash

    yo @plone/volto my-volto-project --addon collective/volto-custom-addon


Install and start

..  code-block:: bash

    $ yarn
    $ yarn start




Footnotes
----------------

.. [1] `yarn workspaces <https://classic.yarnpkg.com/en/docs/workspaces/>`_
    Workspaces are a new way to set up your package architecture. It allows you to setup multiple packages in such a way that you only need to run yarn install once to install all of them in a single pass.

.. [2] `mrs.developer <https://www.npmjs.com/package/mrs-developer>`_ Pull a package from git and set it up as a dependency for the current project codebase.


