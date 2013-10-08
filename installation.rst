Installation & Setup
=====================


Installing Plone
----------------

.. only:: manual

    Plone 4.x requires a working Python 2.6 or 2.7 and several other system-tools that not every OS provides. Therefore the installation of Plone is different on every system. Here are some ways that python can can be used:

.. only:: presentation

    Plone 4.x requires a working Python 2.6 or 2.7 and serveral other tools.

    Installation is different on every system.

* use a Python that comes pre-installed in your operating-system (most Linuxes and Mac OS have one)
* use the `python-buildout <https://github.com/collective/buildout.python>`_
* building Linux-packages
* `homebrew <http://mxcl.github.com/homebrew>`_ (Mac OS X)
* PyWin32 (Windows)

.. only:: manual

    MacOS 10.8 and Ubuntu 12.4 come with a working default Python 2.7 built in. These are the lucky ones. To run a older Plone-version you need Python 2.4 and that's not always easy to install.

    Most developers usually use their primary system to develop Plone.

.. only:: manual

    * Philip has MacOS, therefore he uses the python-buildout to compile all neccessary versions of python and homebrew for some linux-tools.
    * Patrick uses Ubuntu.
    * Alan Runyan (one of Plone's founders) uses Windows. We have no idea how he can live with that but he seems to me managing perfectly well. Plone is much slower on Windows.

.. only:: presentation

    * Philip has MacOS with the python-buildout and homebrew.
    * Patrick uses Ubuntu.
    * Alan Runyan uses Windows.

Plone offers some options for being installed:

1. One-click installers for Mac and Windows (4.3.2 is not yet finished)
2. Unified installers (all 'nix, including MacOS)
3. A vagrant/virtualbox install kit (all platforms)
4. Use your own buildout

You can download all of these at http://plone.org/products/plone/releases/4.3.2


.. only:: manual

    For the training we'll use option 3 and 4 to install and run Plone. We'll create our own buildout and extend it as we wish. But we will do so in a vagrant machine. For your own first experiments we recommend option 2 or 3 (if you have a windows-laptop or encounter problems). Later on you should be able to use your own buildout (we'll cover that later on).

.. only:: presentation

    For the training we'll use option 3 and 4 to install and run Plone.

Read more about installing Plone: https://plone.org/documentation/manual/installing-plone and http://developer.plone.org/getstarted/installation.HTML


Hosting Plone
-------------

.. only:: manual

    If you want to host a real-live Plone-Site yourself then running it from your laptop is not an viable option. A good way to get to know Plone is http://ploud.com where you can host one real Plone-Site for free.

.. only:: presentation

    Try http://ploud.com to host a Plone-Site for free.

You can host Plone...

* with one of many `hosting-providers <http://plone.org/support/hosting-providers>`_
* on a virtual private server
* on dedicated servers
* in the cloud (e.g. using Amazon EC2)

Run Plone on a 5$ plan: http://www.stevemcmahon.com/steves-blog/plone-on-5-a-month

Where to host Plone: http://plone.org/documentation/faq/where-can-i-host-my-plone-site