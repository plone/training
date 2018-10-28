==========================
Running the Content Import
==========================

In this section we will discuss:

  * How to run the import
  * Common errors you might hit during the import
  * Debugging and getting familiar with the exported data
  * Running the import multiple times
  * Writing tests


How to Run the Import
---------------------

First, get your exported data into the new buildout.
At the root of the buildout (the main `ploneconf.migration` folder),
create a folder called `content-import`.
The numbered folders from the export should go in here.
So the structure will look like this:

.. code-block:: console

   ploneconf.migration/
   ├── content-import
   │   ├── 0
   |       ├── 1.json
   |       ├── 2.json
   |       ├── 3.json
   |       ├── ...
   │   ├── 1
   │   ├── 2
   │   ├── 3

In your ploneconf.migration package, there are two ways provided to import the data:
* Import the migration's import profile
* Run a series of upgrade steps

The upgrade steps are available in case you need to run independent steps before or after the import.
A `run_migration` step is provided that does the same thing as importing the migration's import profile.

**Import Profile**

This is where you'll want to start.
No code needs to be written for this, it's already available in the migration package.

* Go to the ZMI > portal_quickinstaller, install `mysite.migration (default)`, if it is not already installed
* Then go to portal_setup > Import tab
* In the first dropdown, find `ploneconf.migration (import)`
* Click 'Import all steps'

If you are running the site in the foreground, you should see things happening now
(if not running in foreground mode, check the site logs).
Information is put into the log for each item that is imported.
You'll want to keep an eye on this to know when the import is done, or has run into an error.
See the 'Common Errors' section below if you have a problem.

When the import has successfully completed, you will see:
`INFO GenericSetup.collective.transmogrifier.genericsetup Transmogrifier pipeline ploneconf.import_content complete`
Check that your content was imported.

**Upgrade Steps**

With more complicated sites and imports,
you may find that additional steps need to be run before and/or after the import.
This can best be done with a series of import steps.
Open `mysite/migration/upgrades.py`.
There a three steps all ready for you to use or modify - 
a `pre_migration` step, the actual import step, and a `post_migration`.
The additional steps give you an opportunity to enable or disable bits of code during the migration.
The commented code provides an example for disabling a subscriber, then re-enabling it as the post-step.
A good use case for this is when importing forms - 
form products like PloneFormGen and EasyForm have subscribers to add some default fields to a new form folder.
You likely won't want this on forms that are being migrated, which already have the fields they need.

To run the import steps:

* Go to the ZMI > portal_quickinstaller, install `mysite.migration (default)`, if it is not already installed
* Then go to portal_setup > Upgrades tab
* Choose `mysite.migration (default)` from the dropdown
* You may need to click 'Show' to see the upgrade steps
* Check all the boxes, and click 'Upgrade'

If you are running the site in the foreground, you should see things happening now
(if not running in foreground mode, check the site logs).
Information is put into the log for each item that is imported.
You'll want to keep an eye on this to know when the import is done, or has run into an error.

Common Errors
-------------

When the import hits an error, it will bail on the import.
If you have PDBDebugMode or similar product installed, you'll get a PDB prompt to help with debugging.
You'll likely run into more errors once you start writing your own blueprints.

* `Exception: Path (content-import) does not exists.`
  * The code can't find your exported data.
    Make sure you have a folder at the root of the buildout called `content-import` with the export.
* `Module collective.jsonmigrator.blueprints.source_json, line 43, in __iter__`
  `ValueError: invalid literal for int() with base 10: 'x'`
  * The code is expecting folders within `content-import` to be numbered
* date set to 'None'
* `AttributeError: _setObject`
  * this happens when the import tries to add content where it's not allowed,
    like a non-folderish item, or a folder with limited content types (? - check)
* `ConstraintNotSatisfied: (u'en', 'language')`
  * Adjust the Language Control Panel in Site Setup to remove the country-specific variants
    and set English as the 'Site language' and 'Available language'.
    (need a better fix)

Debugging Other Errors
----------------------

Throughout the import process, you'll likely run into all sorts of random errors.
Here are some tips for debugging those errors.

1. Read the traceback.
   Some times the traceback does a good job of pointing you straight to the problem.
   Other times you'll find it's pointing at the `for item in self.previous:` in a blueprint.
   This is the trickier kind to debug, but you can...
2. Add a pdb.set_trace(). This can be done in the blueprints, or as part of the pipeline:

    [pdb]
    blueprint = collective.transmogrifier.sections.breakpoint
    condition = python:True

   The `condition` is required, so setting it to `python:True` will trigger a PDB every time.
   This can be changed if you know the exact item or type of item that is failing:

   condition = python:item['_type'] == 'Collection'

3. Find the offending item.
   This allows you to look at the raw data being imported,
   and is sometimes easier than working with the debugger to find the actual problem.
   Right before the traceback, you will see the output from the `logger` for the item being imported.
   You can grep through the entire export folder for the path output by the logger.
   Tip: Don't change the data in the export!
   Unless you know for sure that you will not be exporting the data again,
   it's best to fix the error in the import code.
4. Limit the items being imported.
   Once you've found the item throwing the error and work to fix it,
   you can make the one item the only thing you import!
   Move the entire export to a separate folder,
   and put the single item inside of a numbered folder.
   If you know of a few items that throw an error, you can import just those items.
   The file names of the imported items do not need to be sequential.
5. Test the full import after making your fix.
   If you are working with a large export, then testing a couple folders worth will work.
   You want to make sure your fix didn't break something else.

Running the import multiple times
---------------------------------

One nice thing about Transmogrifer is that you can run an import multiple times!
You don't have to delete imported items before running another import.
It is good to clear out data and run the full import occasionally, but it does not have to be every time.
When you pull a new export from the old site,
the content that gets imported will update the content in the new site.
Keep in mind there are some caveats to importing multiple times:
* Each time the import is run, the objects in Plone get updated whether there are changes or not.
  This will show up in the history of the item.
  This is not always a problem, but some people get picky about it.
* Items do not get deleted.
  If an item was deleted between exports, the import will not delete it.
  You will need to write some code to handle this case.
* Similarly, you will run into a problem if an item is deleted and recreated as a different content type.
  The import will not change the content type, but instead try to import all the other properties.
* If you plan to run the import multiple times, make sure any custom blueprints are expecting it.


Writing tests
-------------

Writing tests can save you a lot of time if you need to write lots of blueprints.
It can be very easy to break part of your import when writing a blueprint,
and tests will help you catch that.
Tests should be added for the general items you are importing,
plus a test for each type of item that throws an error, to make sure the error does not reoccur.