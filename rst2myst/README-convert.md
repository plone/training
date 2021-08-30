# README for converting reStructuredText to MyST

This document describes how to convert the entire repository from reStructuredText to MyST syntax.
This is a one-time operation.
After completion, this file may be deleted from the repository.


## Installation

Start from the project root.
Create a new git branch in which to perform the conversion.

:::{code-block}bash
git checkout -b myst-convert-all
:::

Open the file `mastering-plone/about_mastering.rst`.
Search for "Building the documentation locally" around line 202, and follow its instructions.

We use [RST-to-MyST](https://rst-to-myst.readthedocs.io/en/latest/index.html), a tool for converting reStructuredText to MyST Markdown.

:::{note}
The package `rst-to-myst` is only needed once to convert the files.
Therefore it is not included in `requirements.txt`.
:::

:::bash
pip install "rst-to-myst[sphinx]"
:::

## Conversion

Always perform a dry run before doing an actual run.
We must catch and resolve failures immediately, then fix them in the `.rst` source files.

:::bash
rst2myst convert --dry-run --stop-on-fail \
index.rst \
about/*.rst \
advanced-python/*.rst \
angular/*.rst \
deployment/*.rst \
gatsby/*.rst \
javascript/*.rst \
mastering-plone/*.rst \
mastering-plone-5/*.rst \
plone_training_config/*.rst \
react/*.rst \
solr/*.rst \
teachers-training/*.rst \
testing/*.rst \
theming/*.rst \
transmogrifier/*.rst \
ttw/*.rst \
volto/*.rst \
voltoaddons/*.rst \
voltohandson/*.rst \
workflow/*.rst \
wsgi/*.rst
:::

:::{literalinclude} rst2myst-dryrun.txt
:language: text
:::

Fix warnings in the `.rst` source files, and run the above command (or only a specific file that we want to fix) until no warnings appear.

Commit all fixes.

:::{code-block}bash
git commit -m "MyHelpfulCommitMessage"
:::

:::{danger}
STOP!
Do not proceed beyond this point until you commit fixes to the `.rst` source files.
If you do not save your changes now, you may potentially lose all your work in the next step.
:::

Once we have cleaned up the source `.rst` files, we can run an actual conversion.

:::bash
rst2myst convert --stop-on-fail \
index.rst \
about/*.rst \
advanced-python/*.rst \
angular/*.rst \
deployment/*.rst \
gatsby/*.rst \
javascript/*.rst \
mastering-plone/*.rst \
mastering-plone-5/*.rst \
plone_training_config/*.rst \
react/*.rst \
solr/*.rst \
teachers-training/*.rst \
testing/*.rst \
theming/*.rst \
transmogrifier/*.rst \
ttw/*.rst \
volto/*.rst \
voltoaddons/*.rst \
voltohandson/*.rst \
workflow/*.rst \
wsgi/*.rst
:::

::::{warning}
If you see any warnings, hard reset your git branch.
This will throw away any changes that were not committed to the repo.

:::{code-block}bash
git reset --hard HEAD
:::

Now fix the `.rst` source files and commit those changes.
::::

When you have no warnings, you may proceed to the next step.

## Run rsync shell script

Now that we have converted all the `.rst` files to `.md` files, we need to move the `.md` to a nested directory from the root of the project at `/rst2myst/training` and build the docs in that directory.

First run the dry-run version of the script.
Open the script and read it to see what it does.
It has prolific comments.

:::{code-block}bash
cd rst2myst
./rsync-training-dryrun.sh
:::

If that looks good, then perform an actual rsync.

:::{code-block}bash
cd rst2myst
./rsync-training.sh
:::

If some files do not get rsync-ed over to the nested directory, then delete the subdirectory, modify the relevant rsync include and exclude files, and run the script again. 

## Build docs in each directory

Now we can build and compare the docs between the two source directories to make sure that content renders correctly.

:::{code-block}bash
# Build the MyST docs
cd training
make html
# Build the reST docs
cd ../..
make html
:::

## Clean up

After you are satisfied with the conversion, you may uninstall `rst-to-myst`.

:::bash
pip uninstall "rst-to-myst[sphinx]"
:::

Delete the directory `rst2myst`.
