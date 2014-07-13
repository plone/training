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

- presentation: the narrative documentation that is visible online

- manual ("make manual"): A abbreviated (often bullet-points) version used for the projector during the training.


Contributing
------------

Everyone is welcome to contribute. Minor bugfixes can be pushed directly in the `repository <https://github.com/plone/training>`_, bigger changes should made as `pull-requests <https://github.com/plone/training/pull/>`_.

When contributing to the training you should keep in mind that it builds in two different versions:

manual
    The verbose version used for the online-documentation and for the trainer. Build it in sphinx with ``make manual``.

presentation
    The abbreviated version used for the projector during a training. It should not (but still does) include a lot of verbose text but mostly bullet-points. Build it in sphinx with ``make presentation``.

By prefixing a indented block of text or code with ``.. only:: presentation`` or ``.. only:: manual`` you can control which of the versions the indented block will show up. Content without a prefix will be included in both versions.


License
-------

The Mastering Plone Training is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

Make sure you have filled out a `Contributor Agreement <http://plone.org/foundation/contributors-agreement>`_.

If you haven't filled in a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net
Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons. You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".

