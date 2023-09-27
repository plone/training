---
myst:
  html_meta:
    "description": "Set up your project and development environment"
    "property=og:description": "Set up your project and development environment"
    "property=og:title": "Initial project setup"
    "keywords": "Plone, Volto, Training, Setup, Docker"
---

(voltohandson-quickstart-label)=

# Quick Start

## Set Up Volto Project

To create our first volto project we will install the volto generator tool (https://www.npmjs.com/package/@plone/generator-volto) using `npm install -g yo @plone/generator-volto`. When installed you can use it to generate a brand new volto project:

```shell
yo @plone/volto
```
The dialogue in the console will ask you first to prompt a name for your project. When choosing an apropriate name, please note that due to a current bug your name should not begin with a number. After you have given a name to your project, you will be a wether you want to install any addons. You can skip by pressing the `enter` button, as we dont want to use any 3rd party addons for the training.

```{hint}
In case you want to install any addons you can find a curated list of addons of all different sorts here: https://github.com/collective/awesome-volto
```

After the bootstrapping process is done cd into the newly created project folder and install all necessary dependencies by running `yarn`.

With the initial project and dependencies set up now, you could already start adding your first customzations, but it is recommended to set up your own policy addon to contain all your customizations and additions. To do that create a new addon in the project folder by running:

```shell
yo @plone/volto:addon
```

When prompted to add a name to your addon, just hit enter and your current projects name will be used as name for the addon as well. This will create a new folder with your projects name within the `src/addons` directory. Finally to get you project readily configured run `make develop` to get the configuration inside of `jsconfig` and `mrs.developer.json` updated to use our new policy addon.

## Folder structure

Within your `src` folder of your project you will find the following subfolders:

- actions
- components
- constants
- customizations
- helpers
- reducers

As we want to work within our policy addon instead of directly within our initial project we will have to recreate some of these inside of our addon during the course of this training. Your folder structure inside your projects src directory now should look something like this:

```{image} _static/initial_folder_structure.png
:align: center
:alt: initial folder structure with new addon inside addons folder
```


## Build environments

We need to build two environments.
Start two terminal sessions, one for each environment, Plone and Yarn, and a third session to issue git and other shell commands.
In each terminal session you should be in your project folder `volto-training` or whatever you named your project.

### Plone environment

To run our Volto site, we will use the latest Plone 6 backend Docker image.
You can start it by running the following command:

```shell
docker run -p 8080:8080 -e SITE=Plone plone/plone-backend
```

Keep that process running during the whole training in one of your terminal windows because the container does not have a persistant storage. So once you stop that container again some of you work might get lost again.

```{note}
If you already have expierience setting up Plone instances you can also use a Plone Classic Plone instance with the addons "Plone 6 Frontend (plone.volto)" and "plone.restapi" installed.
```

```{seealso}
An alternate way to set up a complete Plone 6 Project including both frontend and backend setup is using Plone cookiecutter: https://github.com/collective/cookiecutter-plone-starter
```
### Yarn environment

You can now start up your Volto instance by running the following command:

```shell
yarn start
```

## Volto source code

When developing Volto you will find yourself looking quite often at the Volto source code to see how things are done, the code syntax, and how to clone or override components.
For convenience, a symlink to a copy of the Volto code is set up inside `node_modules` when you run `yarn` in your Volto project folder.
You will find this copy of Volto in the `omelette` folder. In some cases this folder will not appear, if you filesystem does not support symlinks.

## Recommended plugins

No matter which integrated development environment (IDE) you use, you should also install these plugins for a better workflow:

- Prettier
- ESlint
- prettier-stylelint (for VSCode)
