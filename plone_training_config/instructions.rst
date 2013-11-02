Installing Plone for the Training
=================================



To not waste too much time with installing and debugging the differences between systems we use a virtual machine (Ubuntu 12.04) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development-environment to everyone.

`Vagrant <http://www.vagrantup.com>`_ is a command-line wrapper for Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage virtual environments.

Keep in mind that you need a fast internet-connection during the process since you'll have to download a complete virtual machine (ubuntu) and several packages and updates.


Install VirtualBox
-------------------------

Vagrant depends on Oracle’s VirtualBox to create virtual environments. Here is a link directly to the download page: https://www.virtualbox.org/wiki/Downloads. We use VirtualBox  4.2.x.


Install and configure Vagrant
-----------------------------

Get the latest version from http://downloads.vagrantup.com for your operating system and install it.

Now your system has a command ``vagrant`` that you can run in the terminal.

First create a directory where you want to do the training in.

.. code-block:: bash

    $ mkdir training
    $ cd training

Download a clean virtual machine (Ubuntu 12.04 Precise Pangolin 32bit). It will be downloaded and made available to the vagrant-command as 'precise32'. It serves as a basis for your virtual machines and can be reused as often as you like:

.. code-block:: bash

    $ vagrant box add precise32 http://files.vagrantup.com/precise32.box

Setup Vagrant to automatically install the current guest-additions. You can choose to skip this step if you encounter any problems with it.

.. code-block:: bash

    $ vagrant plugin install vagrant-vbguest

Now either extract the the files from the attachmeht (if you read this as a mail) or download and extract http://www.starzel.de/plone-tutorial/plone_training_config.zip into your training directory. It should now hold the file "Vagrantfile" and the directories ``manifests/``  and ``puppet_modules/``

Start the VM that is configured in "Vagrantfile"

.. code-block:: bash

    $ vagrant up

This takes a very loooong time since it not only sets up the VM but also updates your VM, installs various packages needed for Plone-development and runs the installer for Plone 4.3.2.

More often than not this stops with the message *Skipping because of failed dependencies*.

More often than not this stops with the message:

.. code-block:: bash

    Skipping because of failed dependencies

If this happens or you have the feeling that something has gone wrong and the installation has not finished correctly for some reason you need to run try the following command to repeat the process. This will only repeat steps that have not finished correctly.

.. code-block:: bash

    $ vagrant provision

You can do this multiple times to fix problems, e.g. if your network-connection was down and steps could not finish because of this.

Once the provisioning-process is completed you can login to the now running virtual machine.

.. code-block:: bash

    $ vagrant ssh

If you use Windows you'll have to login via putty (Install putty and follow the instructions here: http://vagrantup.com/v1/docs/getting-started/ssh.html)

You are now logged in as the user vagrant in ``/home/vagrant``. We'll do all steps of the training as this user.

We installed a Plone 4.3.2 for you in the folder ``/home/vagrant/training/zinstance`` You can run it now and access it from the browser.

.. code-block:: bash

    $ cd training/zinstance
    $ ./bin/instance fg

You can now point your browser at http://localhost:8080 and see Plone. This works since the port 8080 is forwarded from the guest-system (the vagrant-Ubuntu) to the host-system (your normal operating-system). Now create a new Plone-Site by clicking "Create a new Plone-Site". The username and the password are both "admin" (Never do this on a real site!!!).

Do not get accustomized to this site, we will create a buildout based plone during the training. We only test now that the installation has finished.

If you have any problems or questions please mail us at team@starzel.de

.. warning::

    You can also work on your own machine with your own Python and Plone if you really want to but **please please please** make sure that you have a system that will work since we don't want you to loose valuable time learning Plone.


What Vagrant does
-----------------

.. note::

    These steps are automatically done by vagrant and puppet. They are only explained here if you want to know what goes on below the hood.

The first installation is done by Puppet, a tool to automatically manage servers (real and virtual). We won't get into Puppet since it is not that widely used. This is what we basically do if we did it by hand:

First we install some packages::

    $ sudo aptitude update --quiet --assume-yes
    $ sudo apt-get install python-dev python-virtualenv libjpeg62-dev libxslt1-dev git-core subversion zlib1g-dev libbz2-dev wget cURL elinks gettext

Then we create a virtual python environement using virtualenv. This is alway a good practice since that way we get a clean copy of our system-python, we can't break it by installing eggs that might collide with other eggs::

    $ virtualenv --no-site-packages py27

Then we download, unpack and install the unified installer of Plone::

    $ mkdir training
    $ mkdir tmp
    $ cd tmp
    $ wget https://launchpad.net/plone/4.3/4.3.2/+download/Plone-4.3.2-UnifiedInstaller.tgz
    $ tar xzf Plone-4.3.2-UnifiedInstaller.tgz
    $ cd Plone-4.3.2-UnifiedInstaller
    $ ./install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/training

The unified installer is an amazing tool that compiles it's own python, brings with it all the python-eggs we need and puts them in a buildout-cache. It then creates a buildout and makes Plone ready to run.

We will not actually use this Plone during the training. If you want to use it for your own experiments, you can find it in ``/home/vagrant/training/zinstance`` on the virtual machine.

Instead we will now create our own little buildout and only use the python and the eggs that were created when installing the unified installer.

Checkout our tutorial code from http://github.com/starzel/training.

.. code-block:: bash

    $ cd /vagrant/buildouts
    $ git clone https://github.com/starzel/training.git

In your training directory create another directory called 'plone'. Copy the contents from chapter3 of the tutorial code into the new directory.

.. code-block:: bash

    $ mkdir /vagrant/plone
    $ cd /vagrant/plone
    $ cp -R /vagrant/buildouts/chapter3/* .

Then enter the machine via ssh and start building.

.. code-block:: bash

    $ cd /vagrant/plone
    $ virtualenv .
    $ source bin/activate
    $ python bootstrap.py
    $ bin/buildout
    $ bin/instance fg

Now we have fresh buildout based zope site, ready to get a Plone site. Go to http://localhost:8080 and create a plone Site, only activate the Dexterity plugin.

You might wonder, why we use the unified installer. We use the unified installer to set up a cache of packages to download in a much shorter time. Without it, your first buildout on a fresh computer would take more than half an hour on a good internet connection.
