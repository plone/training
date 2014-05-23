Creating reusable packages with eggs
====================================

We already created an egg much earlier.

Now we are going to create a a feature that is completely independent of our ploneconf site and can be reused in other packages.

To make the distinction clear, this is not a package from the namespace :samp:`ploneconf` but from :samp:`starzel`.

We are going to add a voting behavior.

For this we need:

  * A behavior that stores it's data in annotations
  * A viewlet to present the votes
  * A bit of javascript
  * A bit of css
  * Some helper views so that the Javascript code can communicate with Plone

We move to the :file:`src` directory and call a script called :file:`zopeskel` from our projects bin-directory.

.. code-block:: bash

    $ mkdir src
    $ cd src
    $ ../bin/zopeskel

This returns a list of available templates we might use. We choose dexerity since it is pretty small but already has some of the right dependencies we need.

.. code-block:: bash

    $ ../bin/zopeskel dexterity

We answer some questions:

* Enter project name: ``starzel.votable_behavior``
* Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']: ``easy``
* Version (Version number for project) ['1.0']: ``1.0.0``
* Description (One-line description of the project) ['Example Dexterity Product']: ``Voting Behavior``
* Grok-Based? (True/False: Use grok conventions to simplify coding?) [True]: ``False``
* Use relations? (True/False: include support for relations?) [False]: ``False``


We have to modify the generated files slightly.

In :file:`setup.py`, we completely remove the variables setup_requires and paster_plugins. These are required for features that are rarely used and add a lot of code into the source directory that we don't want. To the :samp:`install_requires` list, we add an entry for :samp:`plone.api`.

The file :file:`tests.py` we just delete. This is an outdated test system and we don't want you to start from there.

The file :file:`profiles/default/types.xml` we just delete also. We won't define new types.


