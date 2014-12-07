Installing Plone for the Training
=================================


To not waste too much time with installing and debugging the differences between systems we use a virtual machine (Ubuntu 14.04) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development-environment to everyone.

`Vagrant <http://www.vagrantup.com>`_ is a tool for building complete development environments. We use it together with Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage a virtual environment.

Keep in mind that you need a fast internet-connection during the process since you'll have to download a complete virtual machine (ubuntu) and several packages and updates.


Installing Plone without vagrant
--------------------------------

.. warning::

    If you are **not** used to running Plone on your laptop skip this part and continue with :ref:`install-virtualbox`.

If you **are** experienced with running Plone on your own laptop we encourage you to do so because you will have certain benefits:

* You can use the editor you are used to.
* You can use omelette to have all the code of Plone at your fingertips.
* You do not have to switch between different operating-system during the training.

If you feel comfortable please work on your own machine with your own Python but ** please ** make sure that you have a system that will work since we don't want you to lose valuable time.

You will need to make a small change to the buildout we use during the training.

Set up Plone for the training like this if you use your own OS (Linux or Mac):

.. code-block:: bash

    $ mkdir training
    $ cd training
    $ git clone https://github.com/collective/training_buildout.git buildout
    $ cd buildout
    $ virtualenv-2.7 py27

Now you need to make a small change to the buildout. Open the file ``buildout.cfg`` in an editor and add a ``#`` at the beginning of line 25 where it says ``buildout_dir = /home/vagrant``. Then remove the ``#`` at the next line. It should now read:

.. code-block:: ini

    buildout_dir = ${buildout:directory}

Now you can run the buildout for the first time:

.. code-block:: bash

    $ ./py27/bin/python bootstrap.py
    $ ./bin/buildout

This will take some time and produce a lot of output because it downloads and configures Plone. Once it is done you can start you instance with

.. code-block:: bash

    $ ./bin/instance fg

If the output should be simliar to::

    2014-10-06 15:11:26 INFO ZServer HTTP server started at Mon Oct  6 15:11:26 2014
        Hostname: 0.0.0.0
        Port: 8080
    2014-10-06 15:11:29 INFO Products.PloneFormGen gpg_subprocess initialized, using /usr/local/bin/gpg
    2014-10-06 15:11:29 INFO ZODB.blob (14015) Blob directory `/Users/philip/workspace/training/buildout/var/blobstorage` is unused and has no layout marker set. Selected `bushy` layout.
    2014-10-06 15:11:29 INFO ZODB.blob (14015) Blob temporary directory '/Users/philip/workspace/training/buildout/var/blobstorage/tmp' does not exist. Created new directory.
    2014-10-06 15:11:37 INFO PloneFormGen Patching plone.app.portlets ColumnPortletManagerRenderer to not catch Retry exceptions
    2014-10-06 15:11:37 INFO Zope Ready to handle requests

It the output says ``INFO Zope Ready to handle requests`` then you are up and running and can continue with the next chapter.

.. warning::

    If there is an error-message you should either try to fix it or use vagrant and continue in this chapter.


.. _install-virtualbox:

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

Now either get the attached zip-file (if you read this as a mail) or download it from

:download:`http://plone-training.readthedocs.org/en/latest/_downloads/plone_training_config.zip <../plone_training_config.zip>`.

and copy its contents into your training directory.

.. code-block:: bash

    $ wget http://plone-training.readthedocs.org/en/latest/_downloads/plone_training_config.zip
    $ unzip plone_training_config.zip

The training-directory should now hold the file ``Vagrantfile`` and the directory ``manifests`` which again contains several files.

Now start setting up the VM that is configured in ``Vagrantfile``:

.. code-block:: bash

    $ vagrant up

This takes a **veeeeery loooong time** since it does all the following steps:

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

    If you use Windows you'll have to login with `putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_. Connect to vagrant@127.0.01 at port 2222. User **and** password are ``vagrant``.

You are now logged in as the user vagrant in ``/home/vagrant``. We'll do all steps of the training as this user.

We pre-installed a fresh Plone for you in the folder ``/home/vagrant/Plone/zinstance`` You can run it now and access it from the browser. We will **not** use this Plone-instance in the training, so you can play around with it as much as you want.

Instead we use our own Plone-instance during the training. It is in ``/vagrant/buildout/``. Start it in foreground with ``./bin/instance fg``.

.. code-block:: bash

    vagrant@training:~$ cd /vagrant/buildout
    vagrant@training:/vagrant/buildout$ ./bin/instance fg
    2014-05-20 16:56:54 INFO ZServer HTTP server started at Tue May 20 16:56:54 2014
            Hostname: 0.0.0.0
            Port: 8080
    2014-05-20 16:56:56 INFO Products.PloneFormGen gpg_subprocess initialized, using /usr/local/bin/gpg
    2014-05-20 16:57:02 INFO PloneFormGen Patching plone.app.portlets ColumnPortletManagerRenderer to not catch Retry exceptions
    2014-05-20 16:57:02 INFO Zope Ready to handle requests

.. note::

    In rare cases when you are using OSX with an UTF-8 character set starting Plone might fail with following error:

    .. code-block::

        ValueError: unknown locale: UTF-8

    In that case you have to put the localized keyboard and language settings in the .bash_profile of the vagrant user.

    .. code-block:: bash

        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8

Now the Zope-instance we're using is running. You can stop the running instance anytime using ``ctrl + c``.

If it doesn't, don't worry, your shell isn't blocked. Type reset (even if you can't see the prompt) and press RETURN, and it should become visible again.

If you point your local browser at http://localhost:8080 you see that Plone is running in vagrant. This works because Virtualbox forwards the port 8080 from the guest-system (the vagrant-Ubuntu) to the host-system (your normal operating-system). Now create a new Plone site by clicking "Create a new Plone site". The username and the password are both "admin" (Never do this on a real site!).

The Buildout for this Plone is in a shared folder, this means we run it in the vagrant-box from ``/vagrant/buildout`` but we can also access it in out own operating-system and use our favorite editor. You will find the directory ``buildout`` in the directory ``training`` that you created in the very beginning next to ``Vagrantfile`` and ``manifests``.

.. note::

    The database and the python-packages are not accessible in you own system since large files cannot make use of symlinks in shared folders. The database lies in ``/home/vagrant/var``, the python-packages are in ``/home/vagrant/packages``.

If you have any problems or questions please mail us at team@starzel.de or create a ticket at https://github.com/plone/training/issues.


What Vagrant does
-----------------

Installation is done automatically by vagrant and puppet. If you want to know which steps are actually done please see the chapter :doc:`what_vagrant_does`.
