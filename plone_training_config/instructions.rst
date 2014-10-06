Installing Plone for the Training
=================================



To not waste too much time with installing and debugging the differences between systems we use a virtual machine (Ubuntu 14.04) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development-environment to everyone.

`Vagrant <http://www.vagrantup.com>`_ is a tool for building complete development environments. We use it together with Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage a virtual environment.

Keep in mind that you need a fast internet-connection during the process since you'll have to download a complete virtual machine (ubuntu) and several packages and updates.

.. warning::

    We recommend using a virtual machine for the training if you are not used to running Plone on your laptop.

    You can also work on your own machine with your own Python if you want to but ** please ** make sure that you have a system that will work since we don't want you to lose valuable time.

    If you want to use your own system use the Buildout at https://github.com/starzel/training_without_vagrant.git

    Set up Plone for the training like this if you don't want to use a VM:

    .. code-block:: bash

        $ mkdir training
        $ cd training
        $ git clone https://github.com/starzel/training_without_vagrant.git buildout
        $ cd buildout
        $ virtualenv-2.7 py27
        $ ./py27/bin/python bootstrap.py
        $ ./bin/buildout

Install VirtualBox
------------------

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

Now either get the attached zip-file (if you read this as a mail) or download it from  :download:`http://plone-training.readthedocs.org/en/latest/_downloads/plone_training_config.zip <../plone_training_config.zip>`.
 and copy its contents into your training directory. It should now hold the file "Vagrantfile" and the directory ``manifests``.

.. code-block:: bash
    $ wget http://plone-training.readthedocs.org/en/latest/_downloads/plone_training_config.zip
    $ unzip plone_training_config.zip

Now start setting up the VM that is configured in "Vagrantfile"

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

    If this happens or you have the feeling that something has gone wrong and the installation has not finished correctly for some reason you need to run try the following command to repeat the process. This will only repeat steps that have not finished correctly.

    .. code-block:: bash

        $ vagrant provision

    You can do this multiple times to fix problems, e.g. if your network-connection was down and steps could not finish because of this.

Once Vagrant finishes the provisioning-process, you can login to the now running virtual machine.

.. code-block:: bash

    $ vagrant ssh

.. note::

    If you use Windows you'll have to login with `putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_. Connect to vagrant@127.0.01 at port 2222. User _and_ password are `vagrant`.

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

If you point your local browser at http://localhost:8080 you see that Plone is running in vagrant. This works because Virtualbox forwards the port 8080 from the guest-system (the vagrant-Ubuntu) to the host-system (your normal operating-system). Now create a new Plone-Site by clicking "Create a new Plone-Site". The username and the password are both "admin" (Never do this on a real site!).

The Buildout for this Plone is in a shared folder, this means we run it in the vagrant-box from ``/vagrant/buildout`` but we can also access it in out own operating-system and use our favorite editor. You will find the directory ``buildout`` in the directory ``training`` that you created in the very beginning next to ``Vagrantfile`` and ``manifests``.

.. note::

    The database and the python-packages are not accessible in you own system since large files cannot make use of symlinks in shared folders. The database lies in ``/home/vagrant/var``, the python-packages are in ``/home/vagrant/omelette``.

If you have any problems or questions please mail us at team@starzel.de or create a ticket at https://github.com/plone/training/issues.


What Vagrant does
-----------------

Installation is done automatically by vagrant and puppet. If you want to know which steps are actually done please see the chapter :doc:`what_vagrant_does`.
