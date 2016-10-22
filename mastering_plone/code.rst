Using the code for the training
===============================

You can get the complete code for this training in https://github.com/collective/ploneconf.site

The code-package
----------------

The package

..  note::

    If you want to do it by hand do the following:

    .. code-block:: bash

        cd src
        git clone https://github.com/collective/ploneconf.site.git


Getting the code for a certain chapter
--------------------------------------

To use the code for a certain chapter you need to checkout the appropriate tag for the chapter.
The package will then contain the complete code for that chapter (excluding exercises).
If you want to add the code for the chapter yourself you have to checkout the tag for the previous chapter.


Here is a example:

..  code-block:: bash

    git checkout views_2

The names of the tags are the same as the url of the chapter.
So the tag for the chapter https://training.plone.org/5/mastering_plone/registry.html is ``registry`` and you can get it with :command:`git checkout registry`.


Moving from chapter to chapter
------------------------------

To change the code to the state of the next chapter simply checkout the tag for the next chapter:

..  code-block:: bash

    git checkout views_3


If you made any changes to the code you have to get them out of the way first:

..  code-block:: bash

    git stash

This will stash away your changes but not delete them. You can get them back later.
You should learn about the command :command:`git stash` before you try reapply stashed changes.

If you want to remove any changes you made locally you can delete them with this command:

..  code-block:: bash

    git reset --hard HEAD





Telling Plone about ploneconf.site
----------------------------------

If you did not yet do this (it is covered in chapter :ref:`eggs1-label`) you will have to
modify :file:`buildout.cfg` to have Plone expect the egg :mod:`ploneconf.site` to be in :file:`src`.

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
    ploneconf.site = git https://github.com/collective/ploneconf.site.git



These are the tags for which there is code:

==============================    ===============================
Chapter                           Tag-Name
==============================    ===============================
:doc:`about_mastering`
:doc:`intro`
:doc:`installation`
:doc:`case`
:doc:`features`
:doc:`anatomy`
:doc:`plone5`
:doc:`configuring_customizing`
:doc:`theming`
:doc:`extending`
:doc:`add-ons`
:doc:`dexterity`
:doc:`buildout_1`                 ``buildout_1``
:doc:`eggs1`                      ``eggs1``
:doc:`export_code`                ``export_code``
:doc:`views_1`                    ``views_1``
:doc:`zpt`                        ``zpt``
:doc:`zpt_2`                      ``zpt_2``
:doc:`views_2`                    ``views_2``
:doc:`views_3`                    ``views_3``
:doc:`testing`                    ``testing``
:doc:`behaviors_1`                ``behaviors_1``
:doc:`viewlets_1`                 ``viewlets_1``
:doc:`api`
:doc:`ide`
:doc:`dexterity_2`                ``dexterity_2``
:doc:`custom_search`
:doc:`events`                     ``events``
:doc:`user_generated_content`     ``user_generated_content``
:doc:`resources`                  ``resources``
:doc:`thirdparty_behaviors`       ``thirdparty_behaviors``
:doc:`dexterity_3`                ``dexterity_3``
:doc:`relations`                  ``relations``
:doc:`registry`                   ``registry``
:doc:`frontpage`                  ``frontpage``
:doc:`eggs2`
:doc:`behaviors_2`
:doc:`viewlets_2`
:doc:`reusable`
:doc:`embed`
:doc:`deployment_code`
:doc:`deployment_sites`

==============================    ===============================
