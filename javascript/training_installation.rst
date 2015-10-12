Installing Plone and example packages for the Training
======================================================

To get Plone and example packages for this training installed, please follow the installation instructions at :doc:`/plone_training_config/instructions`.

After that, issue the following command to get the development environment for the ``mockup-minimalpattern`` example package installed::

    make mockup-minimalpattern

.. note::

    To be able to install the JavaScript development tools, you need `NodeJS <https://nodejs.org/en/download/>`_ installed on your development computer.


Installing Mockup
-----------------

Optionally you can install Mockup. Mockup is already included in the `training_buildout <https://github.com/collective/training_buildout/blob/plone5/buildout.cfg>`_. Uncomment the "mockup" line in ``auto-checkout`` and buildout ``eggs`` section.

After that, run buildout:

.. code-block:: bash

    $ bin/buildout -N

.. warning::

    If you are running buildout inside vagrant, always remember to use the vagrant.cfg ``bin/buildout -Nc vagrant.cfg``

