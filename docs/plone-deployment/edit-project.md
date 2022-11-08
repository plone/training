---
myst:
  html_meta:
    "description": "Editing your project for deployment"
    "property=og:description": "Editing your project for deployment"
    "property=og:title": "Editing your project for deployment"
    "keywords": "Edit, Plone, project, add-ons, Volto"
---

# Editing your project

There are some changes possible in the project without writing code by just editing the configuration.
A popular change is adding an add-on.


## About Add-ons

Both Plone Frontend and Plone Backend allow adding add-ons.
Depending on the add-on, it could apply to only one of Plone Backend or Plone Frontend, or both working together.
If the latter is the case, then these would be two different components.

Plone Frontend add-ons are written in JavaScript and are released as NPM packages.
The Plone community maintains a curated list of Plone Frontend add-ons named [Awesome Volto](https://github.com/collective/awesome-volto).

Plone Backend add-ons are written in Python and are released on the Python Package Index (PyPI).
The Plone community maintains a curated list of Plone Backend and Plone Classic UI add-ons named [Awesome Plone](https://github.com/collective/awesome-plone).


## Starting the servers

After a [new project](new-project) was created, let's check that everything runs as expected.


### Frontend

In a terminal, run the following code to start the frontend server:

```shell
make start-frontend
```

After a while you should see:

```console
yarn run v1.22.19
$ razzle start
 WAIT  Compiling...


✔ Client
  Compiled successfully in 620.55ms

✔ Server
  Compiled successfully in 25.64s

✅  Server-side HMR Enabled!
sswp> Handling Hot Module Reloading
Volto is running in SEAMLESS mode
Using internal proxy: http://localhost:3000 -> http://localhost:8080/Plone
🎭 Volto started at 0.0.0.0:3000 🚀
```

### Backend

On a second terminal, run the following code to start the backend server:

```shell
make start-backend
```

After a while you should see:

```console
INFO    [waitress:486][MainThread] Serving on http://0.0.0.0:8080
```

## Check local access

Visit the Plone site at the following URL:

http://plone-conference.localhost:3000


## Stopping the servers

In both terminals, press {kbd}`Ctrl-C`.


## Adding OAuth support

As an example of adding an add-on for this training, we will add a new authentication method, login with GitHub.

There is already a plugin available consisting of one module for Plone Frontend and another for Plone Backend.

The Plugin needs an application key from GitHub.

First you need to create a new application on GitHub.


### Backend

Go to the folder `/backend`.

Append `pas.plugins.authomatic` to `requirements.txt`.
This installs the package, too, when installing Plone.

Edit the file `instance.yml`.
There is a line `package_includes: ['plone_conference']`.
This loads the package configuration when starting Plone Backend.
Append `pas.plugins.authomatic` to the array.
Afterward it should look like the following:

```{code-block} yaml
:emphasize-lines: 6

default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: ['plone_conference', 'pas.plugins.authomatic']

    db_storage: direct
```

To activate the settings, run `make build-backend` in the root folder of the project.


### Frontend

Go to the folder `frontend`, and edit the file `package.json`.

Append `@plone-collective/volto-authomatic` to the lists `dependencies` and `addons`.

To activate the settings, run `make build-frontend` in the root folder of the project.


### Activate the plugin

You need to login to Plone Backend as Administrator (in Classic UI) at `http://localhost:8080`.

At the bottom of the menu on the left, choose {guilabel}`admin`, {guilabel}`Site Setup`, then {guilabel}`add-ons`.
Then choose to install `pas.plugins.authomatic`.

Now configure the plugin by adding the GitHub configuration as JSON.

```json
{
    "github": {
        "display": {
            "title": "GitHub",
            "cssclasses": {
                "button": "btn btn-default",
                "icon": "glypicon glyphicon-github"
            },
            "as_form": false
        },
        "propertymap": {
            "email": "email",
            "link": "home_page",
            "location": "location",
            "name": "fullname",
            "picture": "avatar_url"
        },
        "class_": "authomatic.providers.oauth2.GitHub",
        "consumer_key": "KEYHERE",
        "consumer_secret": "SECRETHERE",
        "access_headers": {
            "User-Agent": "Plone (pas.plugins.authomatic)"
        }
    }
}
```

You need to go to your GitHub account and add an application manually to get the two keys for the application.

Save, and all is set.
Test it by logging out of your Plone site, then try logging back in.
