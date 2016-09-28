.. _instructions-label:

Installing Plone for the Training
=================================

Keep in mind that you need a fast internet connection during installation since you'll have to download a lot of data!


.. _instructions-no-vagrant-label:

.. warning::

    If you feel the desire to try out both methods below (with Vagrant and without), make sure you use different ``training`` directories!  The two installations do not coexist well.


Installing Plone without vagrant
--------------------------------

.. warning::

    If you are **not** used to running Plone on your laptop skip this part and continue with :ref:`install-virtualbox`.

If you **are** experienced with running Plone on your own laptop, we encourage you to do so because you will have certain benefits:

* You can use the editor you are used to.
* You can use *omelette* to have all the code of Plone at your fingertips.
* You do not have to switch between different operating systems during the training.

If you feel comfortable, please work on your own machine with your own Python. But **please** make sure that you have a system that will work, since we don't want you to lose valuable time!

.. note::

    If you also want to follow the JavaScript training and install the JavaScript development tools, you need `NodeJS <https://nodejs.org/en/download/>`_ installed on your development computer.


.. note::

    Please make sure you have your system properly prepared and installed all necessary prerequisites. For example, on Ubuntu/Debian, you need to install the following::

        sudo apt-get install python-setuptools python-virtualenv python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
        sudo apt-get install libreadline-dev wv poppler-utils
        sudo apt-get install git

    For more information or in case of problems see the `official installation instructions <http://docs.plone.org/manage/installing/installation.html>`_.



Set up Plone for the training like this if you use your own OS (Linux or Mac):

.. code-block:: bash

    $ mkdir training
    $ cd training
    $ git clone https://github.com/collective/training_buildout.git buildout
    $ cd buildout
    $ virtualenv-2.7 py27

Now you can run the buildout for the first time:

.. code-block:: bash

    $ ./py27/bin/python bootstrap.py
    $ ./bin/buildout

This will take some time and produce a lot of output because it downloads and configures Plone. Once it is done you can start your instance with

.. code-block:: bash

    $ ./bin/instance fg

The output should be similar to:

.. code-block:: html
    :emphasize-lines: 9

    2015-09-24 15:51:02 INFO ZServer HTTP server started at Thu Sep 24 15:51:02 2015
            Hostname: 0.0.0.0
            Port: 8080
    2015-09-24 15:51:05 WARNING PrintingMailHost Hold on to your hats folks, I'm a-patchin'
    2015-09-24 15:51:05 WARNING PrintingMailHost

    ******************************************************************************

    Monkey patching MailHosts to print e-mails to the terminal.

    This is instead of sending them.

    NO MAIL WILL BE SENT FROM ZOPE AT ALL!

    Turn off debug mode or remove Products.PrintingMailHost from the eggs
    or remove ENABLE_PRINTING_MAILHOST from the environment variables to
    return to normal e-mail sending.

    See https://pypi.python.org/pypi/Products.PrintingMailHost

    ******************************************************************************

    2015-09-24 15:51:05 INFO ZODB.blob (54391) Blob directory `.../buildout/var/blobstorage` is unused and has no layout marker set. Selected `bushy` layout.
    2015-09-24 15:51:05 INFO ZODB.blob (54391) Blob temporary directory '.../buildout/var/blobstorage/tmp' does not exist. Created new directory.
    .../.buildout/eggs/plone.app.multilingual-3.0.11-py2.7.egg/plone/app/multilingual/browser/migrator.py:11: DeprecationWarning: LanguageRootFolder: LanguageRootFolders should be migrate to DexterityContainers
      from plone.app.multilingual.content.lrf import LanguageRootFolder
    2015-09-24 15:51:09 INFO Plone OpenID system packages not installed, OpenID support not available
    2015-09-24 15:51:11 INFO PloneFormGen Patching plone.app.portlets ColumnPortletManagerRenderer to not catch Retry exceptions
    2015-09-24 15:51:11 INFO Zope Ready to handle requests

If the output says ``INFO Zope Ready to handle requests`` then you are in business.

If you point your browser at http://localhost:8080 you see that Plone is running. Now create a new Plone site by clicking "Create a new Plone site". The username and the password are both "admin" (Never do this on a real site!).

Now you have a working Plone site up and running and can continue with the next chapter.  You can stop the running instance anytime using ``ctrl + c``.

