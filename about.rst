.. _about-label:

About Mastering Plone
=====================

This training was created by Philip Bauer and Patrick Gerken of `starzel.de <http://www.starzel.de>`_ to create a canonical training for future Plone developers. The aim is that anyone with the appropriate knowledge can give a training based on it and contribute to it. It is published as Open Source on `github <https://github.com/plone/training>`_ and `training.plone.org <http://training.plone.org/>`_.

If you want to inquire the original authors about organizing a training please contact them at team@starzel.de.


.. _about-upcoming-label:

Upcoming Trainings
------------------

Ask for trainings on https://community.plone.org

.. _about-previous-label:

Previous Trainings
------------------

The Mastering Plone Training was so far held publicly at the following occasions:

* `October 2015, Bucharest <https://2015.ploneconf.org/trainings>`_
* `March 2015, Munich <http://www.starzel.de/leistungen/training/>`_
* Plone Conference 2014, Bristol
* `June 2014, Caracas <https://twitter.com/hellfish2/status/476906131970068480>`_
* `May 2014, Munich <http://www.starzel.de/blog/mastering-plone>`_
* `PythonBrasil/Plone Conference 2013, Brasilia <http://2013.pythonbrasil.org.br/>`_
* `PyCon DE 2012, Leipzig <https://2012.de.pycon.org/>`_
* `Plone Conference 2012, Arnheim <http://2012.ploneconf.org/the-event/training/conference-trainings/mastering-plone>`_
* `PyCon De 2011, Leipzig <http://2011.de.pycon.org/2011/home/>`_


.. _about-trainers-label:

Trainers
--------

The following trainers have given trainings based on Mastering Plone:

Philip Bauer
    Philip Bauer is a web developer from Munich who fell in love with Plone in 2005 and since then works almost exclusively with Plone. A historian by education he drifted towards creating websites in the 90's and founded the company Starzel.de in 2000. He is a member of the Plone foundation, loves teaching and is dedicated to Open Source. Among other Plone-related projects he started creating the Mastering Plone Training so that everyone can become a Plone-Developer.

Patrick Gerken
    Patrick Gerken works with Python since 2002. He started working with pure Zope applications and now develops mainly with Plone, Pyramid and Javascript as well as doing what is called DevOps. He works at Zumtobel Group.

Steve McMahon
    Steve McMahon is a long-time Plone community member, contributor and trainer. He is the creator of PloneFormGen and maintainer of the Unified installer. Steve also wrote several chapters of Practical Plone and is an experienced speaker and instructor.

Steffen Lindner
    Steffen Lindner started developing Plone in 2006. He worked on small Plone sites and also with huge intranet sites. As Open Source / Free Software developer he joined the Plone core developer team 2011 and works at Starzel.de.

Fulvio Casali
    Fulvio Casali has been working almost exclusively with Plone since 2008.  He struggled for years to find his way around the source code of Plone when there was no documentation and no trainings, and feels passionate about helping users and developers become proficient.  He loves participating in Plone community events, and organized two strategic Plone sprints on the northwest coast of the USA and helped galvanized the developer community there.

Johannes Raggam
    Johannes Raggam from Graz/Austria works most of the time with a technology stack based around Python, Plone, Pyramid and Javascript. As an active Open Source / Free Software developer he believes in the power of collaborative work. He is a BlueDynamics Alliance Partner and Plone Core Contributor since 2009, a member of the Plone Framework Team since 2012 and Plone Foundation member.

Franco Pellegrini
    Franco Pellegrini is a software developer from Cordoba, Argentina. He started developing Plone in 2005 in a small software company, and as an independent contractor since 2011. He believes in free software philosophy, and so, he has been a Plone core developer since 2010 and Framework Team member since 2012.

Fred van Dijk
    Fred, from Rotterdam the Netherlands, has been exposed to Plone early on as a user. In 2007 he joined Zest Software to work on and with Plone and Python web apps full time. He can focus on the business side, helping users decide on which features are most valuable to develop or when to stick with standard functionality. He also gives training on using and administering the CMS. On the IT side he has plenty technical knowledge to work on code, system administration and do project management in a team of developers.

Leonardo Caballero
    Leonardo J. Caballero G. of Maracaibo, Venezuela, is a Technical Director at Covantec R.L. and Conectivo C.A. Leonardo maintains the Spanish translations of more than 49 Plone Add-ons as well as Spanish-language documentation for Plone itself. He has contributed several Plone Add-ons that are part of PloneGov. Currently serving the Plone Board as a Plone Ambassador, Leonardo has also served as an Advisory Board member and has spoken at or helped organize Plone and open-source events throughout South America.

