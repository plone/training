.. _about-mastering-label:

About Mastering Plone
=====================

This training was created by Philip Bauer and Patrick Gerken of `starzel.de <https://www.starzel.de>`_ to create
a canonical training for future Plone developers.

The aim is that anyone with the appropriate knowledge can give a training based on it and contribute to it.
It is published as Open Source on `GitHub <https://github.com/plone/training>`_ and `training.plone.org <https://training.plone.org/>`_.

If you want to inquire the original authors about organizing a training please contact them at team@starzel.de.


.. _about-upcoming-label:

Upcoming Trainings
------------------

If you want to have a training near you please ask for trainings on https://community.plone.org

.. _about-previous-label:

Previous Trainings
------------------

The Mastering Plone Training was so far held publicly at the following occasions:

* `Ploneconf 2018 in Tokyo <https://2018.ploneconf.org/>`_
* `August 2018, Munich <https://plone.org/events/community/mastering-plone-training-in-munich>`_
* `Ploneconf 2017 in Barcelona <https://2017.ploneconf.org/>`_
* `Ploneconf 2016 in Boston <https://2016.ploneconf.org/>`_
* October 2015, Bucharest
* `March 2015, Munich <https://www.starzel.de/leistungen/training/>`_
* Plone Conference 2014, Bristol
* `June 2014, Caracas <https://mobile.twitter.com/hellfish2/status/476906131970068480>`_
* `May 2014, Munich <https://www.starzel.de/blog/mastering-plone>`_
* `PythonBrasil/Plone Conference 2013, Brasilia <http://2013.pythonbrasil.org.br/>`_
* PyCon DE 2012, Leipzig
* Plone Conference 2012, Arnheim
* PyCon De 2011, Leipzig


.. _about-trainers-label:

Trainers
--------

The following trainers have given trainings based on Mastering Plone:

Philip Bauer
    Philip Bauer is a web developer from Munich who fell in love with Plone in 2005 and since then works almost exclusively with Plone.
    A historian by education he drifted towards creating websites in the 90's and founded the company Starzel.de in 2000.
    He is a member of the Plone foundation, loves teaching and is dedicated to Open Source.
    Among other Plone-related projects he started creating the Mastering Plone Training so that everyone can become a Plone-Developer.

Patrick Gerken
    Patrick Gerken works with Python since 2002.
    He started working with pure Zope applications and now develops mainly with Plone, Pyramid and JavaScript as well as doing what is called DevOps.
    He works at Zumtobel Group.

Steve McMahon
    Steve McMahon is a long-time Plone community member, contributor and trainer.
    He is the creator of PloneFormGen and maintainer of the Unified installer.
    Steve also wrote several chapters of Practical Plone and is an experienced speaker and instructor.

Steffen Lindner
    Steffen Lindner started developing Plone in 2006.
    He worked on small Plone sites and also with huge intranet sites.
    As Open Source / Free Software developer he joined the Plone core developer team 2011 and works at Starzel.de.

Fulvio Casali
    Fulvio Casali has been working almost exclusively with Plone since 2008.
    He struggled for years to find his way around the source code of Plone when there was no documentation and no trainings,
    and feels passionate about helping users and developers become proficient.

    He loves participating in Plone community events, and organized two strategic Plone sprints on the northwest coast
    of the USA and helped galvanized the developer community there.

Johannes Raggam
    Johannes Raggam from Graz/Austria works most of the time with a technology stack based around Python, Plone, Pyramid and JavaScript.
    As an active Open Source / Free Software developer he believes in the power of collaborative work.

    He is a BlueDynamics Alliance Partner and Plone Core Contributor since 2009, a member of the Plone Framework Team since 2012 and Plone Foundation member.

Franco Pellegrini
    Franco Pellegrini is a software developer from Cordoba, Argentina.
    He started developing Plone in 2005 in a small software company, and as an independent contractor since 2011.
    He believes in free software philosophy, and so, he has been a Plone core developer since 2010 and Framework Team member since 2012.

Fred van Dijk
    Fred, from Rotterdam the Netherlands, has been exposed to Plone early on as a user.
    In 2007 he joined Zest Software to work on and with Plone and Python web apps full time.

    He can focus on the business side, helping users decide on which features are most valuable to develop or when to stick with standard functionality. He also gives training on using and administering the CMS.
    On the IT side he has plenty technical knowledge to work on code, system administration and do project management in a team of developers.

Leonardo Caballero
    Leonardo J. Caballero G. of Maracaibo, Venezuela, is a Technical Director at Covantec R.L. and Conectivo C.A.
    Leonardo maintains the Spanish translations of more than 49 Plone Add-ons as well as Spanish-language documentation for Plone itself.

    He has contributed several Plone Add-ons that are part of PloneGov.
    Currently serving the Plone Board as a Plone Ambassador, Leonardo has also served as an Advisory Board member
    and has spoken at or helped organize Plone and open-source events throughout South America.

.. _about-use-label:


Using the documentation for a training
---------------------------------------