.. warning::

    If there is an error message you should either try to fix it or use vagrant and continue in this chapter.


.. _instructions-vagrant-label:

Installing Plone with vagrant
-----------------------------

In order not to waste too much time with installing and debugging the differences between systems, we use a virtual machine (Ubuntu 14.04) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development environment to everyone.

`Vagrant <https://www.vagrantup.com>`_ is a tool for building complete development environments. We use it together with Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage a virtual environment.

.. _install-virtualbox:

Install VirtualBox
++++++++++++++++++

Vagrant uses Oracle’s VirtualBox to create virtual environments. Here is a link directly to the download page: https://www.virtualbox.org/wiki/Downloads. We use VirtualBox 4.3.x


.. _instructions-configure-vagrant-label:

Install and configure Vagrant
+++++++++++++++++++++++++++++

Get the latest version from https://www.vagrantup.com/downloads.html for your operating system and install it.

.. note::

    In Windows there is a bug in the recent version of Vagrant. Here are the instructions for how to work around the warning ``Vagrant could not detect VirtualBox! Make sure VirtualBox is properly installed``.

Now your system has a command ``vagrant`` that you can run in the terminal.

.. note::

    You don't need to install ``NodeJS`` as mentioned in the previous section. Our Vagrant configuration already does that for you.


First, create a directory in which you want to do the training.

.. warning::

    If you already have a ``training`` directory because you followed the **Installing Plone without vagrant** instructions above, you should either delete it, rename it, or use a different name below.

.. code-block:: bash

    $ mkdir training
    $ cd training

Setup Vagrant to automatically install the current guest additions. You can choose to skip this step if you encounter any problems with it.

.. code-block:: bash

    $ vagrant plugin install vagrant-vbguest

Now download :download:`plone_training_config.zip <../_static/plone_training_config.zip>` and copy its contents into your training directory.

.. code-block:: bash

    $ wget https://raw.githubusercontent.com/plone/training/master/_static/plone_training_config.zip
    $ unzip plone_training_config.zip

The training directory should now hold the file ``Vagrantfile`` and the directory ``manifests`` which again contains several files.

Now start setting up the VM that is configured in ``Vagrantfile``:

.. code-block:: bash

    $ vagrant up

This takes a **veeeeery loooong time** (between 10 minutes and 1h depending on your internet connection and system speed) since it does all the following steps:

* downloads a virtual machine (Official Ubuntu Server 14.04 LTS, also called "Trusty Tahr")
* sets up the VM
* updates the VM
* installs various system-packages needed for Plone development
* downloads and unpacks the buildout-cache to get all the eggs for Plone
* clones the training buildout into /vagrant/buildout
* builds Plone using the eggs from the buildout-cache

.. note::

    Sometimes this stops with the message:

    .. code-block:: bash

        Skipping because of failed dependencies

    If this happens or you have the feeling that something has gone wrong and the installation has not finished correctly for some reason you need to run the following command to repeat the process. This will only repeat steps that have not finished correctly.

    .. code-block:: bash

        $ vagrant provision

    You can do this multiple times to fix problems, e.g. if your network connection was down and steps could not finish because of this.

.. note::

    If while bringing vagrant up you get an error similar to:

    .. code-block:: bash

        ssh_exchange_identification: read: Connection reset by peer

    The configuration may have stalled out because your computer's BIOS requires virtualization to be enabled. Check with your computer's manufacturer on how to properly enable virtualization.  See: https://teamtreehouse.com/community/vagrant-ssh-sshexchangeidentification-read-connection-reset-by-peer

Once Vagrant finishes the provisioning process, you can login to the now running virtual machine.

.. code-block:: bash

    $ vagrant ssh

.. note::

    If you use Windows you'll have to login with `putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_. Connect to vagrant@127.0.01 at port 2222. User **and** password are ``vagrant``.

You are now logged in as the user vagrant in ``/home/vagrant``. We'll do all steps of the training as this user.

Instead we use our own Plone instance during the training. It is in ``/vagrant/buildout/``. Start it in foreground with ``./bin/instance fg``.

