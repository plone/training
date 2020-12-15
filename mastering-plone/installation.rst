.. _installation-label:

Installation & Setup
=====================

A Plone 6 installation is both:

* Plone Classic
* Plone with React frontend Volto

.. sidebar:: Installation & Setup

    .. contents:: Table of Contents
        :depth: 4


.. _installation-plone-label:

Installing Plone
----------------

Python versions required by Plone from version 4.3.x on.

=========  ================
  Plone         Python
=========  ================
 4.3.x      2.7
 5.0.x      2.7
 5.1.x      2.7.9
 5.2.x      2.7.14 or 3.6+
 6.0.x      3.6+
=========  ================

Plone 5.x requires a working Python 2.7 (or Python 3.6+ for Plone 5.2.x) and other system tools that not every OS provides.
The installation of Plone is different on every system.
Here are some ways that Python can be installed:

* use a Python that comes pre-installed in your operating system (most Linux Distributions and macOS have one)
* use the `python buildout <https://github.com/collective/buildout.python>`_
* building Linux packages
* `Homebrew <https://brew.sh>`_ (macOS)
* PyWin32 (Windows)

Most developers use their primary system to develop Plone.
For complex setups they often use Linux virtual machines.

* macOS: Use the system python and `Homebrew <https://brew.sh>`_ for some missing Linux tools.
* Linux: Depending on your Linux flavor you might have to install Python 3.7 yourself and install some tools.
* Windows: Alan Runyan (one of Plone's founders) uses it. A downside: Plone seems to be running slower on Windows.

Plone offers multiple options for being installed:

1. Unified installers (all 'nix, including macOS)
2. A `Docker Image <https://hub.docker.com/_/plone/>`_
3. A `Ansible Playbook <http://docs.plone.org/external/ansible-playbook/docs>`_
4. A `Windows installer <https://github.com/plone/WinPloneInstaller>`_
5. A Vagrant/VirtualBox install kit (all platforms)
6. Use your own Buildout

Visit the `download page <https://plone.org/download>`_ to see all the options.


.. only:: not presentation

    For the training you will use option 2 or 5 to install and run Plone.
    We will create our own Buildout and extend it as we wish.
    If you choose to do so you will run it in a Vagrant machine.

    For your own first experiments we recommend option 1 or 2 (if you have a Windows laptop or encounter problems).
    Later on you should be able to use your own Buildout (we will cover that later on).

.. only:: presentation

    For the training we will use option 2 or 5 to install and run Plone.

.. seealso::

    * https://docs.plone.org/manage/installing/installation.html


.. _installation-Volto-label:

Installing Volto
----------------

| For a Plone 6 installation, not Plone Classic, but with the React frontend **Volto**, by now two installations are needed: Plone and Volto. The former section is describing the options for a Plone installation.
| This section is about setting up a Volto installation. Wording is: Volto installation, Volto app, **Volto project**.


Install pre-requisites.

#.  Install ``nvm`` (Node Version Manager) to manage ``node`` versions.

    .. code-block:: bash

        # macOS
        brew install nvm

        #Linux
        apt-get install nvm

#.  Install node LTS (node version LTS: long time support)

    .. code-block:: bash

        nvm install --lts


Create your Volto project.

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


For more information see `Volto documentation <https://docs.voltocms.com/getting-started/install/>`_


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

    * Plone Installation Requirements: https://docs.plone.org/manage/installing/requirements.html


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
