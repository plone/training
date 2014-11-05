About Mastering Plone
=====================

This training was created by Philip Bauer and Patrick Gerken of `starzel.de <http://www.starzel.de>`_ to create a canonical training for future Plone developers. The aim is that anyone with the appropriate knowledge can give a training based on it and contribute to it. It is published as Open Source on `github <https://github.com/plone/training>`_ and `readthedocs <http://plone-training.readthedocs.org/>`_.

If you want to inquire the original authors about organizing a training please contact them at team@starzel.de.


Upcoming Trainings
------------------

`Spring 2015, Munich <http://www.starzel.de/leistungen/training/>`_ (the exact date will be announced soon)
    by Philip Bauer and Patrick Gerken


Previous Trainings
------------------

The Mastering Plone Training was so far held publicly at the following occasions:

* `Plone Conference 2014, Bristol <http://2014.ploneconf.org/training>`_
* `June 2014, Caracas <https://twitter.com/hellfish2/status/476906131970068480>`_
* `May 2014, Munich <http://www.starzel.de/blog/mastering-plone>`_
* `PythonBrasil/Plone Conference 2013, Brasilia <http://2013.pythonbrasil.org.br/program/training/mastering-plone>`_
* `PyCon DE 2012, Leipzig <https://2012.de.pycon.org/>`_
* `Plone Conference 2012, Arnheim <http://2012.ploneconf.org/the-event/training/conference-trainings/mastering-plone>`_
* `PyCon De 2011, Leipzig <http://2011.de.pycon.org/2011/home/>`_


Trainers
--------

The following trainers have given trainings based on Mastering Plone:

Leonardo Caballero
    Leonardo J. Caballero G. of Maracaibo, Venezuela, is a Technical Director at Covantec R.L. and Conectivo C.A. Leonardo maintains the Spanish translations of more than 49 Plone Add-ons as well as Spanish-language documentation for Plone itself. He has contributed several Plone Add-ons that are part of PloneGov. Currently serving the Plone Board as a Plone Ambassador, Leonardo has also served as an Advisory Board member and has spoken at or helped organize Plone and open-source events throughout South America.

Philip Bauer
    Philip Bauer is a Webdeveloper from Munich who fell in love with Plone in 2005 and since then works almost exclusively with Plone. A historian by education he drifted towards creating websites in the 90's and founded the company Starzel.de in 2000. He is a member of the Plone foundation, loves teaching and is dedicated to Open Source. Among other Plone-related projects he started creating the Mastering Plone Training so that everyone can become a Plone-Developer.

Patrick Gercken
    Patrick Gerken works with Python since 2002. He started working with pure Zope-Applications and now to develops mainly with with Plone, Pyramid and Javascript as well as doing what is called DevOps. He works at Starzel.de.

Steve McMahon
    Steve McMahon is a long-time Plone community member, contributor and trainer. He is the creator of PloneFormGen and maintainer of the Unified installer. Steve also wrote several chapters of Practical Plone and is an experienced speaker and instructor.

Steffen Lindner
    Steffen Lindner started developing Plone in 2006. He worked on small Plone sites and also with huge intranet sites. As Open Source / Free Software developer he joined the Plone core developer team 2011 and works at Starzel.de.


Using the documentation for a training
---------------------------------------

Feel free to organize a training yourself. Please be so kind to contribute any bugfixes or enhancements you made to the documentation for your training.

The training is rendered using sphinx and builds in two flavors:

default
    The verbose version used for the online-documentation and for the trainer. Build it in sphinx with ``make html`` or use the online-version.

presentation
    A abbreviated version used for the projector during a training. It should uses more bullet-points than verbose text. Build it in sphinx with ``make presentation``.

.. note::

    By prefixing an indented block of text or code with ``.. only:: presentation`` you can control that this block is used for the presentation-version only.

    To hide a block from the presentation-version use ``.. only:: not presentation``

    Content without a prefix will be included in both versions.


The readthedocs-theme
+++++++++++++++++++++

We slightly tweaked readthedocs-theme in ``_static/custom.css`` so that it works better with projectors:

- We start hiding the navbar much earlier so that it does not interfere with the text.
- We enlarge the default width of the content-area.

Excercises
++++++++++

Some additional javascript shows hidden solutions for exercises by clicking.

Just prepend the solution with this markup::

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
++++++++++++++++++++++++++++++++++

To build the documentation follow these steps:

.. code-block:: bash

    $ git clone https://github.com/plone/training.git
    $ cd training
    $ virtualenv-2.7 .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ make html

You can now open the output from ``_build/html/index.html``. To build the presentation-version use ``make presentation`` instead of ``make html``. You can open the presentation at ``presentation/index.html``.


Things to do before a training (as a trainer)
+++++++++++++++++++++++++++++++++++++++++++++

- Prepare a mailserver for the user registration mail (http://plone-training.readthedocs.org/en/latest/features.html#configure-a-mailserver)
- If you do only a part of the training (Advanced) prepare a database with the steps of the previous sections. Be aware that the file- and blobstorage in the Vagrant box is here: /home/vagrant/var/ (not with the buildout path /vagrant/buildout/)


Contributing
------------

Everyone is **very welcome** to contribute. Minor bugfixes can be pushed direcly in the `repository <https://github.com/plone/training>`_, bigger changes should made as `pull-requests <https://github.com/plone/training/pull/>`_ and discussed previously in tickets.

By prefixing a indented block of text or code with ``.. only:: presentation`` or ``.. only:: not presentation`` you can control which of the versions the indented block will show up. Content without a prefix will be included in both versions.


License
-------

The Mastering Plone Training is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

Make sure you have filled out a `Contributor Agreement <http://plone.org/foundation/contributors-agreement>`_.

If you haven't filled in a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net
Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons. You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".

