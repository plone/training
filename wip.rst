================
Work In Progress
================


.. todo:: Sync this info with the wiki

Structure
=========

Naming Convention
-----------------

Writing is **not** coding !

Directories
~~~~~~~~~~~

Please use ``-`` and not ``_`` for naming folder

**Bad**: mastering_plone

**Good**: mastering-plone

Underscores are only used for templates like ``_templates`` and for static directories like ``_static``.

Setup
=====

- Every training goes into its own directory in the main repository.
- Every training get its own conf.py and own _template and _static directory with its own content.
- Every training should be able to be build on its own without depending on each other
- One main Makefile to build all trainings [example: website] in the /root of the repository.
- Use intersphinx to link to needed parts if we must. [Not preferred as trainings should be 'standalone']

Tone Of Voice
=============

- Should be set according to audience.
