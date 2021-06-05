.. _instructions-label:

.. todo::

    * Skip Vagrant?
    * Update Vagrant instructions for Plone 5 with Volto


Installing Plone for the Training
=================================

.. sidebar:: Installation for the training

    .. contents:: Table of Contents
        :depth: 4


We need to install the backend **Plone** and the React-based frontend **Volto**.
This will create a folder structure like this:

.. code-block:: text

    training
    ├── backend
    └── frontend

In :file:`backend` we will install Plone and also add our custom Python code.
In :file:`frontend` we will install Volto and also add our custom React code.


.. _instructions-no-vagrant-label:

.. warning::

    If you try both methods below (with Vagrant and without), make sure you use different :file:`training` directories!

    The two installations do not coexist well.


Installing Plone without vagrant
--------------------------------


Installing the backend
++++++++++++++++++++++

.. warning::

    If you are new to running Plone on your computer you could skip this part and continue with :ref:`install-virtualbox`.

We encourage you to install and run Plone on your own machine, because you will have important benefits:

* You can use the editor you are used to.
* You can use *omelette* to have all the code of Plone at your fingertips.
* You do not have to switch between different operating systems during the training.

If you feel comfortable, please work on your own machine with your own Python.

**Please** make sure that you have a system that will work, since we don't want you to lose valuable time!

.. note::

    If you also want to follow the JavaScript training and install the JavaScript development tools,
    you need `NodeJS <https://nodejs.org/en/download/>`_ installed on your development computer.

.. note::

    Please make sure you have your system properly prepared and installed all necessary prerequisites.

The following instructions are based on Ubuntu and macOS, if you use a different operating system (OS), please adjust them to fit your OS.

On Ubuntu/Debian, you need to make sure you system is up-to-date:

.. code-block:: console

    sudo apt-get update
    sudo apt-get -y upgrade

Then, you need to install the following packages:

.. code-block:: console

    sudo apt-get install python3.8-dev python3.8-tk python3.8-venv build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
    sudo apt-get install libreadline-dev wv poppler-utils
    sudo apt-get install git

On macOS you at least need to install some dependencies with `Homebrew <https://brew.sh/>`_

.. code-block:: console

    brew install zlib git readline jpeg libpng libyaml

For more information or in case of problems see the `official installation instructions <https://docs.plone.org/manage/installing/installation.html>`_.

Set up Plone for the training like this if you use your own OS (Linux or macOS):

.. code-block:: console

    mkdir training
    cd training
    git clone https://github.com/collective/training_buildout.git backend
    cd backend

Until Mastering Plone 6 version is released you need to checkout the branch ``plone6``.

.. code-block:: console

    git checkout plone6

Then create a virtual environment with Python 3.7 in the folder :file:`backend` and install some requirements into it.

.. code-block:: console

    python3.8 -m venv .
    ./bin/pip install -r requirements.txt

Now you can run the buildout for the first time:

.. code-block:: console

    ./bin/buildout

This will take **a long time** (~10 minutes on the least powerful Linode) and will produce a lot of output because it downloads and configures more than 260 Python packages. Once it is done you can start your Plone instance with

.. code-block:: console

    ./bin/instance fg

The output should be similar to:

