===========================
Writing the Import Pipeline
===========================

In this section you will:

* Learn about the structure of the migration package
* Customize the pipeline for your site
* Write custom blueprints

Terminology
-----------

pipeline
  The pipeline is a `.cfg` file, so the syntax will be familiar if you regularly edit your buildout.cfg.
  This file details the steps that each exported item takes during the import.
  All steps are looped over for each item in the import.

blueprint
  Each step in the pipeline will specify a `blueprint`.
  This is a Python class that determines how to handle the data for that step.
  There are many blueprints already available in the Transmogrifier add-ons,
  or you may need to write some blueprints to handle your custom content.
  Blueprints are specified by `name`, which is set in the `configure.zcml`


Pipeline Details
----------------

Open the following file in your custom migration package: migration/import/import_content.cfg.
By default, it contains the basic parts needed to migrate your content from a jsonify export.
Unless your site is straight, out-of-the-box Plone and you want to migrate as-is, you'll likely need to customize this file.

First is the `[transmogrifer]` part which specifies the steps to run and their order.
**The order is very important!**
Each line corresponds to a part defined later in the file.
Comments can be added to this file with `#`

The most important pieces are `jsonsource`, `constructor`, and `schemaupdater`.

`jsonsource` specifies the local path to your exported content.
The path is relative to the root of the buildout.
If importing from a different type, such as CSV, there is the blueprint `transmogrify.dexterity.csvimport`.

The `constructor` creates an object in Plone for the current item in the import.
Any blueprints that manipulate the current `item` in the loop need to be in the pipeline before the `constructor`.
Once the object has been created in Plone, you can include blueprints after the `constructor` that manipulate that new object in Plone.

Then the `schemaupdater` migrates all the field and property content from the export to the new Plone object.

The other steps in the blueprint are included because they will likely be needed, but also to serve as examples.
Some steps only need to specify the `blueprint`, while others may require some additional parameters.
You can dig into the blueprint code to get a hint of what parameters might be required.

pathfixer
  The blueprint specified here is `plone.app.transmogrifier.pathfixer`.
  When you open that file, you'll see the `PathFixer` class:

    class PathFixer(object):
        """Changes the start of the path.
        """
        classProvides(ISectionBlueprint)
        implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        """
        :param options['path-key']: The key, under the path can be found in
                                  the item.
        :param options['stripstring']: A string to strip from the beginning of
                                     the path.
        :param options['prependstring']: A string to prepend on the beginning
                                       of the path.
        """

  This is useful for modifying and manipulating the start of each item's path, mainly used for the Plone site name.
  Items exported with jsonify include the Plone site name in the path.
  You'll likely want to remove this so that all items are imported at the root of the site, instead of an extra level down.
  It is also helpful if you want to move content to be in a different folder.

example
  This is provided solely as an example to give you a starting point for making your own blueprint.
  It is currently commented out in the top `[transmogrifier]` section, so it will not run until uncommented.
  The blueprint name, `mysite.example` is defined in the configure.zcml, where it points to the Python Class.
  We'll cover more about the blueprint itself later.

copyuid
  This part uses the `manipulator` blueprint, which allows you to copy a key from the item to the Plone object using a :term:`TALES` expression.
  The `copyuid` part is needed for the `schemaupdater` to properly set the item's UUID.

deserializer
  If the data was contained inside of an attached JSON file, stuff that data back into the pipeline for the next step.

logger
  You get the option to output a line to the log for each item imported in the site.
  The `name` is prepended on to each log message.
  `level` determines the log level.
  You can even have multiple loggers set to different levels, which might provide different output per environment.
  The provided sample will log the `_path` for each imported item.
  Note that this logger is one of the final steps, so the item appears in the log after the item was successfully imported.
  For debugging, it can be helpful to move the logger to the top, so you know which item you need to check when an error is thrown.

savepoint
  For large sites, you may have thousands of items being imported, and it can be a pain to start over when you hit an error.
  The example `savepoint` will commit after every 1000 items.
  This is set to 1000, because a jsonify export saves 1000 items to a folder.
  This will be discussed more later in <import>.