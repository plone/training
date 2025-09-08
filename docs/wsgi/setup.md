---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(setup-label)=

# Setup a box for the training

## Installing Prerequisites

Please follow the instructions given [here](https://2022.training.plone.org/plone_training_config/instructions_plone5.html) to install a Ubuntu 18.04 box for this training.
This training is about deploying Plone, so we will not need the Plone instance provided by these instructions.
If you follow the section on how to [Installing Plone without vagrant](https://2022.training.plone.org/plone_training_config/instructions_plone5.html#installing-plone-without-vagrant), you can therefore stop following the instructions where it reads "Set up Plone for the training like this if you use your own OS (Linux or Mac)".
If instead you have chosen to [Install Plone with Vagrant](https://2022.training.plone.org/plone_training_config/instructions_plone5.html#installing-plone-with-vagrant), you can comment out the `# install plone` section in the `Vagrantfile`:

```{code-block} bash
:emphasize-lines: 9-12

  ...
  # Create a Putty-style keyfile for Windows users
  config.vm.provision :shell do |shell|
      shell.path = "manifests/host_setup.sh"
      shell.args = RUBY_PLATFORM
  end

  # install plone
  #config.vm.provision :puppet do |puppet|
  #    puppet.manifests_path = "manifests"
  #    puppet.manifest_file  = "plone.pp"
  #end


end
```

It is not a problem if you followed the instructions and ended up having a Plone instance.
The Plone instance(s) we create throughout the training will go to a different location, just keep in mind you will not be able to run both instances at the same time because of conflicting ports.

## Creating a Virtualenv for the Training

Next you need to get the training buildout and create a Python virtualenv for the training in a suitable location.
In the vagrant this is the `/vagrant` directory:

```shell
$ cd /vagrant
```

In a native environment, choose whatever location you think is appropriate.

Then in this directory we need to get the training buildout and create a virtualenv:

```shell
$ git clone https://github.com/collective/wsgitraining_buildout.git wsgitraining
$ cd wsgitraining
$ python3.7 -m venv .
$ . bin/activate
(wsgitraining) $ pip install -U pip # upgrade pip to the latest version
```
