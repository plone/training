Changelog
=========

This changelog is only very rough. For the full changelog please refer to https://github.com/plone/training/commits/master


- Scroll sidebar to active navigation element. @ksuess
- Enhance orientation: Add chapter title and training title in sticky top bar. @ksuess
- Enhance orientation: Add breadcrumbs to search results. @ksuess



1.2.5 (unreleased)
------------------

- Overhaul Mastering Plone Development [ksuess]

- Update Volto hands-on training with changes to during the last year [jackahl]

- Language tweaks to WSGI training [polyester]

- Minor fixes, like using implementer and provider decorators [jensens]

- Use behavior shortnames as best practice. [jensens]

- Refine misleading explanation of IFormFieldProvider [jensens]

- Tweaks to Mastering Plone testing page [tkimnguyen]

- Fix React and Volto bootstrapping information. [jensens]

- Fix a typo in Volto redux section and format according to style guide. [jensens]

- Fix AGX links. [jensens]

- Get rid of Grok, it is dead. No need any more to mention it here [jensens]

- Fix a bunch of errors and links-check failure popping up in ``make test`` [jensens]

- Fix Travis setup, use stages now. See #410. [jensens]

- Explanation about less variables and development/production mode in the theming training first chapter. [fredvd]

- Fixes to Advanced Python Training [oz123]

- Add one more chapter to Advanced Python Training [oz123]

- Updates and Fixes in the JavaScript training section [staeff]

- Reorder Javascript exercises [frapell]

- Add content of Advanced Python Training [oz123]

- Markup fixes and small edits [jean]

- different buildout invocation in vagrant setup
  [tschorr]

- Bring similar chapters into sync (ttw/mastering) [jean]

- Add missing Build step [jean]

- Fix some more Sphinx warnings [jean]

- Update to ttw-advanced-2 in theming training [jean]

- Update Mastering Plone Chapters for Ploneconf 2017 and use Plone 5.1rc1
  [pbauer]

- More formatting, markup and editing [jean]

- Update link [sgrepos]

- Add angular training
  [barbichu, fulv]

- Fix some IDs and filename references [jean]

- Update and restructure theming documentation.
  [tmassman, RobZoneNet]

- Fix some IDs and filename references [jean]

- Use correct links for ZCA itself and its usage in Pyramid, as well in
  translation files.
  [stevepiercy]

- Update Features training to reflect that Dexterity is now supported by Working Copy Support and Placeful Workflow.
  [robinsjm2]

- Fix a typo
  [staeff, b4oshany]

- Fix typos, improve wording
  [svx]

- Clarify which template we're editing
  [djowett]

- Fix typos
  [tkimnguyen]

- Fix Sphinx warnings emitted on clean build
  [stevepiercy]

- Update README.rst to refer to how to build the docs locally.
  [stevepiercy]

- Add CONTRIBUTING.md
  [stevepiercy]

- Move PloneConf 2016 to Previous Trainings
  [stevepiercy]

- Update JavaScript training with latest exercises and documentation using
  collective.jstraining
  [vangheem]

- Update theming training to reflect the changes in bobtemplates.plone and
  general cleanup, also add refs to ttw training, remove usage of resource
  registry for theming
  [MrTango]

- Add solr training
  [tomgross]

- Rearrange structure so Mastering Plone now lives in it's own folder.
  [pbauer]

- Fix directions which led to duplicate resourcess being delivered
  Closes https://github.com/plone/training/issues/174
  [davilima6]

- Plone Doc Style for Javascript part.
  [jensens]

- Add spell-checker, auto-build and travis-tests
  [svx]

- Use Plone 5 final and simplify vagrant-setup.
  [pbauer, fulv]

- Rewrite chapter on relations.
  [pbauer]

- Add a training on javasript.
  [frappel, thet]

- Add a training theming Plone 5.
  [MrTango, simahawk]

- A ton of fixes in the development-training in preparation to Ploneconf 2015 in
  Bucarest.
  [fulv]

- Update vagrant installation to include BIOS virtualization note.
  [lbrannon]

- Editing while reading. Edited Rapido chapter for language and formatting.
  [jean]

- Fix a couple of duplicate labels, unmatched literal ending, typo [jean]

- Fix code blocks that made Pygments lexer choke [jean]

- Fix some typos, clarify some examples [jean]

- Some exercises, draft of a new chapter on plone.restapi and some changes [tschorr]

- Exercises for behaviors_2, fix some emphasis [tschorr]

- Fix some typos, apply inline directives: file, Python domain, GUI, literals
  [jean]

- Add Plone 5 Workflow Training
  [calvinhp]

- Editing Dexterity chapters (typos, markup, some grammar) [jean]

- Fix reST lists [davisagli]

- Specify Python version for virtualenv using option, not command alias, as
  alias is not always present [jean]

- Fix duplicate labels [jean]

- Fix tests [gforcada]

- Review solr docs [gforcada]

- Add steps to Plone Deployment regarding images release on GitHub,
  and URL to visit locally deployed site  [danalvrz]

1.2.4 (2014-10-03)
------------------

- Revision of part one for Ploneconf 2014, Bristol
  [smcmahon]

- Revised for Ploneconf 2014, Bristol
  [pbauer, gomez]

- Add first exercises and create css+js for expanding/collapsing the solutions
  [pbauer]

- Fix local build with the rtd-Theme
  [pbauer]

- Add Spanish translation.
  [macagua]

- Add support for translations on transifex
  [macagua]

- Upgrade Vagrant setup to Ubuntu 18.04 LTS
  [tschorr]


1.2.3 (2014-07-11)
------------------

- Move sources to https://github.com/plone/training and render
  at https://plone-training.readthedocs.io/en/legacy/
  [pbauer]

- Integrate with docs.plone.org and papyrus
  [do3cc]

- Change license to https://creativecommons.org/licenses/by/4.0/
  [pbauer]

- Document how to contribute
  [pbauer]

- Update introduction
  [pbauer]

1.2.2 (2014-06-01)
------------------

- Fix all mistakes found during the training in May 2014
  [pbauer]

- Move rst-files to https://github.com/starzel/training
  [pbauer]

1.2.1 (2014-05-30)
------------------

- Publish verbose version on http://starzel.github.io/training/index.html
  [pbauer]

- Add bash-command to copy the code from ploneconf.site_sneak to ploneconf.site for each chapter
  [pbauer]

- include vagrant-setup as zip-file
  [pbauer]

- several small bug fixes
  [pbauer]


1.2 (2014-05-23)
----------------

- Heavily expanded and rewritten for a training in Mai 2014
  [pbauer, do3cc]

- remove grok
  [pbauer]

- use plone.app.contenttypes from the beginning
  [pbauer]

- use plone.api
  [pbauer]

- rewrite vagrant-setup
  [pbauer]

- drop use of plone.app.themeeditor
  [pbauer]

- add more chapters: Dexterity Types II: Growing up, User generated content, Programming Plone, Custom Search, Events, Using third-party behaviors, Dexterity Types III: Python, ...
  [pbauer, do3cc]


1.1 (October 2013)
------------------

- Revised and expanded for Ploneconf 2013, Brasilia
  [pbauer, do3cc]


1.0 (October, 2012)
-------------------

- First version under the title 'Mastering Plone' for Ploneconf 2012, Arnhem
  [pbauer, do3cc]


0.2 October 2011
----------------

- Expanded as Plone-Tutorial for PyCon De 2011, Leipzig
  [pbauer]

0.1 (October 2009)
------------------

- Initial parts created for the Plone-Einsteigerkurs (http://www.plone.de/trainings/einsteiger-kurs/kursuebersicht)
  [pbauer]
