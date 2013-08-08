2. Installation & Setup (60 Min) (Philip)
=========================================


Installation
------------

Plone 4.2 requires a working Python 2.7 and several other system-tools that not every OS provides. Therefore the installation of Plone is differen on every system. Here are some ways that python can can be used:

* use a Python that comes pre-installed in your operating-system (most Linuxes and Mac OS have one)
* use the python-buildout (https://github.com/collective/buildout.python)
* building Linux-packages
* homebrew (Mac OS X)
* PyWin32 (Windows)

MacOS 10.8 and Ubuntu 12.4 come with a working default Python 2.7 built in. These are the lucky ones. But to run a older Plone-version you need Python 2.4 and that's not always easy to install.

Most developers usually use their primary system to develop Plone. Philip has MacOS, therefore he uses the python-buildout (https://github.com/collective/buildout.python) to compile all neccessary versions of python and homebrew (http://mxcl.github.com/homebrew/) for some linux-tools. Patrick uses ubuntu. Some people use the python that comes with Plone's unified installer. Alan Runyan (one of Plone's founders) uses Windows. We have no idea how he can live with that but he seems to manage perfectly well.

Plone offers some options for being installed:

* unified installers for all 'nix (including MacOS)
* one-click installers for Windows and Mac
* very old package for debian (don't use them!)
* install with your own buildout

During the tutorial we'll use Options 1 and 4 to install and run Plone. We'll first use the unified installer and the default Plone-configuration (called buildout) that comes with it. Later we'll create our own buildout and extend it as we wish.

Read more about instaling Plone: https://plone.org/documentation/manual/installing-plone and http://developer.plone.org/getstarted/installation.HTML


Hosting your Website
--------------------

If you want to host a real-live Plone-Site yourself then running it from your laptop is not an viable option. A good way to get to know Plone is http://ploud.com where you can host one real Plone-Site for free.

You can host Plone...

* with one of many hosting-providers (http://plone.org/support/hosting-providers)
* on a virtual private server
* on dedicated servers
* in the cloud (e.g. using Amazon EC2)

Note that you can't use a $5/month hosting provider because they are usually specialize on LAMP-setups (Linux, Apache, MySQL, php) and usually don't meet the minimum requirements for Plone.

Read more about where to host Plone: http://plone.org/documentation/faq/where-can-i-host-my-plone-site


Installing Plone for the Training
---------------------------------

To not waste too much time with installing and debugging the differences between systems we use a virtual machine (ubuntu 12.4) to run Plone during the training. We rely on Vagrant and VirtualBox to give the same development-environment to everyone.

Vagrant (http://www.vagrantup.com) is a command-line wrapper for Oracle’s VirtualBox (https://www.virtualbox.org) to create and manage virtual environments.

Keep in mind that you need a fast internet-connection during the while process since you'll have to download a complete virtual machine (ubuntu) and several packages and updates.


Install VirtualBox
------------------

Vagrant depends on Oracle’s VirtualBox to create virtual environments. Here is a link directly to the download page: https://www.virtualbox.org/wiki/Downloads. We use VirtualBox  4.2.x.


Install and configure Vagrant
-----------------------------

Get the latest version from http://downloads.vagrantup.com for your operating system and install it.

Now your system has a command 'vagrant' that you can run in the terminal.

First create a directory where you want to to the training in::

    $ mkdir training
    $ cd training

Download a clean virtual machine (Ubuntu 12.04 Precise Pangolin 32bit). It will be downloaded and made available to the vagrant-command as 'precise32'. It serves as a basis for your virtual machines and can be reused as often as you like.::

    $ vagrant box add precise32 http://files.vagrantup.com/precise32.box

Setup Vagrant to automatically install the current guest-additions. You can choose to skip this step if you encounter any problems with it.::

    $ vagrant gem install vagrant-vbguest

Now copy the files from http://www.starzel.de/plone-tutorial/plone_training_config.zip into your training directory. It should now hold the file "Vagrantfile" and the directories "manifests/" and "puppet_modules/"::

Start the VM that is configured in "Vagrantfile"::

    $ vagrant up

This takes a very loooong time since it not only sets up the MV but also updates your VM, installs various packages needed for plone-development and runs the installer for Plone 4.2.1.

If you have the feeling that something has gone wrong and the installation has not finished correctly for some reason try the following command to repeat the process. This will only repeat steps that have not finished correctly::

    $ vagrant provision

You can try this multiple times to fix problems, e.g. if your network-connection was down and thus steps could not finish.

Once the provisioning-process is completed you can login to the now running virtual machine::

    $ vagnant ssh

If you use Windows you'll have to login via putty (Install putty and follow the instructions here: http://vagrantup.com/v1/docs/getting-started/ssh.HTML)

You are now logged in as the user vagrant in /home/vagrant. We'll do all steps of the training as this user.

We installed a Plone 4.2.1 for you in the folder /home/vagrant/training/zinstance. You can run it now and access it from the browser.::

    $ cd training/zinstance
    $ ./bin/instance fg

You can now point your browser at http://localhost:8080 and see Plone. This works since the port 8080 is forwarded from the guest-system (the vagrant-ubuntu) to the host-system (your normal operating-system). Now create a new Plone-Site by clicking "Create a new Plone-Site". The username and the password are both "admin" (Never do this on a real site!!!).

If you have any problems or questions please mail us at team@starzel.de

You can also work on your own machine with your own python and Plone if you really want to but please-please-please make sure that you have a system that will work since we don't want to loose any time with installing.


What vagrant does
-----------------

*These steps are automatically done by vagrant and puppet. They are only explained here if you want to know what goes on below the hood.*

The first installation is done by Puppet, a tool to automatically manage servers (real and virtual). We won't get into it Puppet since it's not that widely used. This is what we basically do if we did it by hand:

First we install some packages::

    $ sudo aptitude update --quiet --assume-yes
    $ sudo apt-get install python-dev python-virtualenv libjpeg62-dev libxslt1-dev git-core subversion zlib1g-dev libbz2-dev wget cURL elinks gettext

Then we create a virtual python environement using virtualenv. This is alway a good practice since that way we get a clean copy of our system-python, we can't break it by installing eggs that might collide with other eggs::

    $ virtualenv --no-site-packages py27

Then we download, unpack and install the unified installer of Plone::

    $ mkdir training
    $ mkdir tmp
    $ cd tmp
    $ wget https://launchpad.net/plone/4.2/4.2.1/+download/Plone-4.2.1-UnifiedInstaller.tgz
    $ tar xzf Plone-4.2.1-UnifiedInstaller.tgz
    $ cd Plone-4.2.1-UnifiedInstaller
    $ ./install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/training

The unified installer is an amazing tool that compiles it's own python, brings with it all the python-eggs we need and puts them in a buildout-cache. It then creates a buildout and makes Plone ready to run.

We'll use this Plone, that is found in /home/vagrant/training/zinstance on the virtual machine.

Later we'll leave the unified installer behind and build our own little buildout. Buildout will be explained later in depth.


Starting Plone (Patrick)
------------------------

We control Plone with a small script called "instance"::

    $ ./bin/instance fg

This starts Plone and we can see what it is doing

It offers the following options::

    $ ./bin/instance fg
    $ ./bin/instance start
    $ ./bin/instance stop
    $ ./bin/instance debug -P Plone

Depending on your computer, it will take up to a minute until Zope will tell you that its ready to serve requests.

A Zope standard installation always listens on port 8080, so lets have a look at our Zope site by visiting http://localhost:8080

As you can see, there is no Plone yet!
We have a running Zope with a database but no content. But luckily there is a button to create a Zope site.
Click on that button. This opens a form to create a Plone site. Use "Plone" as the site id.


The anatomy of Plone introduction (Patrick)
-------------------------------------------

Zope, Plone, GenericSetup, CMF, Acquisition, what is all that actually?

Zope is an application server.
It serves applications that you write to users via http.
Before Zope, there usually was an Apache server that would call a script and give the request as an input. The script would then just print HTML to the standard output. Apache returned that to the user. Opening database connections, checking permission constraints, generating valid HTML, configuring caching, interpreting form data and everything you have to do on your own. When the second request comes in, you have to do everything again.

Jim Fulton thought that this was slightly tedious. So he wrote code to handle requests. He believed that site content is object oriented and that the URL should somehow point directly into the object hierarchy, so he wrote an object oriented database, called ZODB.
Then there were transactions, so that it became a real database and after a while there were python scripts that could be edited through the web.
One missing piece is important and complicated: ``Acquisition``.

Acquisition is a kind of magic. Imagine a programming system where you do not access the file system and where you do not need to import code. You work with objects. An object can be a folder that contains more objects, a HTML page, data, or another script. To access an object, you need to know where the object is. Objects are found by paths that look like URLs, but without the domain name. Now Acquisition allows you to write an incomplete path. An incomplete path is a relative path, it does not explicitly state that the path starts from the root, it starts relative to where the code object is. If Zope cannot resolve the path to an object relative to your code, I tries the same path in the containing folder. And then the folder containing the folder.
This might sound weird, what do I gain with this? You can have different data or code depending on your ``context``. Imagine you want to have header images differing for each section of your page, sometimes even differing for a specific subsection of your site. So you define a path header_image and put a header image at the root of your site. If you want a folder to have a different header image, you put the header image into this folder.
Please take a minute to let this settle and think, what this allows you to do.

  - contact forms with different e-mail adresses per section
  - different CSS styles for different parts of your site
  - One site, multiple customers, everything looks different for each customer.

Basically this is Zope.

After many successfully created websites based on Zope, a number of recurring requirements emerged, and some Zope developers started write CMF, the Content Management Framework.
The CMF offers many services that help you to write a CMS based on Zope.
Most objects you see in the ZMI are part of the CMF somehow.
The developers behind CMF do not see CMF as a ready to use CMS. They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

This is one way to do it. The Plone founders Alexander Limi and Alan Runyan thought differently, and created a CMS that was usable and beautiful out of the box, based on CMF. They named in Plone.

Here are two numbers, without further comment:

Last German Zope conference (2010): 80 visitors (There is no international Zope conference)

First German Plone conference (2012): 150 visitors

The Plone and Zope community are very similar. Even though in the past, a lot of Zope developers who did not use Plone envied Plone for it success and tried to marginalize the Plone success with bad mouthing. If you meet a Zope developer making bad remarks about Plone, be kind to him. It is hard to accept that your superior, cleaner system is not used by anybody, because Plone is user friendly and beautiful.

Because there is such a big overlap of the communities, it can sometimes be confusing, where some functionality is coming from.

- CMFEditions: Written by Plone developers
- GenericSetup: Written by CMF developers

Summarizing all this in a single sentence:

    We run Zope the application server. Our main application is Plone.

