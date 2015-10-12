===========================================
The JavaScript development process in Plone
===========================================

Code style
==========

Together with ``plone.api`` we developed `code style guidelines <https://github.com/plone/plone.api/blob/master/docs/contribute/conventions.rst>`_, which we are enforcing now for core Plone development.
Finally!
This makes code so much more readable.
It currently doesn't cover JavaScript code guidelines, but those were thought of, when Mockup was developed.
And luckily, similar to PEP 8 and the associated tooling (``pep8``, ``pyflakes``, ``flake8``), JavaScript also has some guidelines - not official, but well respected.
`Douglas Crockford <http://javascript.crockford.com/>`_ - besides of specifying the JSON standard - wrote the well known book "JavaScript the good parts".
Out of that he developed the code linter `JSLint <http://www.jslint.com/>`_.
Because this one was too strict, some other people wrote `JSHint <http://jshint.com/>`_.

Mockup uses JSHint with the following `.jshintrc configuration file <https://github.com/plone/mockup/blob/master/mockup/.jshintrc>`_:

.. code-block:: javascript

    {
       "bitwise": true,
       "curly": true,
       "eqeqeq": true,
       "immed": true,
       "latedef": true,
       "newcap": true,
       "noarg": true,
       "noempty": true,
       "nonew": true,
       "plusplus": true,
       "undef": true,
       "strict": true,
       "trailing": true,
       "browser": true,
       "evil": true,
       "globals": {
          "console": true,
          "it": true,
          "describe": true,
          "afterEach": true,
          "beforeEach": true,
          "define": false,
          "requirejs": true,
          "require": false,
          "tinymce": true,
          "document": false,
          "window": false
       }
    }


.. note::

    When working with JSHint or JSLint, it can be very useful to get some more context and explanation about several lint-errors.
    There is a lint-error database available, which can be very handy: http://jslinterrors.com/


We strongly recommend to configure your editor of choice to do JavaScript code linting on save.
The Mockup project is enforcing Lint-error-free code.
Besides of that, this will also make you a better coder.
The JSHint site lists some editors with Plugins to support JSHint linting: http://jshint.com/install/


Regarding spaces/tabs and indentation:

- Spaces instead of tabs.
- Tab indentation: 2 characters (to save screen estate).

You have to configure your editor to respect these settings.

Confirming on a common code style makes contributing much more easier, friendly and fun!


Mockup contributions
====================

For each feature, create a branch and make pull-requests on Github.
Try to include all your changes in one commit only, so that our commit history stays clean.
Still, you can do many commits to not accidentally loose changes and still commit to the last commit by doing::

  git commit --amend -am"my commit message".

Don't forget to also include a change log entry in the ``CHANGES.rst`` file.


Documentation
=============

Besides documenting your changes in the ``CHANGES.rst`` file, also include user and developer documentation as appropriate.

For patterns, the user documentation is included in a comment in the header of the pattern file, as described in :ref:`mockup-writing-documentation`.

For function and methods, write an API documentation, following the `apidocjs <http://apidocjs.com/>`_ standard.
You can find some examples throughout the source code.

We also very welcome contributions to the `training documentation <https://github.com/plone/training>`_ and the `official documentation <https://github.com/plone/documentation>`_.
As with other contributions: please create branches and make pull-requests!
