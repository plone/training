---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(voltohandson-quickstart-label)=

# Quick Start

## Set Up Volto Project


To create our first volto project we will youse the volto generator tool. To install that on your machine run:
```
$ npm install -g yo
$ npm install -g @plone/generator-volto
```

After thats done create a folder where your project will be located. You can call it whatever your projectname shall be. In our case we will use `volto-hands-on-training`. Inside that folder run:
```
$ yo @plone/volto
```
The dialogue in the console will ask you for the name of your project and wether you want to install any addons. You can skip both by pressing the `enter` button, as we will use the default name and dont want to use any addons for the training.


## Build environments

We need to build two environments.
Start two terminal sessions, one for each environment, Plone and Yarn, and a third session to issue Git and other shell commands.
In each terminal session you should be in your project folder `volto-hands-on-training`.

### Plone environment

To run your Volto site we will be using the Plone docker image with all extensions that are necessary to work with Volto installed. Start Plone by running

```shell
$ docker run -it --rm --name=plone -p 8080:8080 -e SITE=Plone -e ADDONS="plone.volto" -e ZCML="plone.volto.cors" -e PROFILES="plone.volto:default-homepage" plone
```

Keep that process running during the whole training in one of your console windows.

If you are already comfortable with setting up classic Plone sites you can also set up a new Plone environment on your machine. To be compatible with Volto it needs to have the following addon products installed:
- collective.folderishtypes.dx
- collective.folderishtypes 3.0.0
- plone.restapi 7.0.0
- plone.volto 3.1.0a2

### Yarn environment

To make sure all dependencies necessary to run Voltoare installed run:

```shell
yarn
```
You can now start up your Volto instance by running the following command:

```shell
yarn
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


