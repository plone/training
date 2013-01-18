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

During the tutorial we'll use Options 1 and 4 to install and run Plone.

Read more about instaling Plone: https://plone.org/documentation/manual/installing-plone and http://developer.plone.org/getstarted/installation.html


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


Vagrant and Virtualbox
----------------------

To not waste too much time with installing and debugging the differences between systems we use a virtual machine (ubuntu 12.4) to run Plone during the training. For this we use VirtualBox and vagrant.

Vagrant (http://www.vagrantup.com) is a command-line wrapper for Oracle’s VirtualBox (https://www.virtualbox.org) to create and manage virtual environments.


Installation
------------

*These steps are automatically done by vagrant/puppet.* They are only explained here.

We'll first use the unified installer and the default Plone-configuration (called buildout) that comes with it. Later we'll create our own buildout and extend it as we wish.

The first installation is in fact done by Puppet, a tool to automatically manage servers (real and virtual). We won't get into it Puppet since it's not that widely used. This is what we bascally do if we did it by hand:

First we install some packages::

    $ sudo aptitude update --quiet --assume-yes
    $ sudo apt-get install python-dev python-virtualenv libjpeg62-dev libxslt1-dev git-core subversion zlib1g-dev libbz2-dev wget curl elinks gettext

Then we create a virtual python environement using virtualenv. This is alway a good practice since that way we get a clean copy of our system-pythonm we can't break it by installing stuff that might collide with other stuff::

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

We control Plone with a small script called "instance"

``$ ./bin/instance fg``

This starts Plone and we can see what it's doing

It offers the following options:


.. sourcecode:: bash

    ./bin/instance fg
    ./bin/instance start
    ./bin/instance fstop
    ./bin/instance debug -P Plone

Depending on your computer, it will take up to a minute until Zope will tell you that its ready to serve requests.

A Zope standard installation always listens on port 8080, so lets have a look at our Zope site by visiting http://localhost:8080

As you can see, there is no Plone yet!
We have a running Zope with a database but no content. But luckily there is that button to create a Zope site.
Click on that button. This opens a form to create a Plone site. Use "Plone" as the site id.


The anatomy of Plone introduction (Patrick)
-------------------------------------------

Zope, Plone, Genericsetup, CMF, Acquisition, whats all that, actually?

Zope is an application server.
Before Zope, there usually was an Apache server that would call a python/perl/shell script and send the request via stdout or something. The script would then just print html to the standard output.

Jim Fulton thought that this is pretty stupid. So he wrote some code to handle requests. He believed that site content is object oriented and that the url should somehow point directy into the object hierarchy, so he wrote an object oriented database, called ZODB.
Then there were transactions, so that it became a real database and after a while there were python scripts that could be edited through the web.
One lost puzzlepiece is important, ``Acquisition``.

Acquisition is a kind of magic. Imagine a world, where there is no file system, and there are no imports. If you have a folder food, and in there is a folder fruits, and in there is a page apple, and there are many many different pages on different levels in hierarchy, how would you implement some kind of functionality like displaying an e-mail adress that is defined centrally?
The Answer to this is Acquisition. In my page that shall show the e-mail, I would maybe call context.getEmail(). Context stands for the object on which I currently am in the ZODB. Now there is no script getEmail() in here, but thanks to acquisition, python looks for the attribute a level higher, and another level and so on. This is the way to go for writing whole applications through the web and in a structured manner.

Basically this is Zope.

When I open http://localhost:8080/Plone/manage, I see the Zope Management Interface, a view into my object oriented database.

After many successfully created websites based on Zope, a number of recurring requirements emerged, and the CMF, the Content Management Framework was written.
Most objects you see in the ZMI are part of the CMF somehow.
The people behind CMF do not see CMF as a CMS. They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

This is one way to do it. Plone Founders Alexander Limi and Alan Runyan thought differently, and created a CMS that was usable and beautiful out of the box. Plone.

Well, what do you think was a more successful way to go on?

A little hint:

Last german Zope conference (2010): 80 ppl (There is no international Zope conf)

First german Plone conferene (2012): 150ppl

Nowadays, all communities communicate via mailing lists primarely, and the plone mailing lists are the most active ones.
Unfortunately, it is not so easy to identify the origins of a piece of code. CMFEditions? From Plone. GenericSetup? Thats from the CMF people. Nowadays it is safe to say that if you aren't sure, ask the Plonies. (As a long time "no Plone just Zope" dev, this makes me sad. But then again, Plonistas have been frowned upon by many Zope devs for a long time, now look who iss successful now ;-) )

Summed all up in one sentence, this sentence would be:

    We run Zope, the application server. Our main application is Plone.

