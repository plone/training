# Building the documentation locally

If you want to contribute to the training documentation or teach with a local version of the training documentation, here are the steps to take for a local setup.

## Dependencies and new build

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
cd docs
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
cd docs
make html
```

## Update existing

```bash
git pull
source bin/activate
make html
open _build/html/index.html
```

## Sync the browser while editing

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

## Technical set up to do before a training (as a trainer)

- Prepare a mailserver for the user registration mail (See {ref}`features-mailserver-label`)
- If you do only a part of the training (Advanced) prepare a database with the steps of the previous sections. Be aware that the file- and blobstorage in the Vagrant box is here: /home/vagrant/var/ (not at the buildout path /vagrant/buildout/)

## Upgrade the vagrant and buildout to a new Plone-version

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

If you are a trainer there is a special mini training about giving technical trainings. These chapters don't contain any Plone specific advice.
There's background, theory, check lists, and tips for anyone trying to teach technical subjects: {doc}`/teachers-training/index`


(about-contribute-label)=

## Contributing

Everyone is **very welcome** to contribute.
Minor bug fixes can be pushed directly in the [repository](https://github.com/plone/training),
bigger changes should be made as [pull-requests](https://github.com/plone/training/pulls/) and discussed previously in tickets.

Make sure you have filled out a [Contributor Agreement](https://plone.org/foundation/contributors-agreement).


(about-licence-label)=

## License

The Mastering Plone Training is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
