.. _javascript-label:

Exercises
=========

Prerequisites
-------------

- Follow the instructions here to get a training buildout installed:
  https://training.plone.org/5/plone_training_config/instructions.html
- Fork https://github.com/collective/collective.jstraining and install your fork
  into your buildout from the previous step
- npm/nodejs install on your system
- webpack installed on your system


Install forked collective.jstraining
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add this line to the end of your `buildout.cfg` file:

    collective.jstraining = git <location of your fork>

`<location of your fork>` should be replaced with where your fork is.

Finally, add `collective.jstraining` to the auto-checkout list::

    auto-checkout =
      ...
      collective.jstraining
      ...

Contents
--------

..  toctree::
    :maxdepth: 3
    :numbered: 1

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
