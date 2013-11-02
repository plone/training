Creating your own eggs to customize Plone
=========================================

Our own code has te be organised as an egg. An Egg is a zip file or a directory that follows certain conventions. We are going to use zopeskel. Zopeskel creates a skeleton projekt. We only need to fill the holes.

If your vagrant-machine is not running yet you should start it now.

.. code-block:: bash

    $ vagrant up
    $ vagrant ssh
    $ cd /vagrant/buildouts
    $ git pull
    $ cd /vagrant/plone
    $ cp /vagrant/buildouts/chapter6/buildout.cfg .
    $ cp /vagrant/buildouts/chapter6/versions.cfg .
    $ source ./bin/activate
    $ ./bin/buildout
    $ cd src


We move to the ``src`` directory and call a script called ``zopeskel``.

.. code-block:: bash

    $ mkdir src
    $ cd src
    $ ../bin/zopeskel

This returns a list of available templates we might use. We choose plone_basic.

.. code-block:: bash

    $ ../bin/zopeskel plone_basic

* Enter project name: ``ploneconf.talk``

.. manual-only::

    If this is your first egg, this is a very special moment. We are going to create the egg with a script that generates a lot of necessary files. They all are necessary, but sometimes in a subtle way. It takes a while do understand their full meaning. Only last year I learnt and understood why I should have a manifest.in file. You can get along without one, but trust me, you get along better with a proper manifest file.

Lets have a look at it.

* bootstrap.py
* buildout.cfg
* CHANGES.txt
* CONTRIBUTORS.txt
* docs/*
* README.txt
* setup.py
* configure.zcml
* metadata.xml

