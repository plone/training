.. _mastering_plone-label:

===========================
Mastering Plone Development
===========================

This is the documentation for the "Mastering Plone" training.

Mastering Plone is intended as a week-long training for people who are new to Plone or want to learn about the current best practices of Plone development. It can be split in two trainings:

- A beginner training (2 to 3 days) that covers chapters 1-18.
- An advanced training (3 to 5 days) that covers the rest.

At conferences a shortened 2-day version of the advanced training with a slightly modified order is held.

.. todo::

    These chapters are outdated and will probably be removed:

    * :doc:`export_code` (replaced by creating talk as a python schema)

    These chapters are outdated and need to be updated:

    * :doc:`views_1`: We still need browser views with Volto but there needs to be good example why and where?
    * :doc:`testing`: Add information about writeing tests for Volto. Link to new testing training: https://training.plone.org/5/testing/
    * :doc:`dexterity_2`: Shorten to only cover GS and upgrade-steps. Marker interface/behavior is no longer needed with a python talk schema \o/
    * :doc:`frontpage`: Move to a earlier place and build frontpage using the blocks. Should include a listing of features content from :doc:`behaviors_1`

    These chapters teach developing with classing Plone without Volto (i.e. server-side rendering):

    * :doc:`zpt` (replaced by :doc:`volto_semantic_ui`)
    * :doc:`zpt_2` (needs a new chapter on overriding components)
    * :doc:`views_2` (replaced by :doc:`volto_talkview`)
    * :doc:`views_3` (replaced by :doc:`volto_talk_listview`)
    * :doc:`viewlets_1` (replaced by a new chapter)
    * :doc:`events_classic` (replaced by :doc:`events`)
    * :doc:`viewlets_advanced_classic` (replaced by :doc:`viewlets_advanced_classic`)


..  toctree::
    :maxdepth: 2
    :numbered:
    :caption: Mastering Plone

    about_mastering
    intro
    case
    what_is_plone
    installation
    ../plone_training_config/instructions.rst
    features
    anatomy
    plone5
    volto_basics
    configuring_customizing
    theming
    extending
    add-ons
    buildout_1
    eggs1
    dexterity
    dexterity_2_talk
    dexterity_reference
    volto_semantic_ui
    volto_overrides
    volto_talkview
    volto_talk_listview
    behaviors_1
    viewlets_1
    api
    testing
    ide
    dexterity_2
    custom_search
    events
    user_generated_content
    resources
    thirdparty_behaviors
    dexterity_3
    volto_components_sponsors
    relations
    registry
    frontpage
    eggs2
    behaviors_2
    viewlets_2
    reusable
    embed
    deployment_code
    deployment_sites
    restapi
    future_of_plone
    optional


Please note that this document is *not complete* without the spoken word of a trainer.

We attempt to include the most important parts of what we teach in the training. But reading it here can not be considered equal to attending a training.

.. The following items are hidden in this toctree to prevent Sphinx warnings. They might be used by trainers only, or for historical purposes.

..  toctree::
    :hidden:

    code
    timing
