# README for converting reStructuredText to MyST

This document describes how to convert the entire repository from reStructuredText to MyST syntax.
This is a one-time operation.


## Prerequisites

-   You already have a working clone of this repository.
-   You have checked out this branch, `myst-rst2myst-conversion-process`, in your working clone to follow the instructions.
    You may build the docs and open the HTML output of these instructions in a browser window, or follow along and jump between `literalinclude` files.
-   In a sibling directory to this project's root, make a clean clone where you will perform the instructions.
    This allows you to make mistakes without messing up your current work and messing around with `git`.

    ```bash
    git clone https://github.com/plone/training.git myst
    ```
-   [Homebrew](https://brew.sh/).
-   `rsync`
    On macOS 10.15.7 and earlier, and possibly later versions, an old version of `rsync` hangs forever when using the `--dry-run` option under certain unknown conditions.
    Install the latest version of `rsync`.
  
    ```bash
    brew install rsync
    ```


## Installation

Start from the project root.
Create a new git branch in which to perform the conversion.

```bash
git checkout -b myst-convert-all
```

Open the file `mastering-plone/about_mastering.rst`.
Search for "Building the documentation locally" around line 202, and follow its instructions.

We use [RST-to-MyST](https://rst-to-myst.readthedocs.io/en/latest/index.html), a tool for converting reStructuredText to MyST Markdown.

```{note}
The package `rst-to-myst` is only needed once to convert the files.
Therefore it is not included in `requirements.txt`.
```

```bash
pip install "rst-to-myst[sphinx]"
```

## Conversion

Always perform a dry run before doing an actual run.
We must catch and resolve failures immediately, then fix them in the `.rst` source files.

```bash
rst2myst convert --dry-run --stop-on-fail --no-colon-fences \
index.rst \
about/**/*.rst \
advanced-python/**/*.rst \
angular/**/*.rst \
deployment/**/*.rst \
gatsby/**/*.rst \
javascript/**/*.rst \
mastering-plone/**/*.rst \
mastering-plone-5/**/*.rst \
plone_training_config/**/*.rst \
react/**/*.rst \
solr/**/*.rst \
teachers-training/**/*.rst \
testing/**/*.rst \
theming/**/*.rst \
transmogrifier/**/*.rst \
ttw/**/*.rst \
volto/**/*.rst \
voltoaddons/**/*.rst \
voltohandson/**/*.rst \
workflow/**/*.rst \
wsgi/**/*.rst
```

```{literalinclude} rst2myst-dryrun.txt
:language: text
```

Fix warnings in the `.rst` source files, and run the above command (or only a specific file that we want to fix) until no warnings appear.

Commit all fixes.

```bash
git commit -m "MyHelpfulCommitMessage"
```

```{danger}
STOP!
Do not proceed beyond this point until you commit fixes to the `.rst` source files.
If you do not save your changes now, you may potentially lose all your work in the next step.
```

Once we have cleaned up the source `.rst` files, we can run an actual conversion.

```bash
rst2myst convert --stop-on-fail --no-colon-fences \
index.rst \
about/**/*.rst \
advanced-python/**/*.rst \
angular/**/*.rst \
deployment/**/*.rst \
gatsby/**/*.rst \
javascript/**/*.rst \
mastering-plone/**/*.rst \
mastering-plone-5/**/*.rst \
plone_training_config/**/*.rst \
react/**/*.rst \
solr/**/*.rst \
teachers-training/**/*.rst \
testing/**/*.rst \
theming/**/*.rst \
transmogrifier/**/*.rst \
ttw/**/*.rst \
volto/**/*.rst \
voltoaddons/**/*.rst \
voltohandson/**/*.rst \
workflow/**/*.rst \
wsgi/**/*.rst
```

````{warning}
If you see any warnings, hard reset your git branch.
This will throw away any changes that were not committed to the repo.

```bash
git reset --hard HEAD
```

Now fix the `.rst` source files and commit those changes.
````

When you have no warnings, you may proceed to the next step.

## Run rsync shell script

Now that we have converted all the `.rst` files to `.md` files, we need to move the `.md` to a nested directory from the root of the project at `/rst2myst/training` and build the docs in that directory.

First run the dry-run version of the script.
Open the script and read it to see what it does.
It has prolific comments.

```bash
cd rst2myst
./rsync-training-dryrun.sh
```

If that looks good, then perform an actual rsync.

```bash
./rsync-training.sh
```

If some files do not get rsync-ed over to the nested directory, then delete the subdirectory, modify the relevant rsync include and exclude files, and run the script again. 

## Build docs in each directory

Now we can build and compare the docs between the two source directories to make sure that content renders correctly.

```bash
# Build the MyST docs in /rst2myst/training
cd training
make html
# Build the reST docs in /
cd ../..
make html
```

## Clean up

After you are satisfied with the conversion, let's do some clean up.

Remove all `.rst` files in root, except for `README.rst` and `CHANGES.rst`.

```bash
# From the project root directory
rm -r index.rst \
about/**/*.rst \
advanced-python/**/*.rst \
angular/**/*.rst \
deployment/**/*.rst \
gatsby/**/*.rst \
javascript/**/*.rst \
mastering-plone/**/*.rst \
mastering-plone-5/**/*.rst \
plone_training_config/**/*.rst \
react/**/*.rst \
solr/**/*.rst \
teachers-training/**/*.rst \
testing/**/*.rst \
theming/**/*.rst \
transmogrifier/**/*.rst \
ttw/**/*.rst \
volto/**/*.rst \
voltoaddons/**/*.rst \
voltohandson/**/*.rst \
workflow/**/*.rst \
wsgi/**/*.rst
```

Move all `.md` files to root using `rsync`.
First let's do a dry-run.

```bash
cd rst2myst
./rsync-md-reverse-dryrun.sh
```

If that looks good, then perform an actual rsync.

```bash
./rsync-md-reverse.sh
```

In `conf.py` remove `rst2myst/training/**` from `exclude_patterns`.

Uninstall `rst-to-myst`.

```bash
pip uninstall "rst-to-myst[sphinx]"
```

Delete the directory `rst2myst`.

Finally commit and push all the changes to GitHub, and create a pull request for review.
