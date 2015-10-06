Scratchpad
==========

Scratchpat for text snippets to be included somewhere else in the training.


General advises
---------------

.. note::

    When providing static resources (JS/LESS/CSS) for Plone 5's resource
    registry, use ``plone.resource`` based resources instead of Zope's browser
    resources. The latter are cached heavily and you won't get your changes
    build with zope resources.

.. note::

    A bundle can depend on another. This is mainly used for the order of
    inclusion in the rendered content. Currently, it doesn't hook in the
    require js dependency mechanism. This means, each bundle gets all their
    dependencies compiled in, which raise the response paiload unnecessarily.
    To avoid this, add your resources to existing bundles, like the "plone"
    bundle.

.. note::

    The mockup grunt infrastructure is build with a convention over
    configuration approach in mind. It's actually very picky about a lot of
    things: locations of your bundle files, location of your bundle less files,
    location of your pattern js and less files and the require js ids of those.
    Bundles have to be named "mockup-bundles-BUNDLENAME", patterns have to be
    named "mockup-patterns-PATTERNNAME".



Structure
---------


About this training
    Training Agenda
        DAY1
            Framework Tools
            Create Mockup Pattern
            Integrate Other (Non-Mockup based) Javascript
        DAY2
            Practicing

Preparing for the training
    About Javascript, Mockup, Patternslib and Plone 5
        History of everything, What's what.

Installation Mockup


Development environment
    Javascript and editor support
    Code Linter
    Grunt
    Bower
    Testing

Whirlwind tour through Mockup, Patternslib and Javascript in Plone 5
    Short explanation of the code tree / main modules:
    Mockup
    Patternslib
    Plone 5

Developing a Pattern
    A Barebone Pattern
        Based on collective.minimalpattern

        Pattern explained

    Adding a bower.json dependency

    Testing the Pattern


Integrating the Pattern
    Integration in Plone 5
    Integration in Plone 4
    Integration in Mockup w/out Plone


No-Pattern Javascript in Plone

    The require JS way

    The old, require JS-less way


Using other Frameworks in Plone

    Angular JS
    React JS


Comparison to other frameworks

    Patternslib and Web Components
    Patternslib and React Components
    Patternslib and Angular JS directives
    Plone and ES 6


