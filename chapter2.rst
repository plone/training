2. Installation & Setup (60 Min) (Philip)
=========================================

Hosting your own site
---------------------

If you want to host a Plone-website yourself then running it on your Laptop may not be the smartest option. We will cover some options for hosting tomorrow. One option is http://ploud.com whre you can host one real Plone-Site for free.

Options:

* Ploud.net
* Webfaction
* gocept
* Starzel
* AWS
* Rackspace


Brief introduction of several installation-options
--------------------------------------------------

Plone 4.2 requires a working Python 2.7 and several other system-tools that not every OS provides. Therefore the installation of Plone is differen on every system (

* MacPorts / homebrew
* python-buildout
* PyWin32
* Linux-packages
* pre-installed Pythons

MacOS 10.8 and Ubuntu 12.4 come with a working default Python 2.7 built in. These are the lucky ones. But to run a older Plone-version you need Python 2.4 and that's not always easy to install.

To find out how to install Plone on your machine read http://plone.org/documentation/manual/installing-plone

Everyone usually uses his primary system to develop Plone. I use MacOS and therefore I use the python-buildout (https://github.com/collective/buildout.python) to compile all neccessary version of python and homebrew (http://mxcl.github.com/homebrew/) for some linux-tools. Patrick uses ubuntu. Our friend Stefan always uses the unified installer's python. Alan Runyan (one of Plone's founders) uses Windows and i have no idea how he can live with that.

* unified installers for all 'nix (including MacOS)
* one-click installers for Windows and Mac
* very old package for debian (don't use)
* use some your python and create your own buildout


Vagrant and Virtualbox
----------------------

To not waste too much time with installing and debugging the differences between systems we use a virtual machine (ubuntu 12.4) to run Plone during the training. We install virtualbox and vagrant a wrapper that manages virtual machines.

Vagrant is a wrapper for Oracle’s VirtualBox to create and manage virtual environments.


Installation
------------

*All these steps are done by vagrant/puppet.*

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


Customising the buildout (Patrick)
----------------------------------

TODO: (enter "admin" as password?)
Now, lets run buildout and wait a bit...
Buildout will create a start script for us. The start script accepts some parameters, the first is the command.




Starting Plone (Patrick)
------------------------

We control Plone with a small script called "instance"

``$ ./bin/instance fg``
    this starts Plone and we can see what it's doing

It offers the following options::

    ./bin/instance fg
    ./bin/instance start
    ./bin/instance fstop
    ./bin/instance debug -P Plone

Depending on your computer, it will take up to a minute until zope will tell you that its ready to serve requests.

A Zope Standard installation always listens on port 8080, so lets have a look at our Zope Site by visiting http://localhost:8080

As you can see, there is no Plone yet!
We have a running zope with a database but no content. But luckily there is that button to create a zope site.
Click on that button. Use "Plone" as the site id.


The anatomy of Plone introduction (Patrick)
-------------------------------------------

Systemarchitektur erklären (5 Minuten)

* Zope
  * Scripts in the database
  * Acqusition to simulate class and stuff, persistency.
* CMF
* Plone
* Erweiterungen



Now, lets clear up a bit of mumbo jumbo.
I talk about Zope, sometimes about Plone. Whats the difference about that?

Zope is an application server. Before zope, there usually was an apache server that would call a python script, and send the request via stdout or something. The script would then just print some stuff and this was the html.
Jim Fulton thought, that this is pretty stupid. So he wrote some code to handle requests. He believed that site content is object oriented and that the url should somehow point directy into the object hierarchy, so he wrote an object oriented database, called ZODB. Then there where transactions, so that it became a real database and after a while, python scripts that could be edited through the web, followed. One lost puzzle is important, Acquisition.
Acquisition was kind of magic. Imagine a world, where there is no file system, and there are no imports. That is the vision of zope. Now if you have a folder food, and in there is a folder fruits, and in there is a page apple, and there are many many different pages on different levels in hierarchy, how would you implement some kind of functionality like displaying an e-mail adress that is defined centraly? The Answer is acquisition. In my View, I would maybe call context.getEmail(). Context stands for the object on which I currently am in the ZODB. Now there is no script getEmail() in here, but thanks to acquisition, python looks for the attribute a level higher, and another level and so on. This is the way to go for writing whole applications through the web and in a structured manner.
Basically this is Zope.
When I open http://localhost:8080/Plone/manage, I see the Zope Management Interface, a view into my object oriented database.

After many successfully created websites based on zope, a number of recurring requirements emerged, and the CMF, the Content Management Framework was written.
Most objects you see in the ZMI are part of the CMF somehow.
The people behind CMF did not see CMF as a CMS. They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

This is one way to do it. Plone Founders Alexander Limi and Alan Runyan thought differently, and created a CMS that was usable and beautiful out of the box. Plone.

Well, what do you think was a more successful way to go on?
(Hint: Last german zope conference (2010): 80 ppl (There is no international zope conf), First german plone conf(2012): 150ppl)
In practice, there is much much less in Zope world going on than in the Plone World. That means, that the question, what is part of CMF and what not, is a bit diluted. CMFEditions is not part of CMF, btw.

So the important parts are this:
We run Zope, the application server. Our Main application is Plone.

