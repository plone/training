---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Editing your project

There are some changes possible in the project without writing code by just editing the configuration.
A popular change is adding an add-on.

## About Add-Ons

Both Plone Frontend and Plone Backend allows adding add-ons.
Dependent on the add-on it could consist out of one part, like only for Plone Backend or only Plone Frontend.
Or it needs to install add-ons in both, working together.
If the latter is the case these are two different components.

Plone Frontend add-ons are written in Javascript and are released as NPM packages.
The Plone community maintains a curated list of Plone Frontend add-ons named [Awesome Volto](https://github.com/collective/awesome-volto).

Plone Backend add-ons are written in Python and are released on the Python Package Index (PyPI).
The Plone community maintains a curated list of Plone Backend and Plone Classic UI add-ons named [Awesome Plone](https://github.com/collective/awesome-plone).


## Starting the servers

After a [new project](new-project.md) was created lets check every thing runs as expected.

### Frontend
On a terminal, run the following code to start the frontend server:

```{code-base} shell
make start-frontend
```
After a while you should see:

TODO: Add image here

### Backend

On a second terminal, run the following code to start the backend server:

```{code-base} shell
make start-frontend
```

After a while you should see:

```
INFO    [waitress:486][MainThread] Serving on http://0.0.0.0:8080`
```

## Check Local access

http://plone-conference.localhost:3000

## Stopping the servers

On both terminals press `Ctrl-c`.

# Adding OAuth Support

As an example for this training we add a new authentication method:
Login with GitHub.

There is already a plugin available consisting out of one module for Plone Frontend and another for Plone Backend.

The Plugin needs am application key from Github.

First you need to create a new application on GitHub ...

## Backend

Go to the folder `/backend`.

Append `pas.plugins.authomatic` to `requirements.txt`.
This installs the package too when installing Plone.

Edit file `instance.yml`.
In there is a line `package_includes: ['plone_conference']`.
This loads the package configuration when starting Plone Backend.
Append `pas.plugins.authomatic` to the array.
Afterwars its looks like so:

```
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: ['plone_conference', `pas.plugins.authomatic']

    db_storage: direct
```

To activate the settings run `make build-backend` in the root folder of the project.

## Frontend

Go to folder `frontend` and edit the package.json.

Append `@plonecollective/volto-authomatic` to the lists if `dependencies` and `addons`.

To activate the settings run `make build-frontend` in the root folder of the project.

## Activate the plugin

You need to login as administrator to Plone Backend (in Classic UI) at `http://localhost:8080`.

At the bottom of the menu on the left choose `admin`, then `Site Setup` and then `add-ons`.
Then choose to install `pas.plugins.authomatic`.

Now configure the plugin by adding the Github configuration as JSON.

```
{
    "github": {
        "display": {
            "title": "Github",
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

You need to go to your Github account and add an application manually to get the two keys for the application.

Save and all is set.
