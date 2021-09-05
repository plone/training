(about-use-label)=

## Using the documentation for a training

Feel free to organize a training yourself.
Please be so kind to contribute any bug fixes or enhancements you made to the documentation for your training.

The training is rendered using Sphinx and builds in two flavors:

default
  The verbose version used for the online documentation and for the trainer.
  Build it in Sphinx with `make html` or use the online version.

presentation
  An abbreviated version used for the projector during a training.
  It should use more bullet points than verbose text.
  Build it in Sphinx with `make presentation`.

:::{note}
By prefixing an indented block of text or code with `.. only:: presentation` you can control
that this block is used for the presentation version only.

To hide a block from the presentation version use `.. only:: not presentation`

Content without a prefix will be included in both versions.
:::


### Exercises and Solutions

Collapsed solutions of exercises:

````{admonition} Complete code of the component Sed posuere consectetur est at lobortis.
:class: toggle

```{code-block} jsx
:linenos:
:emphasize-lines: 2,4

import React from 'react';
import { defineMessages, injectIntl } from 'react-intl';
import { v4 as uuid } from 'uuid';
import { omit, without } from 'lodash';
```
````

Be aware of the nested directives! Increase back ticks!

    ````{admonition} Complete code of the component
    :class: toggle

    ```{code-block} jsx
    :linenos:
    :emphasize-lines: 2,4

    import React from 'react';
    import { defineMessages, injectIntl } from 'react-intl';
    import { v4 as uuid } from 'uuid';
    import { omit, without } from 'lodash';
    ```
    ````


## Building the documentation locally

### Dependencies and new build

Please make sure that you have [Enchant](https://abiword.github.io/enchant/) installed. This is needed for spell-checking.

Install Enchant on macOS:

```console
brew install enchant
```

Install Enchant on Ubuntu:

```console
sudo apt-get install enchant
```

To build the documentation follow these steps:

```console
git clone https://github.com/plone/training.git
cd training
python -m venv .
source bin/activate
```

Now install dependencies and build.

```console
pip install -r requirements.txt
make html
```

You can now open the output `_build/html/index.html` in your browser.

To build the presentation version use `make presentation` instead of `make html`. You can open the presentation at `_build/presentation/index.html`.

If you use macOS you can do:

```console
open _build/html/index.html
```

In the case of Linux, Ubuntu for example you can do:

```console
firefox _build/html/index.html
```

or with Chrome

```console
google-chrome _build/html/index.html
```

**All steps in short**

```console
git clone https://github.com/plone/training.git
cd training
python -m venv .
source bin/activate
pip install -r requirements.txt
make html
```

### Update existing

```bash
git pull
source bin/activate
make html
open _build/html/index.html
```

### Sync the browser while editing

To watch the changes in browser while editing you can use gulp.

Install once the gulp command line utility.

```bash
npm install --global gulp-cli
```

Install once the gulp project with

```bash
npm install
```

Run gulp when starting working on the training with

```bash
gulp
```

and see a browser window opening on <http://localhost:3002/>.

### Technical set up to do before a training (as a trainer)

- Prepare a mailserver for the user registration mail (See {ref}`features-mailserver-label`)
- If you do only a part of the training (Advanced) prepare a database with the steps of the previous sections. Be aware that the file- and blobstorage in the Vagrant box is here: /home/vagrant/var/ (not at the buildout path /vagrant/buildout/)

### Upgrade the vagrant and buildout to a new Plone-version

- In <https://github.com/collective/training_buildout> change [buildout.cfg](https://github.com/collective/training_buildout/blob/master/buildout.cfg) to extend from the new `versions.cfg` on <http://dist.plone.org/release>
- Check if we should to update any versions in <https://github.com/collective/training_buildout/blob/master/versions.cfg>
- Commit and push the changes to the training_buildout
- Modify the vagrant-setup by modifying {file}`plone_training_config/manifests/plone.pp`. Set the new Plone-version as `$plone_version` in line 3.
- Test the vagrant-setup it by creating a new vagrant-box using the new config.
- Create a new zip-file of all files in `plone_training_config` and move it to `_static`:

```console
cd plone_training_config
zip -r ../_static/plone_training_config.zip *
```

- Commit and push the changes to <https://github.com/plone/training>

## Train the trainer

If you are a trainer there is a special mini training about giving technical trainings.
We really want this material to be used, re-used, expanded, and improved by Plone trainers world wide.

These chapters don't contain any Plone specific advice.
There's background, theory, check lists, and tips for anyone trying to teach technical subjects.

{doc}`/about/teachers-training/index`

(about-contribute-label)=

## Contributing

Everyone is **very welcome** to contribute.
Minor bug fixes can be pushed directly in the [repository](https://github.com/plone/training),
bigger changes should made as [pull-requests](https://github.com/plone/training/pulls/) and discussed previously in tickets.

(about-licence-label)=

## License

The Mastering Plone Training is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

Make sure you have filled out a [Contributor Agreement](https://plone.org/foundation/contributors-agreement).

If you haven't filled out a Contributor Agreement, you can still contribute.
Contact the Documentation team, for instance via the [mailinglist](https://sourceforge.net/p/plone/mailman/plone-docs/)
or directly send a mail to <mailto:plone-docs@lists.sourceforge.net>

Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons.

You can also add in a comment with your pull request "I, \<full name>, agree to have this published under Creative Commons 4.0 International BY".
