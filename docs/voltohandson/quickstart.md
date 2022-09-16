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

To create our first volto project we will youse the volto generator tool. First create a folder in which your project will be located.You can call it whatever your projectname shall be. In our case we will use `volto-hands-on-training`. Inside that directory run:

```
npm init yo @plone/volto
```

The dialogue in the console will ask you for the name of your project and wether you want to install any addons. You can skip both by pressing the `enter` button, as we will use the default name and dont want to use any addons for the training.

```{image} _static/volto_generator_terminal.png
:align: center
:alt: Console with Volto generator dialogue
```

## Build environments

We need to build two environments.
Start two terminal sessions, one for each environment, Plone and Yarn, and a third session to issue git and other shell commands.
In each terminal session you should be in your project folder `volto-hands-on-training`.

### Plone environment

To run our Volto site, we will use the Plone 6 Docker image.
You can start it by running the following command:

```shell
docker run -p 8080:8080 plone/plone-backend:6.0.0a1
```

Keep that process running during the whole training in one of your terminal windows.

Before we can begin, you need to create a new Plone instance with the required add-ons installed.
Open the classic Plone interface on `localhost:8080`.
As we need to install a few add-ons before we can use it with Volto, do **not** click the :guilabel:`Create a new Plone site` button.
Instead use the :guilabel:`Advanced` button to get to the add-on selection.
From the options there, select :guilabel:`Plone 6 Frontend (Default content on homepage)` and :guilabel:`Plone 6 Frontend (plone.volto)`.
Also unselect :guilabel:`Example content`.
Continue by clicking :guilabel:`Create Plone Page`.
You might need to wait for a few minutes until the page is created.

```{image} _static/required_plone_configuration.png
:align: center
:alt: Plone Addons configuration page
```

If you are already comfortable with setting up classic Plone sites you can also set up a new Plone environment on your machine. To be compatible with Volto it needs to have the following addon products installed:

- collective.folderishtypes.dx
- collective.folderishtypes 3.0.0
- `plone.restapi` 8.12.1
- plone.volto 3.1.0a2

### Yarn environment

To ensure all required dependencies for starting Volto are installed run:

```shell
yarn
```

You can now start up your Volto instance by running the following command:

```shell
yarn start
```

## Volto source code

When developing Volto you will find yourself looking quite often at the Volto source code to see how things are done, the code syntax, and how to clone or override components.
For convenience, a symlink to a copy of the Volto code is set up inside `node_modules` when you run `yarn` in your Volto project folder.
You will find this copy of Volto in the `omelette` folder.

## Recommended plugins

No matter which integrated development environment (IDE) you use, you should also install these plugins:

- Prettier
- ESlint
- prettier-stylelint (for VSCode)
