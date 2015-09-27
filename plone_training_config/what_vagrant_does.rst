What Vagrant does
-----------------

.. note::

    These steps are automatically done by vagrant and puppet. They are only explained here if you want to know what goes on under the hood.

Puppet does the first installation. Puppet is a tool to automatically manage servers (real and virtual). We won't get into Puppet since it is not that widely used. This is basically what Puppet does if we did it by hand:

First we update Ubuntu and install some packages.

.. code-block:: bash

    $ sudo aptitude update --quiet --assume-yes
    $ sudo apt-get install build-essential
    $ sudo apt-get install python-dev
    $ sudo apt-get install python-tk
    $ sudo apt-get install libjpeg-dev
    $ sudo apt-get install libxml2-dev
    $ sudo apt-get install libxslt-dev
    $ sudo apt-get install git
    $ sudo apt-get install libz-dev
    $ sudo apt-get install libssl-dev
    $ sudo apt-get install subversion
    $ sudo apt-get install wget
    $ sudo apt-get install curl
    $ sudo apt-get install elinks
    $ sudo apt-get install vim
    $ sudo apt-get install gettext
    $ sudo apt-get install python-virtualenv
    $ sudo apt-get install putty-tools

Then we create a virtual python environment using virtualenv. This is always a good practice since that way we get a clean copy of our system python, so that we can't break it by installing eggs that might collide with other eggs.

.. code-block:: bash

    $ virtualenv --no-site-packages /home/vagrant/py27

Now we download and unpack a buildout-cache that holds all the python packages that the a version of Plone consists of. We could skip this step and have buildout download all packages individually but that takes much longer.

.. code-block:: bash

    $ wget http://dist.plone.org/release/5.0rc3/buildout-cache.tar.bz2
    $ tar xjf buildout-cache.tar.bz2

Then we check out our tutorial buildout from https://github.com/collective/training_buildout and build it.

.. code-block:: bash

    $ cd /vagrant
    $ git clone https://github.com/collective/training_buildout.git buildout
    $ cd buildout
    $ /home/vagrant/py27/bin/python bootstrap.py
    $ ./bin/buildout -c vagrant_provisioning.cfg

This will download additional eggs that are not yet part of the buildout-cache and configure Plone to be ready to run.

At this point vagrant has finished its job.

You can now connect to the machine and start Plone.

.. code-block:: bash

    $ vagrant ssh
    $ cd /vagrant/buildout
    $ ./bin/instance fg

Now we have a fresh Buildout-based Zope site, ready to add a Plone site. Go to http://localhost:8080 and create a Plone site.
