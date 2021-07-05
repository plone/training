.. _installation-label:

Installation & Setup of **Plone 6**
=====================

**Wording**

A **Plone 6** installation is a combo of a Plone backend [1]_ with a Plone frontend [2]_.
All together we call it Plone.

.. [1] backend: your data is stored here.
.. [2] frontend: that's what your editors see and use.

| Whereas **Plone Classic** is still a valuable installation of Plone.
| *Plone Classic* is a valuable installation of a full featured CMS as it is since decades and still will be.
| *Plone Classic* means: A Plone installation for a Website. No ReactJS stuff, just Plone, just Python. Everything in one installation, backend and frontend.


**And now the sparkling Plone:**

| This training is about Plone.
| This training is about Plone 6.


.. _installation-plone-label:

Installing Plone backend
------------------------

Make sure you have a current and by Plone supported **Python 3** version. 
One way to achieve is `pyenv` which lets you manage different Python versions.
It even let's you setup virtual Pythons of the same version for individual projects.
https://github.com/pyenv/pyenv-installer

.. code-block:: console
    
    pyenv install 3.8.10
    pyenv virtualenv 3.8.10 plonepy
    pyenv activate plonepy

This installs and activates a Python 3.8.10. It does not affect your system Python as it is an isolated virtual Python environment.


Prerequisites
*************

The following instructions are based on Ubuntu and macOS.
If you use a different operating system (OS), please adjust them to fit your OS.

On Ubuntu/Debian, you need to make sure your system is up-to-date:

.. code-block:: console

    sudo apt-get update
    sudo apt-get -y upgrade

Then, you need to install the following packages:

.. code-block:: console

    sudo apt-get install python3.7-dev python3.7-tk python3.7-venv build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
    sudo apt-get install libreadline-dev wv poppler-utils
    sudo apt-get install git

On MacOS you at least need to install some dependencies with `Homebrew <https://brew.sh/>`_

.. code-block:: console

    brew install zlib git readline jpeg libpng libyaml


.. seealso::

    For more information or in case of problems see the `official installation instructions <https://docs.plone.org/manage/installing/installation.html>`_.


Get Plone backend and install
*********************

Download Plone from https://plone.org/download

Follow the instructions. Select option 'standalone' for your first Plone installation.

.. note::

    You do not find a Plone 6 to download? 
    Well it's not released.
    We still do a Plone 6 setup: Plone backend plus Plone frontend.
    If Plone backend is still a Plone 5, that's OK.

.. TODO::

    Install necessary helpers for Volto frontend: restapi, folderish contenttypes, dexterity root,…


.. _installation-Volto-label:

Installing Plone frontend
-------------------------

| For a Plone 6 installation by now two installations are needed: Plone backend and Volto frontend. The former section is describing the options for a Plone backend installation.
| This section is about setting up a Volto project.


Install pre-requisites:

#.  Install `nvm` (Node Version Manager) to manage `node` versions.

    .. code-block:: bash

        # macOS
        brew install nvm

        #Linux
        apt-get install nvm

#.  Install `node` LTS (node version LTS: long time support)

    .. code-block:: bash

        nvm install --lts

#.  Install package manager `yarn`.

    .. code-block:: bash

        npm install --global yarn

Create your Volto project:

#.  Generate a project with yeoman

    .. code-block:: bash

        npm init yo @plone/volto

    | It will take a while to install all dependencies.
    | `yo` will ask questions. Respond to the first by entering your project name, the next by pressing :kbd:`Enter` and to the other two by now with ``false``.

    The output will look like this:

    .. code-block:: console

        me@here sandbox % npm init yo @plone/volto
        npx: installed 14 in 3.392s
        Getting latest Volto version
        Retrieving Volto's yarn.lock
        Using latest released Volto version: 10.4.1
        ? Project name volto-project-myprojectname
        ? Project description A Volto-powered Plone frontend
        ? Would you like to add addons? false
        ? Would you like to add workspaces? false
           create volto-project-myprojectname/package.json
           create volto-project-myprojectname/yarn.lock
           create volto-project-myprojectname/.eslintrc.js
           ...

#.  Start up the project **volto-project-myprojectname** with

    .. code-block:: bash

        cd volto-project-myprojectname
        yarn start

If successful, you get:

    🎭 Volto started at http://localhost:3000 🚀


Create a Plone site object **Plone** on http://localhost:8080

Point your browser to http://localhost:3000 and see that Plone is up and running.


You can stop the Volto app anytime using :kbd:`ctrl + c`.


.. seealso::

    For more information see `Volto documentation <https://docs.voltocms.com/getting-started/install/>`_.


.. _installation-hosting-label:

Hosting Plone
-------------

.. only:: not presentation

    If you want to host a real live Plone site yourself then running it from your laptop is not a viable option.

You can host Plone...

* with one of many professional `hosting providers <https://plone.com/providers>`_
* on a virtual private server
* on dedicated servers
* on `Heroku <https://www.heroku.com>`_ you can run Plone for *free* using the `Heroku buildpack for Plone <https://github.com/plone/heroku-buildpack-plone>`_

.. seealso::

    Plone Installation Requirements: https://docs.plone.org/manage/installing/requirements.html


.. _installation-prod-deploy-label:

Production Deployment
---------------------

The way we are setting up a Plone site during this class may be adequate for a small site
— or even a large one that's not very busy — but you are likely to want to do much more if you are using Plone for anything demanding.

* Using a production web server like Apache or nginx for URL rewriting, SSL and combining multiple, best-of-breed solutions into a single web site.

* Reverse proxy caching with a tool like Varnish to improve site performance.

* Load balancing to make best use of multiple core CPUs and even multiple servers.

* Optimizing cache headers and Plone's internal caching schemes with plone.app.caching.

And, you will need to learn strategies for efficient backup and log file rotation.

All these topics are introduced in `Guide to deploying and installing Plone in production <https://docs.plone.org/manage/deploying/index.html>`_.
