.. _installation-label:

Installation & Setup of **Plone 6**
=====================

**Wording**:

A **Plone 6** installation is a combo of a Plone backend [1]_ with a Plone frontend [2]_. All together we call it Plone.

.. [1] backend: your data is stored here.
.. [2] frontend: that's what your editors see and use.

| Whereas **Plone Classic** is still a valuable installation of Plone.
| *Plone Classic* is a valuable installation of a full featured CMS as it is since decades and still will be.
| *Plone Classic* means: A Plone installation for a Website. No ReactJS stuff, just Plone, just Python. Everything in one installation.

**And now the sparkling Plone:**

| This training is about Plone.
| This training is about Plone 6.

TODO description of Plone (Plone 6 bla bla bla)


.. _installation-plone-label:

Installing Plone
----------------

TODO shorten section 'Installing & Setup Plone'

get pyenv

get Plone

basta

.. seealso::

    * https://docs.plone.org/manage/installing/installation.html


.. _installation-Volto-label:

Installing Volto
----------------

| For a Plone 6 installation, not just Plone Classic, but with the React frontend **Volto**, by now two installations are needed: Plone and Volto. The former section is describing the options for a Plone installation.
| This section is about setting up a Volto project.


Install pre-requisites.

#.  Install ``nvm`` (Node Version Manager) to manage ``node`` versions.

    .. code-block:: bash

        # macOS
        brew install nvm

        #Linux
        apt-get install nvm

#.  Install ``node`` LTS (node version LTS: long time support)

    .. code-block:: bash

        nvm install --lts

#.  Install package manager ``yarn``.

    .. code-block:: bash

        npm install --global yarn

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
