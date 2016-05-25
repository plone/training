Using the code for the training
===============================

We provide the code for this training divided into chapters.

The code-package
----------------

The package containing the eggs for each chapter is already automatically downloaded by buildout into a directory called ``src/ploneconf.site_sneak/``.

..  note::

    If you want to do it by hand do the following:

    .. code-block:: bash

        $ cd src
        $ git clone https://github.com/collective/ploneconf.site_sneak.git
        $ git checkout plone5


Copy the relevant chapter so that Plone can use it
--------------------------------------------------

To use the code for a certain chapter stop Plone and do this:

.. code-block:: bash

    $ cp -R src/ploneconf.site_sneak/chapters/<number_and_name_of_chapter>/ src/ploneconf.site
    $ ./bin/buildout
    $ ./bin/instance fg

This will:

* replace any existing previous chapter with the one you want to copy
* run buildout and restart Plone


Telling Plone about ploneconf.site
----------------------------------

If you did not yet do this (it is covered in chapter :ref:`eggs1-label`) you will have to
modify ``buildout.cfg`` to have Plone expect the egg ``ploneconf.site`` to be in ``src``.

.. code-block:: cfg
    :linenos:
    :emphasize-lines: 6, 12

    eggs =

    ...

    # our add-ons
        ploneconf.site
    #    starzel.votable_behavior

    ...

    [sources]
    ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site



These are the names of the folders for which there is code.
The corresponding folders with the code for Plone 5 have ``_p5`` appended::

    01_eggs1
    02_export_code
    03_zpt
    04_zpt_2
    05_views_2
    06_views_3
    07_behaviors_1
    08_viewlets_1
    09_dexterity_2
    10_events
    11_user_generated_content
    12_resources
    13_dexterity_3
    14_embed
