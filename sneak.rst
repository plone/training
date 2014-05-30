Using the code for the training
===============================

Modify ``buildout.cfg`` to have Plone expect the egg ``ploneconf.site`` to be in ``src``.

.. code-block:: cfg
    :linenos:
    :emphasize-lines: 6, 12

    eggs =

    ...

    # our addons
        ploneconf.site
    #    starzel.votable_behavior

    ...

    [sources]
    ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site


Download the code into a directory called ``src/ploneconf.site_sneak``.

.. code-block:: bash

    $ cd src
    $ git clone https://github.com/starzel/ploneconf.site_sneak.git

To use the code for a certain chapter stop Plone and do this:

.. code-block:: bash

    $ cd src
    $ rm -rf ploneconf.site
    $ cp -R ploneconf.site_sneak/chapters/<number_and_name_of_chapter>/ ploneconf.site
    $ cd ../..
    $ ./bin/buildout
    $ ./bin/instance fg

This will

* remove the old code
* copy the code from a chapter
* run buildout and restart Plone

These are the chapters for which there is code::

    12_eggs1
    13_dexterity
    14_views_1
    16_zpt_2
    17_views_2
    18_views_3
    19_behaviors_1
    20_viewlets_1
    23_dexterity_2
    25_events
    26_user_generated_content
    27_ressources
    29_dexterity_3
    34_embed
