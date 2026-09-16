---
myst:
  html_meta:
    "description": "How to install Plone 6 for the training"
    "property=og:description": "How to install Plone 6 for the training"
    "property=og:title": "Installation"
    "keywords": "Installation and Setup of Plone 6 for the training 'Mastering Plone Development'"
---

# Installation

This chapter provides instructions on how to install **Plone with the training code**.

For general Plone installation, deployment, and hosting instructions, refer to the authoritative Plone 6 documentation in {doc}`plone6docs:install/index`.

We encourage you to install and run `Plone` on your own machine, as you will have important benefits:

- You can work with your favorite editor.
- You have all the code of Plone at your fingertips in `site-packages` or `node_modules`.


(installation-prerequisites-label)=

## Prerequisites

We recommend to work on Linux or Mac, not Windows.

You will need some other software in order to install and run Plone.
Follow {ref}`create-project-cookieplone-prerequisites-for-installation-label` to install the following tools, if you don't have them already:

  - uv
  - nvm
  - Node.js
  - GNU make
  - Git


(installation-project-structure)=

## The project structure

The main project for this training is structured as a {term}`monorepo`.
It is a single Git repository which includes both the Plone backend and its React-based frontend Volto, in the following folder structure:

```text
mastering-plone-project
├── backend
└── frontend
```

The {file}`backend` folder contains Plone and our custom backend code and configuration.
The {file}`frontend` folder contains Volto and our custom frontend code and configuration.


(installation-project-label)=

## Install the project

Clone the [`mastering-plone-project` repository](https://github.com/collective/mastering-plone-project).

```shell
git clone git@github.com:collective/mastering-plone-project.git
cd mastering-plone-project
```

```{tip}
The initial structure for this project repository was created by following {ref}`create-project-cookieplone-create-volto-project-label`.
```

Install the project with:

```shell
make install
```

The install command executes multiple tasks.
It will:
- create a Python virtual environment and install Python dependencies using uv
- generate configuration for a Zope instance using `cookiecutter-zope-instance`
- install Node dependencies using pnpm
- create a new Plone site with our `ploneconf.site` add-on installed

By creating and working with a **Python virtual environment**, we are independent of the system Python installation.
The correct version of Python and dependency packages are installed in an isolated path (`backend/.venv`).

The specification of which Python packages to install comes from {file}`backend/pyproject.toml`.

The build generates **Zope configuration** files with Cookiecutter `cookiecutter-zope-instance`.
The file we will modify to update our Zope / Plone configuration is {file}`backend/instance.yaml`.
In this file we will add add-ons that are installed as Python packages and shall be loaded in our instance.
`instance.yaml` is the one configuration file for our Zope / Plone instance.
The [documentation of `cookiecutter-zope-instance`](https://plone.github.io/cookiecutter-zope-instance/) explains a lot more that can be configured like the port or another storage. 

The specification of which Node.js packages to install comes from {file}`frontend/package.json` and {file}`frontend/mrs.developer.json`.

After changes in configuration files, a reinstall is necessary:

```shell
make install
```

(installation-start-backend-label)=

## Start the backend

We are now ready to start the backend with:

```shell
make backend-start
```

Voilà, your Plone is up and running on http://localhost:8080.

The output should be similar to:

```shell
% make backend-start

2026-07-21 15:12:15,604 INFO    [chameleon.config:40][MainThread] directory cache: /Users/davisagli/Plone/mastering-plone-project/backend/instance/var/cache.
2026-07-21 15:12:16,003 WARNING [ZODB.FileStorage:409][MainThread] Ignoring index for /Users/davisagli/Plone/mastering-plone-project/backend/instance/var/filestorage/Data.fs
2026-07-21 15:12:16,155 INFO    [plone.restapi.patches:15][MainThread] PATCH: Disabled ZPublisher.HTTPRequest.ZopeFieldStorage.VALUE_LIMIT. This enables file uploads larger than 1MB.
2026-07-21 15:12:16,364 INFO    [plone.app.event:17][MainThread] icalendar has been set up to use pytz instead of zoneinfo.
2026-07-21 15:12:17,232 INFO    [plone.volto:22][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2026-07-21 15:12:17,630 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 87938.
2026-07-21 15:12:17,633 INFO    [waitress:449][MainThread] Serving on http://127.0.0.1:8080
2026-07-21 15:12:17,633 INFO    [waitress:449][MainThread] Serving on http://[::1]:8080
```

Troubleshooting: We are here to help: Please file an issue in [training repository](https://github.com/plone/training/issues). 

Point your browser to <http://localhost:8080> to see `Plone` running.

```{figure} _static/instructions_plone_running.png
:alt: Plone is running.
:scale: 50 %

Plone, up and running.
```

You can see that there is already an existing Plone site that was created by the install command.

You can stop the running instance anytime using {kbd}`ctrl c`.


(installation-start-frontend-label)=

## Start the frontend

The frontend must be run as a separate process.
Open a second terminal and start it with:

```shell
make frontend-start
```

Point your browser to <http://localhost:3000> and see that the site is up and running.

You can stop the frontend anytime using {kbd}`ctrl c`.


(installation-log-in-label)=

## Log in

Log in to your new site with Login Name `admin` and Password `admin`.

````{tip}
The initial password for the admin user is defined in {file}`backend/instance.yaml`.
You should change your password in production sites via `http://localhost:8080/acl_users/users/manage_users`.

If you ever have the need to create an emergency user, create one with:

```shell
backend/.venv/bin/addzopeuser masterofdisaster mypassworD£xyz2 -c backend/instance/etc/zope.conf
```

````

After logging in, the site should look like this:

```{figure} _static/frontpage_volto_logged_in.png
```


(installation-change-ports-label)=

## Change ports

If you want the Plone backend to listen on port 9080 instead of the default 8080, open the file {file}`backend/instance.yml` in your favorite editor.

Add the `wsgi_listen` option.

```yaml
default_context:
    initial_user_password: 'admin'
    zcml_package_includes: 'ploneconf.site'
    wsgi_listen: localhost:9080
```

Now restart your backend.

```shell
make backend-start
```

You will also have to tell the frontend that the backend is now running on a different port!

You need to change the environment variable `RAZZLE_INTERNAL_API_PATH` to the base URL of the backend:

```shell
RAZZLE_INTERNAL_API_PATH=http://localhost:9080/Plone make frontend-start
```

If your Plone instance isn't called `Plone`, you can use the same approach:

```shell
RAZZLE_INTERNAL_API_PATH=http://localhost:8080/mysite make frontend-start
```

By default the frontend will listen on port 3000.
You can change the port for the frontend by specifying the environment variable `PORT`:

```shell
PORT=1234 make frontend-start
```


(installation-mailserver-label)=

## Configure a mail server

````{only} not presentation
For production-level deployments you have to configure a mail server.
Later in the training we will create some content rules that send emails when new content is put on our site.

For the training you don't have to configure a working mail server.
The Plone add-on `Products.PrintingMailHost` is installed, which will print all outgoing emails to the console instead of sending them.
````

Head over to the mail control panel http://localhost:8080/Plone/@@mail-controlpanel and apply the following configuration:

- Server: {samp}`localhost`
- Username: leave blank
- Password: leave blank
- Site 'From' name: Your name
- Site 'From' address: Your email address

Click on {guilabel}`Save and send test e-mail`.
You will see the mail content in the console output of your instance.
Plone will not actually send the email to the receiver's address unless you remove or deactivate [Products.PrintingMailHost](https://pypi.org/project/Products.PrintingMailHost/).