.. _about-use-label:


Using the documentation for a training
---------------------------------------

Feel free to organize a training yourself. Please be so kind to contribute any bug fixes or enhancements you made to the documentation for your training.

The training is rendered using sphinx and builds in two flavors:

default
    The verbose version used for the online documentation and for the trainer. Build it in sphinx with ``make html`` or use the online version.

presentation
    A abbreviated version used for the projector during a training. It should use more bullet points than verbose text. Build it in sphinx with ``make presentation``.

.. note::

    By prefixing an indented block of text or code with ``.. only:: presentation`` you can control that this block is used for the presentation version only.

    To hide a block from the presentation version use ``.. only:: not presentation``

    Content without a prefix will be included in both versions.


The readthedocs theme
+++++++++++++++++++++

We slightly tweaked readthedocs theme in ``_static/custom.css`` so that it works better with projectors:

- We start hiding the navigation bar much earlier so that it does not interfere with the text.
- We enlarge the default width of the content-area.

Exercises
++++++++++

Some additional javascript shows hidden solutions for exercises by clicking.

Just perpend the solution with this markup::

    ..  admonition:: Solution
        :class: toggle

Here is a full example::

    Exercise 1
    ^^^^^^^^^^

    Your mission, should you choose to accept it...

    ..  admonition:: Solution
        :class: toggle

        To save the world with only seconds to spare do the following:

        .. code-block:: python

            from plone import api

It will be rendered like this:

Exercise 1
^^^^^^^^^^

Your mission, should you choose to accept it...

..  admonition:: Solution
    :class: toggle

    To save the world with only seconds to spare do the following:

    .. code-block:: python

        from plone import api


Building the documentation locally
----------------------------------

Dependencies
++++++++++++

Please make sure that you have `Enchant <http://www.abisource.com/projects/enchant/>`_ installed, this is needed for spell-checking.

Install Enchant on OS X:

.. code-block:: bash

    brew install enchant

Install Enchant on Ubuntu:

.. code-block:: bash

    sudo apt-get install enchant


To build the documentation follow these steps:

.. code-block:: bash

    $ git clone https://github.com/plone/training.git --recursive
    $ cd training
    $ virtualenv-2.7 .
    $ source bin/activate

Now install dependencies and build.

.. code-block:: bash

    $ pip install -r requirements.txt
    $ make html

You can now open the output from ``_build/html/index.html``. To build the presentation version use ``make presentation`` instead of ``make html``. You can open the presentation at ``presentation/index.html``.

Build new
---------

.. code-block:: bash

    $ git clone https://github.com/plone/training.git --recursive
    $ cd training
    $ virtualenv-2.7 .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ make html

Now you can open documentation with your web-bowser.

If you use OS X you can just do:

.. code-block:: bash

    $ open _build/html/index.html

In the case of Linux, Ubuntu for example you can do:

.. code-block:: bash

    $ firefox _build/html/index.html

.. note::

    If you do not use Firefox but Chrome, please replace firefox with google-chrome e.g

.. code-block :: bash

    $ google-chrome _build/html/index.html




Update existing
+++++++++++++++

.. code-block:: bash

    $ git pull
    $ source bin/activate
    $ make html
    $ open _build/html/index.html


Technical set up to do before a training (as a trainer)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

- Prepare a mailserver for the user registration mail (http://plone-training.readthedocs.org/en/latest/features.html#configure-a-mailserver)
- If you do only a part of the training (Advanced) prepare a database with the steps of the previous sections. Be aware that the file- and blobstorage in the Vagrant box is here: /home/vagrant/var/ (not at the buildout path /vagrant/buildout/)

Train the trainer
-----------------

If you are a trainer there is a special mini training about giving technical trainings. We really want this material to be used, re-used, expanded and improved by Plone trainers world wide. These chapters don't contain any Plone specific advice, there's background, theory,  check lists and tips for anyone trying to teach technical subjects.

:doc:`trainthetrainer/index`

.. _about-contribute-label:

Contributing
------------

Everyone is **very welcome** to contribute. Minor bug fixes can be pushed directly in the `repository <https://github.com/plone/training>`_, bigger changes should made as `pull-requests <https://github.com/plone/training/pulls/>`_ and discussed previously in tickets.


.. _about-licence-label:

License
-------

The Mastering Plone Training is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

Make sure you have filled out a `Contributor Agreement <https://plone.org/foundation/contributors-agreement>`_.

If you haven't filled out a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net
Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons. You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".

