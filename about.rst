About Mastering Plone
=====================

History
-------

This training was created for the "Mastering Plone"-trainings by Philip Bauer and Patrick Gerken of `starzel.de <http://www.starzel.de>`_. It was published in order to create a canonical Plone Training so that anyone with the appropriate knowledge can give a training based on it.


Using the documentation for a training
---------------------------------------

Feel free to organize a training yourself. Please be so kind to contribute any bugfixes or enhancements you made to the documentation for your training.

If you want to contact the original authors about a training you can reach them at team@starzel.de.

The training is rendered using sphinx and builds in two flavors:

default
    The verbose version used for the online-documentation and for the trainer. Build it in sphinx with ``make html`` or use the online-version.

presentation
    A abbreviated version used for the projector during a training. It should uses more bullet-points than verbose text. Build it in sphinx with ``make presentation``.

.. note::

    By prefixing an indented block of text or code with ``.. only:: presentation`` you can control that his block is used for the presentation-version only.

    To hide a block from the presentation-version use ``.. only:: not presentation``

    Content without a prefix will be included in both versions.

The readthedocs-theme
---------------------

We slightly tweaked readthedocs-theme in ``_static/custom.css`` so that it works better with projectors:

- We start hiding the navbar much earlier so that it does not interfere with the text.
- We enlarge the default width of the content-area.

Some additional javascript shows hidden solutions for exercises by clicking.

Just prepend the solution with this markup::

    ..  admonition:: Solution
        :class: toggle

Here is a full example::

    Exercise 1
    ++++++++++

    Your mission, should you choose to accept it...

    ..  admonition:: Solution
        :class: toggle

        I have no clue how they always save the world with only seconds to spare. It would probably contain coding:

        .. code-block:: python

            from plone import api

It will be rendered like this:

Exercise 1
++++++++++

Your mission, should you choose to accept it...

..  admonition:: Solution
    :class: toggle

    I have no clue how they always save the world with only seconds to spare. It would probably contain coding:

    .. code-block:: python

        from plone import api

Building the documentation locally
----------------------------------

To build the documentation follow these steps:

.. code-block:: bash

    $ git clone https://github.com/plone/training.git
    $ cd training
    $ virtualenv-2.7 .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ make html

You can now open the output from ``_build/html/index.html``. To build the presentation-version use ``make presentation`` instead of ``make html``. You can open that output at ``presentation/index.html``.


Contributing
------------

Everyone is welcome to contribute. Minor bugfixes can be pushed direcly in the `repository <https://github.com/plone/training>`_, bigger changes should made as `pull-requests <https://github.com/plone/training/pull/>`_.

By prefixing a indented block of text or code with ``.. only:: presentation`` or ``.. only:: not presentation`` you can control which of the versions the indented block will show up. Content without a prefix will be included in both versions.


License
-------

The Mastering Plone Training is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

Make sure you have filled out a `Contributor Agreement <http://plone.org/foundation/contributors-agreement>`_.

If you haven't filled in a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net
Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons. You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".