.. code-block:: console
    :emphasize-lines: 40

    pbauer@bullet:/workspace/training/backend$  ./bin/instance fg
    2019-09-05 20:11:03,708 WARNING [Init:89][MainThread] Class Products.CMFFormController.ControllerPythonScript.ControllerPythonScript has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    2019-09-05 20:11:03,715 WARNING [Init:89][MainThread] Class Products.CMFFormController.ControllerValidator.ControllerValidator has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    2019-09-05 20:11:03,776 WARNING [Products.PDBDebugMode:31][MainThread]

    ******************************************************************************

    Debug-Mode enabled!

    This will result in a pdb when a exception happens.
    Turn off debug mode or remove Products.PDBDebugMode to disable.

    See https://pypi.python.org/pypi/Products.PDBDebugMode

    ******************************************************************************

    2019-09-05 20:11:04,858 INFO    [chameleon.config:38][MainThread] directory cache: /Users/pbauer/workspace/training/backend/var/cache.
    2019-09-05 20:11:07,151 WARNING [plone.behavior:172][MainThread] Specifying 'for' in behavior 'Tiles' if no 'factory' is given has no effect and is superfluous.
    2019-09-05 20:11:08,353 WARNING [PrintingMailHost:30][MainThread] Hold on to your hats folks, I'm a-patchin'
    2019-09-05 20:11:08,353 WARNING [PrintingMailHost:124][MainThread]

    ******************************************************************************

    Monkey patching MailHosts to print e-mails to the terminal.

    This is instead of sending them.

    NO MAIL WILL BE SENT FROM ZOPE AT ALL!

    Turn off debug mode or remove Products.PrintingMailHost from the eggs
    or remove ENABLE_PRINTING_MAILHOST from the environment variables to
    return to normal e-mail sending.

    See https://pypi.python.org/pypi/Products.PrintingMailHost

    ******************************************************************************

    2019-09-05 20:11:08,390 INFO    [Zope:45][MainThread] Ready to handle requests
    Starting server in PID 30620.
    Serving on http://0.0.0.0:8080


If the output says ``Serving on http://0.0.0.0:8080`` then you are in business.

If you point your browser at http://localhost:8080 you see that Plone is running.

.. figure:: _static/instructions_plone_running.png
	:scale: 50 %
	:alt: Plone is running.

	A running plone instance.

There is no Plone site yet.
We will create one in the next chapter.

You can stop the running instance anytime using :kbd:`ctrl + c`.

.. warning::

    If there is an error message you should either try to fix it or use vagrant and continue in this chapter.

.. _instructions-install_frontend-label:

Installing the frontend
+++++++++++++++++++++++

You have two options:

    1. Create the frontend from scratch using the Volto generator.
    2. Use the existing Volto project for this training `volto-ploneconf <https://github.com/collective/volto-ploneconf.git>`_ with all the code for the training.

.. note::

    If you are completely new to node and companions, please see `Volto Documentation <https://docs.voltocms.com/getting-started/install/>`_ to find information about node, nvm, npx, yarn and the React thing.


Option 1: Frontend from scratch with Volto generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _instructions-install_frontend-prerequisites-label:


Install pre-requisites.

#.  Install ``nvm`` (Node Version Manager) to manage ``node`` versions.

    .. code-block:: bash

        # macOS
        brew install nvm

        #Linux
        apt-get install nvm

#.  Install node LTS (node version LTS: long time support)

    .. code-block:: bash

        nvm install --lts

#.  Install package manager ``yarn``.

    .. code-block:: bash

        npm install --global yarn


Create your Volto frontend project.

#.  Generate a project with yeoman

    .. code-block:: bash

        npm init yo @plone/volto

    | It will take a while to install all dependencies.
    | `yo` will ask questions. Respond to the first by entering your project name, the next by pressing :kbd:`Enter` and to the other two by now with ``false``.

    The output will look like this:

    .. code-block:: bash

        me@here training % npm init yo @plone/volto
        npx: installed 14 in 3.392s
        Getting latest Volto version
        Retrieving Volto's yarn.lock
        Using latest released Volto version: 10.4.1
        ? Project name frontend
        ? Project description A Volto-powered Plone frontend
        ? Would you like to add addons? false
        ? Would you like to add workspaces? false
           create frontend/package.json
           create frontend/yarn.lock
           create frontend/.eslintrc.js
           ...

#.  Start up the project **frontend** with

    .. code-block:: bash

        cd frontend
        yarn start

If successful, you get:

    🎭 Volto started at http://localhost:3000 🚀


Create a Plone site object **Plone** on http://localhost:8080

Point your browser to http://localhost:3000 and see that Plone is up and running.


You can stop the frontend anytime using :kbd:`ctrl + c`.


.. _volto-install-troubleshooting:

