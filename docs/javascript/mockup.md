---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Mockup

A Patternslib based collection of components.

Plone 5 ships with a revamped UI (User Interface).
An important part of the new UI is a collection of new input widgets, that we are used to work with in the so called Web 2.0 era.

For Plone, it was high time to update and modernize its input widgets.

Not because the new ones look much better, but because they offer a much more comfortable way of entering data.

To update Plone widgets was the goal of [plone.app.widgets](https://pypi.org/project/plone.app.widgets), started by Nathan van Gheem and pushed forward by Rok Garbas.
Rok forked Patternslib and created the Mockup project.

Patternslib used a complex configuration syntax parser instead of a simple JSON based approach and the test coverage was not high enough.
Besides it was fun to create something new, so Mockup was born.

There were concerns about having two projects with the same goal.
JC Brand took the initiative and brought the two projects back together.

Where Mockup had a dependency on [mockup-core](https://github.com/plone/mockup-core) with a base pattern to extend from, a configuration parser, pattern registry and Grunt infrastructure, this dependency was removed and replaced by a dependency on [patternslib](https://patternslib.com/).

Those projects led the foundation to the new way of developing JavaScript in Plone.

## Mockup Project Structure

This is how Mockup is structured on the filesystem:

```
mockup
├── bower.json               - Bower managed dependencies
├── Makefile                 - Makefile targets to bootstrap, build bundles
├── mockup                   - All the source in here (to be able to add to Python egg)
│   ├── bower_components     - External dependencies managed by Bower
│   ├── configure.zcml       - Registers Mockup resource directory
│   ├── Gruntfile.js         - Grunt build configuration. Extends js/grunt.js
│   ├── index.html           - Entry file for generated documentation
│   ├── js
│   │   ├── bundles          - Mockup bundle files
│   │   │   ├── docs.js
│   │   │   ├── plone.js
│   │   │   ├── widgets.js
│   │   │   └── ...
│   │   ├── config.js        - RequireJS configuration
│   │   ├── docs             - ReactJS based documentation framework
│   │   │   ├── app.js
│   │   │   └── ...
│   │   ├── grunt.js         - Grunt base configuration
│   │   ├── i18n.js
│   │   ├── i18n-wrapper.js
│   │   ├── router.js
│   │   ├── ui
│   │   │   ├── templates
│   │   │   │   └── popover.xml
│   │   │   └── views
│   │   │       ├── base.js
│   │   │       ├── buttongroup.js
│   │   │       └── ...
│   │   └── utils.js         - Utils to be reused
│   ├── less                 - Less files for bundles. Mostly import less files from
│   │   ├── base.less          a bundle's pattern dependencies.
│   │   ├── docs.less
│   │   ├── plone.less
│   │   ├── widgets.less
│   │   └── ...
│   ├── lib                                 - Non-Bower libraries
│   │   ├── jquery.event.drag.js
│   │   └── jquery.event.drop.js
│   ├── node_modules -> ../node_modules     - Grunt needs this link here...
│   ├── patterns                            - Patterns in here
│   │   ├── autotoc                         - The autodoc pattern
│   │   │   ├── pattern.autotoc.less        - Pattern specific Less file
│   │   │   └── pattern.js                  - Pattern itself
│   │   ├── livesearch
│   │   │   ├── pattern.js
│   │   │   └── pattern.livesearch.less
│   │   ├── select2
│   │   │   ├── pattern.js
│   │   │   └── pattern.select2.less
│   │   └── ...
│   └── tests                               - All tests in here
│       ├── config.js                       - RequireJS configuration for tests
│       ├── fakeserver.js                   - Fake test server
│       ├── files
│       │   ├── lessconfig.js
│       │   ├── mapper.html
│       │   └── r.js
│       ├── i18n-test.js
│       ├── images                          - Test resources
│       │   ├── extralarge.jpg
│       │   ├── large.jpg
│       │   └── ...
│       ├── json                            - Test data
│       │   ├── contextInfo.json
│       │   ├── fileTree.json
│       │   └── ...
│       ├── pattern-autotoc-test.js         - Tests for the autodoc pattern
│       ├── pattern-livesearch-test.js
│       ├── pattern-select2-test.js
│       └── ...
├── node_modules             - Node modules directory
├── package.json             - Node package metadata
├── provision.sh             - Vagrant provision file
├── setup.py                 - Mockup egg setup
└── Vagrantfile              - Vagrant configuration
```

## A Minimal Pattern

The following is a minimal pattern example, except that it uses [jQuery](https://jquery.com/) and changes some HTML elements' text.

```javascript
define([
  'pat-base',
  'jquery'
], function (Base, $) {
  'use strict';

  var Minimalpattern = Base.extend({
    name: 'minimalpattern',
    trigger: '.pat-minimalpattern',  // has to be exact like this: 'pat-' + patternname.
    defaults: {                      // default options
      text: 'Super Duper!'
    },
    init: function () {              // pattern initialization. called for each matching pattern.
      var self = this;
      self.$el.html(self.options.text);  // self.$el is the matching pattern element.
    }
  });
  return Minimalpattern;
});
```

For a complete example including tests, bundle config und Plone integration see:
<https://github.com/collective/mockup-minimalpattern>