Feel free to organize a training yourself.
Please be so kind to contribute any bug fixes or enhancements you made to the documentation for your training.

The training is rendered using Sphinx and builds in two flavors:

default
    The verbose version used for the online documentation and for the trainer.
    Build it in Sphinx with ``make html`` or use the online version.

presentation
    An abbreviated version used for the projector during a training.
    It should use more bullet points than verbose text.
    Build it in Sphinx with ``make presentation``.

.. note::

    By prefixing an indented block of text or code with ``.. only:: presentation`` you can control
    that this block is used for the presentation version only.

    To hide a block from the presentation version use ``.. only:: not presentation``

    Content without a prefix will be included in both versions.


The readthedocs theme
+++++++++++++++++++++

We slightly tweaked the `Read the Docs Theme <https://github.com/rtfd/sphinx_rtd_theme>`_
in ``_static/custom.css`` so that it works better with projectors:

- We start hiding the navigation bar much earlier so that it does not interfere with the text.
- We enlarge the default width of the content-area.

Exercises
++++++++++

Some additional JavaScript shows hidden solutions for exercises by clicking.

Prepend the solution with this markup::

    ..  admonition:: Solution
        :class: toggle

Here is a full example

.. code-block:: rst

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

Please make sure that you have `Enchant <https://abiword.github.io/enchant/>`_ installed. This is needed for spell-checking.

Install Enchant on macOS:

.. code-block:: console

    brew install enchant

Install Enchant on Ubuntu:

.. code-block:: console

    sudo apt-get install enchant


To build the documentation follow these steps:

.. code-block:: console

    git clone https://github.com/plone/training.git
    cd training
    python -m venv .
    $ source bin/activate

Now install dependencies and build.

.. code-block:: console

    pip install -r requirements.txt
    make html

You can now open the output from ``_build/html/index.html``.
To build the presentation version use ``make presentation`` instead of ``make html``.

You can open the presentation at ``presentation/index.html``.

Build new
---------

.. code-block:: console

    git clone https://github.com/plone/training.git
    cd training
    python -m venv .
    source bin/activate
    pip install -r requirements.txt
    make html

Now you can open documentation with your web-bowser.

If you use macOS you can do:

.. code-block:: console

    open _build/html/index.html

In the case of Linux, Ubuntu for example you can do:

.. code-block:: console

    firefox _build/html/index.html

.. note::

    If you do not use Firefox but Chrome, please replace firefox with google-chrome e.g

.. code-block :: console

    google-chrome _build/html/index.html




Update existing
+++++++++++++++

.. code-block:: bash

    $ git pull
    $ source bin/activate
    $ make html
    $ open _build/html/index.html


Technical set up to do before a training (as a trainer)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

- Prepare a mailserver for the user registration mail (See :ref:`features-mailserver-label`)
- If you do only a part of the training (Advanced) prepare a database with the steps of the previous sections. Be aware that the file- and blobstorage in the Vagrant box is here: /home/vagrant/var/ (not at the buildout path /vagrant/buildout/)


Upgrade the vagrant and buildout to a new Plone-version
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

- In https://github.com/collective/training_buildout change `buildout.cfg <https://github.com/collective/training_buildout/blob/master/buildout.cfg>`_ to extend from the new `versions.cfg` on http://dist.plone.org/release
- Check if we should to update any versions in https://github.com/collective/training_buildout/blob/master/versions.cfg
- Commit and push the changes to the training_buildout
- Modify the vagrant-setup by modifying :file:`plone_training_config/manifests/plone.pp`. Set the new Plone-version as `$plone_version` in line 3.
- Test the vagrant-setup it by creating a new vagrant-box using the new config.
- Create a new zip-file of all files in `plone_training_config` and move it to `_static`:

.. code-block:: console

   cd plone_training_config
   zip -r ../_static/plone_training_config.zip *

- Commit and push the changes to https://github.com/plone/training


Train the trainer
-----------------

If you are a trainer there is a special mini training about giving technical trainings.
We really want this material to be used, re-used, expanded, and improved by Plone trainers world wide.

These chapters don't contain any Plone specific advice.
There's background, theory, check lists, and tips for anyone trying to teach technical subjects.

:doc:`../teachers-training/index`

.. _about-contribute-label:

Contributing
------------

Everyone is **very welcome** to contribute.
Minor bug fixes can be pushed directly in the `repository <https://github.com/plone/training>`_,
bigger changes should made as `pull-requests <https://github.com/plone/training/pulls/>`_ and discussed previously in tickets.


.. _about-licence-label:

License
-------

The Mastering Plone Training is licensed under a `Creative Commons Attribution 4.0 International License <https://creativecommons.org/licenses/by/4.0/>`_.

Make sure you have filled out a `Contributor Agreement <https://plone.org/foundation/contributors-agreement>`_.

If you haven't filled out a Contributor Agreement, you can still contribute.
Contact the Documentation team, for instance via the `mailinglist <https://sourceforge.net/p/plone/mailman/plone-docs/>`_
or directly send a mail to plone-docs@lists.sourceforge.net

Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons.

You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".
