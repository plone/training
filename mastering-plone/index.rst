.. _mastering_plone-label:

=============================
Mastering Plone 6 Development
=============================

`Mastering Plone Development` is intended as a training to learn proven practices of Plone development.

It's both, an online course and a sketch for an on the spot training.

The story of a conference platform provides a week-long training of several development topics that can be split in two trainings:

- A beginner training (2 to 3 days) that covers the essentials of Plone and Plone Volto.
- An advanced training (3 to 5 days) that covers advanced topics.

..  warning::

    This is the Mastering Plone 6 Training.

    The biggest change from `Mastering Plone 5 <https://training.plone.org/5/mastering-plone-5/>`_ is that Mastering Plone 6 teaches developing for the React-based frontend Volto as well as for Plone Classic i.e. using server-side rendered templates.
    In many chapters that use Volto there is a link to a chapter that covers the same tasks in Plone Classic, and vice versa.

    Plone 6 is not yet released and thus the training is a work in-progress and there are still some rough edges.


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
    * :doc:`viewlets_advanced_classic` (replaced by :doc:`volto_components_sponsors`)
    * :doc:`theming` (replaced by :doc:`volto_theming`)


..  toctree::
    :maxdepth: 2
    :numbered:
    :caption: Mastering Plone 6

    about_mastering
    intro
    case
    what_is_plone
    installation
    ../plone_training_config/instructions.rst
    features
    anatomy
    plone_versions
    volto_basics
    configuring_customizing
    volto_overrides
    volto_semantic_ui
    volto_theming
    extending
    add-ons
    buildout_1
    eggs1
    dexterity
    dexterity_2_talk
    dexterity_reference
    volto_talkview
    behaviors_1
    volto_frontpage
    volto_talk_listview
    api
    ide
    custom_search
    events
    upgrade_steps
    volto_testing
    user_generated_content
    thirdparty_behaviors
    dexterity_3
    volto_components_sponsors
    volto_addon
    volto_richtexteditor
    volto_custom_block
    volto_custom_addon
    volto_custom_addon2
    relations
    registry
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
