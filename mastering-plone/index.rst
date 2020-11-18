.. _mastering_plone-label:

===========================
Mastering Plone Development
===========================

`Mastering Plone Development` is intended as a training to learn proven practices of Plone development.

It's both, an online course and a sketch for an on the spot training.

The story of a conference platform provides a week-long training of several development topics that can be split in two trainings:

- A beginner training (2 to 3 days) that covers the essentials of Plone and Plone Volto.
- An advanced training (3 to 5 days) that covers advanced topics.

.. todo::

    These chapters are outdated and need to be updated:

    * :doc:`views_1`: We still need browser views with Volto but there needs to be good example why and where?
    * :doc:`registry`: Create a controlpanel in Volto.
    * :doc:`frontpage`: Move to a earlier place and build frontpage using the blocks. Should include a listing of features content from :doc:`behaviors_1`

    These chapters teach developing with classing Plone without Volto (i.e. server-side rendering):

    * :doc:`zpt` (replaced by :doc:`volto_semantic_ui`)
    * :doc:`zpt_2` (needs a new chapter on overriding components)
    * :doc:`views_2` (replaced by :doc:`volto_talkview`)
    * :doc:`views_3` (replaced by :doc:`volto_talk_listview`)
    * :doc:`viewlets_1` (replaced by a new chapter)
    * :doc:`events_classic` (replaced by :doc:`events`)
    * :doc:`viewlets_advanced_classic` (replaced by :doc:`viewlets_advanced_classic`)
    * :doc:`theming` (replaced by :doc:`volto_theming`)


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
    extending
    add-ons
    buildout_1
    eggs1
    dexterity
    dexterity_2_talk
    dexterity_reference
    behaviors_1
    api
    volto_testing
    ide
    dexterity_2
    custom_search
    events
    volto_overrides
    volto_semantic_ui
    volto_theming
    volto_talkview
    volto_talk_listview
    user_generated_content
    thirdparty_behaviors
    dexterity_3
    volto_components_sponsors
    volto_richtexteditor
    volto_custom_block
    volto_addon
    volto_custom_addon
    relations
    registry
    frontpage
    volto_frontpage
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
