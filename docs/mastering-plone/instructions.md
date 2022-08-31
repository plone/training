---
myst:
  html_meta:
    "description": "How to install Plone 6 for the training"
    "property=og:description": "How to install Plone 6 for the training"
    "property=og:title": ""
    "keywords": "Installation and Setup of Plone 6 for the training 'Mastering Plone Development'"
---

(instructions-label)=

# Installing Plone for the Training

We install the `Plone` backend and its `React`-based frontend `Volto`.
This starts with the following folder structure:

```text
training
├── backend
└── frontend
```

In {file}`backend` we install Plone and add our custom Python code.
In {file}`frontend` we install Volto and add our custom React code.


(instructions-install-backend-label)=

## Installing the backend

We encourage you to install and run `Plone` on your own machine, as you will have important benefits:

- You can work with your favorite editor.
- You have all the code of Plone at your fingertips in `site-packages` tree.


### Prerequisites

Please see [official installation instructions](https://6.dev-docs.plone.org/install/source.html#installation-backend).


### Installation

Set up Plone with the training code: `ploneconf.site` add-on and `training.votable` add-on.

```shell
mkdir training
cd training
git clone https://github.com/collective/training_buildout.git backend
cd backend
```

Until Mastering Plone 6 version is released, please checkout the branch `plone6`.

```shell
git checkout plone6
```

Create a Python virtual environment.
Install prerequisites.
Run {term}`mxdev` to be prepared to install Plone packages with pip.

```shell
python -m venv venv
source venv/bin/activate
pip install -U pip wheel mxdev
mxdev -c mx.ini
```

For more info about the fancy tool {term}`mxdev`, see [official installation instructions](https://6.dev-docs.plone.org/install/source.html#installation-backend).

Install your Plone packages, core and add-ons:

```shell
pip install -r requirements-mxdev.txt
```

Generate your Zope configuration with cookiecutter.
This is also necessary after changes of `instance.yaml`.

```shell
cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

Run Zope:

```shell
runwsgi instance/etc/zope.ini
```

Voilà, your Plone is up and running on http://localhost:8080.


````{note}
Troubleshooting

If you encounter bug "The 'Paste' distribution was not found and is required by the application": Be sure that you have activated your virtual Python environment and are running its runwsgi and not another one.

```shell
source venv/bin/activate
runwsgi instance/etc/zope.ini
```
````

The output should be similar to:

```shell

me@here backend % runwsgi instance/etc/zope.ini
2022-08-24 00:45:39,083 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 93572.
2022-08-24 00:45:39,085 INFO    [waitress:486][MainThread] Serving on http://[::1]:8080
2022-08-24 00:45:39,085 INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```

Troubleshooting: We are here to help: Please file an issue in [training repo](https://github.com/plone/training/issues). 


Point your browser to <http://localhost:8080> to see `Plone` running.

```{figure} _static/instructions_plone_running.png
:alt: Plone is running.
:scale: 50 %

`Plone`, up and running.
```

There is no Plone site yet.
We will create one in the next chapter.

You can stop the running instance anytime using {kbd}`ctrl + c`.

```{figure} _static/instructions_create_instance.png
:alt: Ready to create a `Plone` instance.
:scale: 50 %

Ready to create a `Plone` instance
```





(instructions-install-frontend-label)=

## Installing the frontend

You have two options:

> 1. Create the frontend from scratch using the Volto generator.
> 2. Use the prepared Volto project [volto-ploneconf](https://github.com/collective/volto-ploneconf) with all the code for the training.


### Option 1: Frontend from scratch with Volto generator


{ref}`plone6docs:install-source-volto-frontend-label`


### Option 2. Start with prepared training project `volto-ploneconf` with all code for the training

Prepare the pre-requisites explained in {ref}`plone6docs:install-source-volto-frontend-label`.


Get the code for the frontend from github and install:

```shell
git clone https://github.com/collective/volto-ploneconf.git frontend
cd frontend
yarn
```

Now you can start the app with:

```
$ yarn start
```

Create a Plone site object *Plone* on <http://localhost:8080>

Point your browser to <http://localhost:3000> and see that Plone is up and running.

You can stop the frontend anytime using {kbd}`ctrl + c`.
