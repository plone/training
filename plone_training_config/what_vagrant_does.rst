What Vagrant does
-----------------

.. note::

    These steps are automatically done by vagrant and puppet. They are only explained here if you want to know what goes on below the hood.

Puppet does the first installation, Puppet is a tool to automatically manage servers (real and virtual). We won't get into Puppet since it is not that widely used. This is what we basically do if we did it by hand:

First we update the ubuntu and install some packages.

.. code-block:: bash

    $ sudo aptitude update --quiet --assume-yes
    $ sudo apt-get install build-essential
    $ sudo apt-get install python-dev
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

Then we create a virtual python environment using virtualenv. This is alway a good practice since that way we get a clean copy of our system-python, we can't break it by installing eggs that might collide with other eggs::

    $ virtualenv --no-site-packages /home/vagrant/py27

Then we download, unpack and install the unified installer of Plone.

.. code-block:: bash

    $ mkdir Plone
    $ mkdir tmp
    $ cd tmp
    $ wget https://launchpad.net/plone/4.3/4.3.3/+download/Plone-4.3.3-UnifiedInstaller.tgz
    $ tar xzf Plone-4.3.3-UnifiedInstaller.tgz
    $ cd Plone-4.3.3-UnifiedInstaller
    $ ./install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/Plone

The unified installer is an amazing tool that compiles it's own python, brings with it all the python-eggs we need and puts them in a buildout-cache. It then creates a Buildout and makes Plone ready to run.

We will not actually use this Plone during the training. If you want to use it for your own experiments, you can find it in ``/home/vagrant/Plone/zinstance`` on the virtual machine.

Instead vagrant now creates our own little Buildout and only uses the eggs that the unified installer created. First we copy the buildout-cache that holds all the python-packages that Plone consists of.

.. code-block:: bash

    $ cp -Rf /home/vagrant/Plone/buildout-cache /home/vagrant

Then we checkout our tutorial buildout from http://github.com/collective/training_buildout and build it.

.. code-block:: bash

    $ cd /vagrant
    $ git clone https://github.com/collective/training_buildout.git buildout
    $ cd buildout
    $ /home/vagrant/py27/bin/python bootstrap.py
    $ ./bin/buildout

At this point vagrant has finished it's job.

You can now connect to the machine and start plone.

.. code-block:: bash

    $ vagrant ssh
    $ cd /vagrant/buildout
    $ ./bin/instance fg

Now we have fresh Buildout based Zope site, ready to get a Plone site. Go to http://localhost:8080 and create a Plone site, only activate the  :guilabel:`Dexterity-based Plone Default Types` plugin.

You might wonder, why we use the unified installer. We use the unified installer to set up a cache of packages to download in a much shorter time. Without it, your first Buildout on a fresh computer would take more than half an hour on a good internet connection.