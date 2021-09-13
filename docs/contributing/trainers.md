---
html_meta:
  "description": "Using the documentation for a training"
  "keywords": "Plone, Trainings"
---

(contributing-trainers-label)=

# Using the documentation for a training

Feel free to organize a training yourself.
Please be so kind to contribute any bug fixes or enhancements you made to the documentation for your training.

Trainers should read {doc}`setup-build` and the trainings in {doc}`/plone_training_config/instructions` and {doc}`/teachers-training/index`.
These documents help trainers prepare for a successful training experience.


## Technical set up to do before a training (as a trainer)

```{important}
Much of this section is duplicated in {file}`/mastering-plone/about_mastering.md` and {file}`/mastering-plone-5/about_mastering.md`.
We should purge duplicitous content, and use references to a primary source.
```

- Prepare a mail server for the user registration mail (See {ref}`features-mailserver-label`)
- If you do only a part of the training (Advanced), prepare a database with the steps of the previous sections. Be aware that the file and blobstorage in the Vagrant box is at `/home/vagrant/var/` and not at the buildout path `/vagrant/buildout/`.

## Upgrade the vagrant and buildout to a new Plone-version

```{important}
Much of this section is duplicated in {file}`/mastering-plone/about_mastering.md` and {file}`/mastering-plone-5/about_mastering.md`.
We should purge duplicitous content, and use references to a primary source.
```


- In <https://github.com/collective/training_buildout> change [buildout.cfg](https://github.com/collective/training_buildout/blob/master/buildout.cfg) to extend from the new `versions.cfg` on <https://dist.plone.org/release>.
- Check if we should to update any versions in <https://github.com/collective/training_buildout/blob/master/versions.cfg>.
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

{doc}`/teachers-training/index`
