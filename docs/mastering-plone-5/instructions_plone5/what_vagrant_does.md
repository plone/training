---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
orphan:
---

# What Vagrant is and does

```{note}
These steps are automatically done by Vagrant and Puppet for you. They are only interesting if you want to know what goes on under the hood for preparing your virtual training environment.
```

Vagrant is an automation tool for developers to script the configuration and starting/stopping of virtual machines using applications like VirtualBox or Vmware Fusion/Workstation. The beauty of Vagrant is that it is largely platform independent for Linux, Windows and Apple, so with one 'Vagrantfile' per project you describe a base installation virtual image and all kinds of virtual machine settings you would otherwise have to click and type together in Virtual machine application.

What Vagrant for example does is install a port forward so that `http://localhost:8080` on your physical computer is automatically forwarded to the port Plone will be listening on in the guest virtual machine. After Vagrant has done its thing to set up your virtual machine we are not finished though. Although Vagrant has the option to prebuild specific images it would be a lot of work and waste of bandwidth to redownload a machine images (300-600Mb) each time we would like to change small things in our virtual training environment.

Puppet is a configuration management tool (others you might have heard of are Chef, Ansible and SaltStack) and helps system admnistrators to automatically manage servers (real and virtual). We won't get into Puppet in detail, but it builds on top of our base Vagrant image to further set up our environment.

Vagrant detects when you set up a new machine and runs Puppet or other Provisioners by default only once, although it also can be used to keep machines up to date, which is a bit harder. See the {file}`Vagrantfile` and [Vagrant Documentation](https://developer.hashicorp.com/vagrant/docs), especially the *Provisioning* chapter.

This is basically what Puppet does if we were to configure our system by hand:

First we update Ubuntu and install some packages.

```shell
$ sudo aptitude update --quiet --assume-yes
$ sudo aptitude upgrade --quiet --assume-yes
$ sudo apt-get install build-essential
$ sudo apt-get install curl
$ sudo apt-get install elinks
$ sudo apt-get install gettext
$ sudo apt-get install git
$ sudo apt-get install libedit-dev
$ sudo apt-get install libjpeg-dev
$ sudo apt-get install libpcre3-dev
$ sudo apt-get install libssl-dev
$ sudo apt-get install libxml2-dev
$ sudo apt-get install libxslt-dev
$ sudo apt-get install libyaml-dev
$ sudo apt-get install libz-dev
$ sudo apt-get install nodejs
$ sudo apt-get install npm
$ sudo apt-get install python3.7-dev
$ sudo apt-get install python3.7-tk
$ sudo apt-get install python3.7-venv
$ sudo apt-get install subversion
$ sudo apt-get install unzip
$ sudo apt-get install vim
$ sudo apt-get install wget
$ sudo apt-get install wv
$ sudo apt-get install poppler-utils
$ sudo apt-get install putty-tools
```

Then we create a virtual python environment using virtualenv. This is always a good practice since that way we get a clean isolated copy of our system python, so that we do not break the system python by installing eggs that might collide with other eggs. Python is nowadays used a lot by your operating system as well for all kinds of system tools and scripting.

```shell
$ python3.7 -m venv /home/vagrant/py37
```

Install zc.buildout, setuptools and other dependencies for the current version into the new virtualenv.

```shell
$ /home/vagrant/py37/bin/pip install -r http://dist.plone.org/release/5.2/requirements.txt
```

Now we download and unpack a buildout-cache that holds all the python packages that make up Plone. This is an optimisation: We could skip this step and have buildout download all packages individually from the [python packaging index PyPi](https://pypi.org) but that takes much longer on a first install.

```shell
$ wget http://dist.plone.org/release/5.2/buildout-cache.tar.bz2
$ tar xjf buildout-cache.tar.bz2
```

Then we check out our tutorial buildout from <https://github.com/collective/training_buildout> and build it.

```shell
$ cd /vagrant
$ git clone https://github.com/collective/training_buildout.git buildout
$ cd buildout
```

Then we run buildout:

```shell
$ /home/vagrant/py37/bin/buildout -c vagrant_provisioning.cfg
```

This will download many additional eggs that are not yet part of the buildout-cache and configure Plone to be ready to run.

At this point Vagrant and Puppet have finished their job to set up your virtual training environment on your local machine.

You can now connect to the machine and start Plone.

```shell
$ vagrant ssh
$ cd /vagrant/buildout
$ ./bin/instance fg
```

Now we have a fresh Buildout-based Zope application server, ready to add a Plone site. Go to <http://localhost:8080> and create a Plone site.
