Development Environment
=======================

This document assumes you already have Plone up and running. If you don't, please refer to :doc:`/plone_training_config/instructions`.

We are also going to be using an already created package with some boiler plate (:doc:`More info </sneak>`)

Copy over the ``20_javascript_p5`` folder

.. code-block:: bash

    $ cp -R src/ploneconf.site_sneak/chapters/20_javascript_p5/ src/ploneconf.site

Modify your buildout.cfg so Plone can find it

.. code-block:: cfg
    :linenos:
    :emphasize-lines: 5, 9, 13

    [buildout]
    ...
    auto-checkout =
    ...
        ploneconf.site
    ...
    eggs =
    ...
        ploneconf.site
    ...

    [sources]
    ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site

Run buildout

.. code-block:: bash

    $ bin/buildout -N

.. warning::

    If you are running buildout inside vagrant, always remember to use the vagrant.cfg ``bin/buildout -Nc vagrant.cfg``

