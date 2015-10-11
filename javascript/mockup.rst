=====================================================
Mockup - A Patternslib based collection of components
=====================================================


Plone 5 ships with a revamped UI. An important part of the new UI are a collection of new input widgets, as we are used to use in the so called Web 2.0 era.

For Plone, it was high time to update and moderize it's input widgets. Not because the new ones look much better, but because they offer a much comfortable way of entering data. To update Plone's widgets was the goal of ``plone.app.widgets``, started by Nathan van Gheem and pushed wide forward by Rok Garbas. Rok forked Patternslib and created the Mockup project. Patternslib used a complex configuration syntax parser instead of a simple JSON based approach and the test coverage was not high enough. Besides it was fun to create something new, so Mockup was born. There were concerns about having two project with the same goal, so JC Brand took the initiative and brought the two projects back together. Where Mockup had a dependency on ``mockup-core`` with a base pattern to extend from, a configuration parser, pattern registry and Grunt infrastructure, this dependency was removed and replaced by a dependency on ``patternslib``.

However the story behind this was, those projects led the foundation to the new way of developing JavaScript in Plone.


The Mockup project structure
============================

This is how Mockup is structured on the filesystem::

    mockup
    ├── bower.json               - Bower managed dependencies
    ├── Makefile                 - Makefile targets to bootstrap, build bundles
    ├── mockup
    │   ├── bower_components
    │   ├── configure.zcml
    │   ├── Gruntfile.js
    │   ├── index.html
    │   ├── js
    │   │   ├── bundles
    │   │   │   ├── docs.js
    │   │   │   ├── plone.js
    │   │   │   └── widgets.js
    │   │   │   └── ...
    │   │   ├── config.js        - RequireJS configuration
    │   │   ├── docs             - ReactJS based documentation framework
    │   │   │   ├── app.js
    │   │   │   ├── ...
    │   │   ├── grunt.js
    │   │   ├── i18n.js
    │   │   ├── i18n-wrapper.js
    │   │   ├── router.js
    │   │   ├── ui
    │   │   │   ├── templates
    │   │   │   │   └── popover.xml
    │   │   │   └── views
    │   │   │       ├── base.js
    │   │   │       ├── buttongroup.js
    │   │   │       ├── ...
    │   │   └── utils.js
    │   ├── less
    │   │   ├── base.less
    │   │   ├── docs.less
    │   │   ├── plone.less
    │   │   └── widgets.less
    │   │   └── ...
    │   ├── lib
    │   │   ├── jquery.event.drag.js
    │   │   └── jquery.event.drop.js
    │   ├── node_modules -> ../node_modules
    │   ├── patterns
    │   │   ├── autotoc
    │   │   │   ├── pattern.autotoc.less
    │   │   │   └── pattern.js
    │   │   ├── livesearch
    │   │   │   ├── pattern.js
    │   │   │   └── pattern.livesearch.less
    │   │   ├── select2
    │   │   │   ├── pattern.js
    │   │   │   └── pattern.select2.less
    │   └── tests
    │       ├── config.js
    │       ├── fakeserver.js
    │       ├── files
    │       │   ├── lessconfig.js
    │       │   ├── mapper.html
    │       │   └── r.js
    │       ├── i18n-test.js
    │       ├── images
    │       │   ├── extralarge.jpg
    │       │   ├── large.jpg
    │       │   ├── ...
    │       ├── json
    │       │   ├── contextInfo.json
    │       │   ├── fileTree.json
    │       │   ├── ...
    │       ├── pattern-autotoc-test.js
    │       ├── pattern-livesearch-test.js
    │       ├── pattern-select2-test.js
    │       ├── ...
    ├── node_modules
    ├── package.json
    ├── provision.sh
    ├── setup.py
    └── Vagrantfile