Troubleshooting
'''''''''''''''

See https://docs.voltocms.com/getting-started/install/#install-volto


Option 2. Start with existing training project ``volto-ploneconf`` with all code for the training
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install package manager ``yarn``.

    .. code-block:: bash

        npm install --global yarn

Get the finished code for the frontend from github and install:

.. code-block:: console

    git clone https://github.com/collective/volto-ploneconf.git frontend
    cd frontend
    yarn

Now you can start it with::

    $ yarn start

Create a Plone site object *Plone* on http://localhost:8080

Point your browser to http://localhost:3000 and see that Plone is up and running.

You can stop the frontend anytime using :kbd:`ctrl + c`.



.. _instructions-vagrant-label:

Installing Plone with Vagrant
-----------------------------

.. warning::

    This part is not yet updated to install the frontend Volto!

    Use a local installtion (see above) until that is done.


We use a virtual machine (Ubuntu 18.04) to run Plone during the training.

We rely on `Vagrant <https://www.vagrantup.com>`_ and `VirtualBox <https://www.virtualbox.org>`_ to give the same development environment to everyone.

`Vagrant <https://www.vagrantup.com>`_ is a tool for building complete development environments.

We use it together with Oracle’s `VirtualBox <https://www.virtualbox.org>`_ to create and manage a virtual environment.

.. _install-virtualbox:

Install VirtualBox
++++++++++++++++++

Vagrant uses Oracle’s VirtualBox to create virtual environments.

Here is a link directly to the download page: https://www.virtualbox.org/wiki/Downloads.

We use VirtualBox 6.0.x


.. _instructions-configure-vagrant-label:

Install and configure Vagrant
+++++++++++++++++++++++++++++

Get the latest version from https://www.vagrantup.com/downloads.html for your operating system and install it.

Now your system has a command :command:`vagrant` that you can run in the terminal.

First, create a directory in which you want to do the training.

.. warning::

    If you already have a :file:`training` directory because you followed the **Installing Plone without vagrant** instructions above,
    you should either delete it, rename it, or use a different name below.

.. code-block:: console

    mkdir training
    cd training

Setup Vagrant to automatically install the current guest additions.
You can choose to skip this step if you encounter any problems with it.

.. code-block:: console

    vagrant plugin install vagrant-vbguest

Now download :download:`plone_training_config.zip <../_static/plone_training_config.zip>` and copy its contents into your training directory.

.. code-block:: console

    wget https://github.com/plone/training/raw/master/_static/plone_training_config.zip
    unzip plone_training_config.zip

The training directory should now hold the file :file:`Vagrantfile` and the directory :file:`manifests` which again contains several files.

Now start setting up the virtual machine (VM) that is configured in :file:`Vagrantfile`:

.. code-block:: console

    vagrant up

This takes a **veeeeery loooong time** (between 10 minutes and 1h depending on your Internet connection and system speed) since it does all the following steps:

* downloads a virtual machine (Official Ubuntu Server 18.04 LTS, also called "Bionic Beaver")
* sets up the VM
* updates the VM
* installs various system-packages needed for Plone development
* clones the training buildout into /vagrant/buildout
* builds Plone annd installs all dependencies

.. note::

    Sometimes this stops with the message:

    .. code-block:: console

        Skipping because of failed dependencies

If this happens or you have the feeling that something has gone wrong and the installation has not finished correctly for some reason
you need to run the following command to repeat the process.

This will only repeat steps that have not finished correctly.

.. code-block:: console

   vagrant provision

You can do this multiple times to fix problems, e.g. if your network connection was down and steps could not finish because of this.

.. note::

    If while bringing vagrant up you get an error similar to:

    .. code-block:: console

        ssh_exchange_identification: read: Connection reset by peer

The configuration may have stalled out because your computer's BIOS requires virtualization to be enabled.
Check with your computer's manufacturer on how to properly enable virtualization.

See: https://teamtreehouse.com/community/vagrant-ssh-sshexchangeidentification-read-connection-reset-by-peer

Once Vagrant finishes the provisioning process, you can login to the now running virtual machine.

.. code-block:: console

    vagrant ssh

.. note::

    If you use Windows you'll have to login with `putty <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.
    Connect to vagrant@127.0.01 at port 2222. User **and** password are ``vagrant``.

You are now logged in as the user vagrant in :file:`/home/vagrant`.

We'll do all steps of the training as this user.

Instead we use our own Plone instance during the training.
It is in :file:`/vagrant/buildout/`. Start it in foreground with :command:`./bin/instance fg`.

.. code-block:: console

    vagrant@training:~$ cd /vagrant/buildout/
    vagrant@training:/vagrant/buildout$ ./bin/instance fg
    2019-03-07 10:38:17,666 WARNI [Init:88][MainThread] Class Products.CMFFormController.ControllerPythonScript.ControllerPythonScript has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    2019-03-07 10:38:17,670 WARNI [Init:88][MainThread] Class Products.CMFFormController.ControllerValidator.ControllerValidator has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    2019-03-07 10:38:21,160 WARNI [plone.behavior:172][MainThread] Specifying 'for' in behavior 'Tiles' if no 'factory' is given has no effect and is superfluous.
    2019-03-07 10:38:22,473 WARNI [PrintingMailHost:30][MainThread] Hold on to your hats folks, I'm a-patchin'
    2019-03-07 10:38:22,474 WARNI [PrintingMailHost:124][MainThread]

    ******************************************************************************

    Monkey patching MailHosts to print e-mails to the terminal.

    This is instead of sending them.

    NO MAIL WILL BE SENT FROM ZOPE AT ALL!

    Turn off debug mode or remove Products.PrintingMailHost from the eggs
    or remove ENABLE_PRINTING_MAILHOST from the environment variables to
    return to normal e-mail sending.

    See https://pypi.python.org/pypi/Products.PrintingMailHost

    ******************************************************************************

    2019-03-07 10:38:22,510 INFO  [Zope:44][MainThread] Ready to handle requests
    Starting server in PID 25230.
    Serving on http://0.0.0.0:8080

.. note::

    In rare cases when you are using macOS with an UTF-8 character set starting Plone might fail with the following error:

    .. code-block:: text

       ValueError: unknown locale: UTF-8

In that case you have to put the localized keyboard and language settings in the .bash_profile
of the vagrant user to your locale (like ``en_US.UTF-8`` or ``de_DE.UTF-8``)

.. code-block:: bash

    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8

Now the Zope instance we're using is running.
You can stop the running instance anytime using :kbd:`ctrl + c`.

If it doesn't, don't worry, your shell isn't blocked.

Type :kbd:`reset` (even if you can't see the prompt) and press RETURN, and it should become visible again.

If you point your local browser at http://localhost:8080 you see that Plone is running in Vagrant.

This works because VirtualBox forwards the port 8080 from the guest system (the vagrant Ubuntu) to the host system (your normal operating system).

There is no Plone site yet - we will create one in chapter 6.

The Buildout for this Plone is in a shared folder.
This means we run it in the vagrant box from :file:`/vagrant/buildout` but we can also access it in our own operating system and use our favorite editor.

You will find the directory :file:`buildout` in the directory :file:`training` that you created in the beginning
next to :file:`Vagrantfile` and :file:`manifests`.

.. note::

    The database and the python packages are not accessible in your own system since large files cannot make use of symlinks in shared folders.
    The database lies in ``/home/vagrant/var``, the python packages are in ``/home/vagrant/packages``.

If you have any problems or questions please mail us at team@starzel.de or create a ticket at https://github.com/plone/training/issues.


.. _instructions-vagrant-does-label:

What Vagrant does
+++++++++++++++++

Installation is done automatically by vagrant and puppet.
If you want to know which steps are actually done please see the chapter :doc:`what_vagrant_does`.

.. _instructions-vagrant-care-handling-label:

.. note::

    **Vagrant Care and Handling**

    Keep in mind the following recommendations for using your Vagrant VirtualBoxes:

    * Use the :command:`vagrant suspend` or :command:`vagrant halt` commands to put the VirtualBox to "sleep" or to "power it off" before attempting to start another Plone instance anywhere else on your machine, if it uses the same port.  That's because vagrant "reserves" port 8080, and even if you stopped Plone in vagrant, that port is still in use by the guest OS.
    * If you are done with a vagrant box, and want to delete it, always remember to run :command:`vagrant destroy` on it before actually deleting the directory containing it.  Otherwise you'll leave its "ghost" in the list of boxes managed by vagrant and possibly taking up disk space on your machine.
    * See :command:`vagrant help` for all available commands, including :command:`suspend`, :command:`halt`, :command:`destroy`, :command:`up`, :command:`ssh` and :command:`resume`.
