Installation & Setup
=====================


Installing Plone
----------------

.. only:: not presentation

    Plone 4.3.x requires a working Python 2.7 and several other system-tools that not every OS provides. Therefore the installation of Plone is different on every system. Here are some ways that Python can can be used:

.. only:: presentation

    Plone 4.3.x requires a working Python 2.7 and several other tools.

    Installation is different on every system.

* use a Python that comes pre-installed in your operating-system (most Linuxes and Mac OS have one)
* use the `python-buildout <https://github.com/collective/buildout.python>`_
* building Linux-packages
* `homebrew <http://mxcl.github.com/homebrew>`_ (Mac OS X)
* PyWin32 (Windows)

.. only:: not presentation

    MacOS 10.8 and Ubuntu 14.04 come with a working default Python 2.7 built in. These are the lucky ones. To run a Plone-version older than 4.0 you need Python 2.4. That's not always easy to install.

Most developers use their primary system to develop Plone. For complex setups they often use virtual linux-machines.

* OS X: Use the python-buildout to compile python and homebrew for some missing linux-tools.
* Linux: Depending on your linux-flavor you might have to build python yourself and install some tools.
* Windows: Alan Runyan (one of Plone's founders) uses it. A downside: Plone seems to be running much slower on Windows.

Plone offers multiple options for being installed:

1. One-click installers for Mac and Windows
2. Unified installers (all 'nix, including MacOS)
3. A vagrant/virtualbox install kit (all platforms)
4. Use your own Buildout

You can download all of these at http://plone.org/products/plone/releases/4.3.3


.. only:: not presentation

    For the training we'll use option 3 and 4 to install and run Plone. We'll create our own Buildout and extend it as we wish. But we will do so in a vagrant machine. For your own first experiments we recommend option 2 or 3 (if you have a windows-laptop or encounter problems). Later on you should be able to use your own Buildout (we'll cover that later on).

.. only:: presentation

    For the training we'll use option 3 and 4 to install and run Plone.

.. seealso::

    * https://plone.org/documentation/manual/installing-plone
    * http://docs.plone.org/manage/installing/installation.html


Hosting Plone
-------------

.. only:: not presentation

    If you want to host a real-live Plone-Site yourself then running it from your laptop is not a viable option.

You can host Plone...

* with one of many professional `hosting-providers <http://plone.org/support/hosting-providers>`_
* on a virtual private server
* on dedicated servers
* on `heroku <http://heroku.com>`_ you can run Plone for *free* using the `Heroku buildpack for Plone <https://github.com/niteoweb/heroku-buildpack-plone>`_
* in the cloud (e.g. using Amazon EC2 or `Codio.com <http://blog.dbain.com/2014/04/install-plone-in-under-5-minutes-on.html>`_)

.. seealso::

    * Plone Installation Requirements: http://docs.plone.org/manage/installing/requirements.html
    * Run Plone on a 5$ plan: http://www.stevemcmahon.com/steves-blog/plone-on-5-a-month
    * Where to host Plone: http://plone.org/documentation/faq/where-can-i-host-my-plone-site
    * Guide to deploying and installing Plone in production: http://docs.plone.org/manage/deploying/index.html
