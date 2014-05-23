Installing Plone for the Training
=================================



To not waste too much time with installing and debugging the differences between systems we use a virtual machine (Ubuntu 14.04) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development-environment to everyone.

`Vagrant <http://www.vagrantup.com>`_ is a tool for building complete development environments. We use it together with Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage a virtual environment.

Keep in mind that you need a fast internet-connection during the process since you'll have to download a complete virtual machine (ubuntu) and several packages and updates.

.. warning::

    We recommend using a virtual machine for the training if you are not used to running Plone on your laptop.

    You can also work on your own machine with your own Python if you want to but **please please please** make sure that you have a system that will work since we don't want you to lose valuable time.

    If you want to use your own system use the Buildout at https://github.com/starzel/training_without_vagrant.git (since the one we set up via puppet has several directories set to folders not shared with the host).

    Set up Plone for the training like this if you don't want to use a VM:

    .. code-block:: bash

        $ mkdir training
        $ cd training
        $ git clone https://github.com/starzel/training_without_vagrant.git buildout
        $ cd buildout
        $ virtualenv py27
        $ ./py27/bin/python bootstrap.py
        $ ./bin/buildout

Install VirtualBox
-------------------------

Vagrant uses Oracle’s VirtualBox to create virtual environments. Here is a link directly to the download page: https://www.virtualbox.org/wiki/Downloads. We use VirtualBox  4.3.x.


Install and configure Vagrant
-----------------------------

Get the latest version from http://www.vagrantup.com/downloads for your operating system and install it.

.. note::

    In Windows there is a bug in the recent version of Vagrant. Here are the instruction how to work around the warning ``Vagrant could not detect VirtualBox! Make sure VirtualBox is properly installed``.

Now your system has a command ``vagrant`` that you can run in the terminal.

First create a directory where you want to do the training in.

.. code-block:: bash

    $ mkdir training
    $ cd training

Setup Vagrant to automatically install the current guest-additions. You can choose to skip this step if you encounter any problems with it.

.. code-block:: bash

    $ vagrant plugin install vagrant-vbguest

Now either unzip the attachment (if you read this as a mail) or download the zip file http://www.starzel.de/plone-tutorial/plone_training_config.zip and copy its contents into your training directory. It should now hold the file "Vagrantfile" and the directory ``manifests``.

Start the VM that we configured in "Vagrantfile"

.. code-block:: bash

    $ vagrant up

This takes a **veeeeery loooong time** since it:

* downloads a virtual machine (Official Ubuntu Server 14.04 LTS, also called "Trusty Tahr")
* sets up the VM
* updates the VM
* installs various packages needed for Plone development
* downloads and unpack the unified installer for Plone
* runs the unified installer for Plone.
* copy the eggs to a location we use in the training
* clones the training-buildout into /vagrant/buildout
* builds Plone using the eggs from the buildout-cache

.. note::

    Sometimes this stops with the message *Skipping because of failed dependencies*.

    .. code-block:: bash

        Skipping because of failed dependencies

    If this happens or you have the feeling that something has gone wrong and the installation has not finished correctly for some reason you need to run try   the following command to repeat the process. This will only repeat steps that have not finished correctly.

    .. code-block:: bash

        $ vagrant provision

    You can do this multiple times to fix problems, e.g. if your network-connection was down and steps could not finish because of this.

Once Vagrant finishes the provisioning-process, you can login to the now running virtual machine.

.. code-block:: bash

    $ vagrant ssh

.. note::

    If you have to use Windows you'll have to login to with ``putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_. Connect to vagrant@127.0.01 at port 2222. User _and_ password are `vagrant`.

You are now logged in as the user vagrant in ``/home/vagrant``. We'll do all steps of the training as this user.

We pre-installed a fresh Plone for you in the folder ``/home/vagrant/Plone/zinstance`` You can run it now and access it from the browser. We will **not** use this Plone-instance in the training, so you can play around with it as much as you want.

Instead we use our own Plone-instance during the training. It is in ``/vagrant/buildout/``. Start it in foreground with ``./bin/instance fg``.

.. code-block:: bash

    vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/buildout
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/buildout$ ./bin/instance fg
    2014-05-20 16:56:54 INFO ZServer HTTP server started at Tue May 20 16:56:54 2014
            Hostname: 0.0.0.0
            Port: 8080
    2014-05-20 16:56:56 INFO Products.PloneFormGen gpg_subprocess initialized, using /usr/local/bin/gpg
    2014-05-20 16:57:02 INFO PloneFormGen Patching plone.app.portlets ColumnPortletManagerRenderer to not catch Retry exceptions
    2014-05-20 16:57:02 INFO Zope Ready to handle requests

Now the Zope-instance we're using is running. You can stop the running instance anytime using ``ctrl + c``.

You can now point your local browser at http://localhost:8080 and see the Plone that is running in vagrant. This works because Virtualbox forwards the port 8080 from the guest-system (the vagrant-Ubuntu) to the host-system (your normal operating-system). Now create a new Plone-Site by clicking "Create a new Plone-Site". The username and the password are both "admin" (Never do this on a real site!).

The Buildout for this Plone is in a shared folder, this means we run it in the vagrant-box from ``/vagrant/buildout`` but we can also access it in out own operating-system and use our favorite editor. You will find the directory ``buildout`` in the directory ``training`` that you created in the very beginning next to ``Vagrantfile`` and ``manifests``.

.. note::

    The database and the python-packages are **not accessible** in you own system since large files and you canot use symlinks in shared folders. The database lies in ``/home/vagrant/var``, the python-packages are in ``/home/vagrant/omelette``.

If you have any problems or questions please mail us at team@starzel.de


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

Then we create a virtual python environement using virtualenv. This is alway a good practice since that way we get a clean copy of our system-python, we can't break it by installing eggs that might collide with other eggs::

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

Then we checkout our tutorial code from http://github.com/starzel/training and build it.

.. code-block:: bash

    $ cd /vagrant
    $ git clone https://github.com/starzel/training.git buildout
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