.. code-block:: bash

    vagrant@training:~$ cd /vagrant/buildout
    vagrant@training:/vagrant/buildout$ ./bin/instance fg
    2015-09-24 15:51:02 INFO ZServer HTTP server started at Thu Sep 24 15:51:02 2015
            Hostname: 0.0.0.0
            Port: 8080
    2015-09-24 15:51:05 WARNING PrintingMailHost Hold on to your hats folks, I'm a-patchin'
    2015-09-24 15:51:05 WARNING PrintingMailHost

    ******************************************************************************

    Monkey patching MailHosts to print e-mails to the terminal.

    This is instead of sending them.

    NO MAIL WILL BE SENT FROM ZOPE AT ALL!

    Turn off debug mode or remove Products.PrintingMailHost from the eggs
    or remove ENABLE_PRINTING_MAILHOST from the environment variables to
    return to normal e-mail sending.

    See https://pypi.python.org/pypi/Products.PrintingMailHost

    ******************************************************************************

    2015-09-24 15:51:05 INFO ZODB.blob (54391) Blob directory `.../buildout/var/blobstorage` is unused and has no layout marker set. Selected `bushy` layout.
    2015-09-24 15:51:05 INFO ZODB.blob (54391) Blob temporary directory '.../buildout/var/blobstorage/tmp' does not exist. Created new directory.
    .../.buildout/eggs/plone.app.multilingual-3.0.11-py2.7.egg/plone/app/multilingual/browser/migrator.py:11: DeprecationWarning: LanguageRootFolder: LanguageRootFolders should be migrate to DexterityContainers
      from plone.app.multilingual.content.lrf import LanguageRootFolder
    2015-09-24 15:51:09 INFO Plone OpenID system packages not installed, OpenID support not available
    2015-09-24 15:51:11 INFO PloneFormGen Patching plone.app.portlets ColumnPortletManagerRenderer to not catch Retry exceptions
    2015-09-24 15:51:11 INFO Zope Ready to handle requests

.. note::

    In rare cases when you are using OSX with an UTF-8 character set starting Plone might fail with the following error:

    .. code-block:: text

       ValueError: unknown locale: UTF-8

    In that case you have to put the localized keyboard and language settings in the .bash_profile of the vagrant user to your locale (like ``en_US.UTF-8`` or ``de_DE.UTF-8``)

    .. code-block:: bash

        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8

Now the Zope instance we're using is running. You can stop the running instance anytime using ``ctrl + c``.

If it doesn't, don't worry, your shell isn't blocked. Type ``reset`` (even if you can't see the prompt) and press RETURN, and it should become visible again.

If you point your local browser at http://localhost:8080 you see that Plone is running in vagrant. This works because VirtualBox forwards the port 8080 from the guest system (the vagrant Ubuntu) to the host system (your normal operating system). Now create a new Plone site by clicking "Create a new Plone site". The username and the password are both "admin" (Never do this on a real site!).

The Buildout for this Plone is in a shared folder.  This means we run it in the vagrant box from ``/vagrant/buildout`` but we can also access it in our own operating system and use our favorite editor. You will find the directory ``buildout`` in the directory ``training`` that you created in the very beginning next to ``Vagrantfile`` and ``manifests``.

.. note::

    The database and the python packages are not accessible in your own system since large files cannot make use of symlinks in shared folders. The database lies in ``/home/vagrant/var``, the python packages are in ``/home/vagrant/packages``.

If you have any problems or questions please mail us at team@starzel.de or create a ticket at https://github.com/plone/training/issues.


.. _instructions-vagrant-does-label:

What Vagrant does
+++++++++++++++++

Installation is done automatically by vagrant and puppet. If you want to know which steps are actually done please see the chapter :doc:`what_vagrant_does`.

.. _instructions-vagrant-care-handling-label:

.. note::

    **Vagrant Care and Handling**

    Keep in mind the following recommendations for using your Vagrant virtualboxes:

    * Use the ``vagrant suspend`` or ``vagrant halt`` commands to put the virtualbox to "sleep" or to "power it off" before attempting to start another Plone instance anywhere else on your machine, if it uses the same port.  That's because vagrant "reserves" port 8080, and even if you stopped Plone in vagrant, that port is still in use by the guest OS.
    * If you are done with a vagrant box, and want to delete it, always remember to run ``vagrant destroy`` on it before actually deleting the directory containing it.  Otherwise you'll leave its "ghost" in the list of boxes managed by vagrant and possibly taking up disk space on your machine.
    * See ``vagrant help`` for all available commands, including ``suspend``, ``halt``, ``destroy``, ``up``, ``ssh`` and ``resume``.
