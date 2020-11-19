.. _volto_custom_addon-label:

Extending Volto With Custom Add-on Package
==========================================

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  Creating a Volto add-on


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout



As soon as you have repeating needs in Volto projects, you will want to move the code to an addon-on that can be applied to multiple projects. One of several ways to start with a new add-on is the **EEA Volto add-on template** on github at https://github.com/eea/volto-addon-template.

As stated in its wiki the setup process is:

1. `Create a new repository <https://github.com/eea/volto-addon-template/generate>`_ from volto-addon-template

2. Clone your new repository on your local machine like:

    ..  code-block:: bash

            $ git clone https://github.com/collective/volto-custom-addon
            $ cd volto-custom-addon

3. Bootstrap

    ..  code-block:: bash

            $ yarn bootstrap

4. See changes and commit:

    ..  code-block:: bash
    
            $ git diff
            $ git commit -am "Initial commit"
            $ git push


Develop your new add-on
-----------------------

Create a sandbox project

..  code-block:: bash

    yo @plone/volto sandbox-volto-custom-addon --addon collective/volto-custom-addon

Install mrs.developer to let the project know about the *source* of your add-on.

..  code-block:: bash

    yarn add mrs-developer -W

Update :file:`package.json`:

..  code-block:: bash

    "scripts": {
        …
        "develop": "missdev --config=jsconfig.json --output=addons",
    }

The configuration file :file:`mrs.developer.json` instructs mrs.developer from where it has to pull the package. So, create mrs.developer.json and add:

..  code-block:: bash

    {
        "collective-volto-custom-addon": {
            "package": "@plone-collective/volto-custom-addon",
            "url": "git@github.com:collective/volto-custom-addon.git",
            "path": "src"
        }
    }

run

..  code-block:: bash

    yarn develop

You see your addon cloned to `src/addons/`.

Read more about `mrs.developer` [2]_ configuration options.

With mrs.developer set up to code your add-on, its just left to add the add-on as any add-on to your Volto project:

Update :file:`package.json`:

..  code-block:: bash


    "workspaces": [
      "src/addons/*"
    ],
    "addons": [
      …
      "@plone-collective/volto-custom-addon"
    ],
    "dependencies": {
        …
        "@plone-collective/volto-custom-addon": "github:collective/volto-custom-addon"
    },

Install and start

..  code-block:: bash

    $ yarn
    $ yarn start


Step to the next chapter :doc:`volto_custom_addon2` to see how to create a new block type. We will do this in an add-on to apply the feature to multiple projects.

.. NOTE:: You can now release the new add-on to npm. 


Enrich an existing project with your new released add-on
--------------------------------------------------------

You already released your add-on. Go on with `package.json`and add your new add-on.

Update `package.json`:

..  code-block:: bash

    "addons": [
      …
      "@plone-collective/volto-custom-addon"
    ],
    "workspaces": [
      "src/addons/*"
    ],
    "dependencies": {
      …
      "@plone-collective/volto-custom-addon": "1.0.1"
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


