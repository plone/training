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

In a second terminal, run the following code to start the backend server:

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

The Plugin needs an application key and secret from GitHub.


### Backend

Go to the folder `backend`.

Open the file `requirements.txt`, and append `pas.plugins.authomatic`.
This installs the package, too, when installing Plone.

Edit the file `instance.yaml`.
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

Finally, restart the backend with `make start-backend`.


### Frontend

Go to the folder `frontend`, and edit the file `package.json`.

Append `@plone-collective/volto-authomatic` to the lists `dependencies` and `addons`.

To activate the settings, run `make build-frontend` in the root folder of the project.

Finally, restart the frontend with `make start-frontend`.


### Get your GitHub key and secret

First create a GitHub OAuth application. Follow the excellent GitHub documentation [Creating an OAuth App](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app).

Use the following values:

Application name
: `plone-conference`

Homepage URL
: `http://localhost:3000/`

Application description
: `Plone Conference`

Authorization callback URL
: `http://localhost:3000/`

After creating the OAuth application, you will have a client ID.
Save this for the next section {ref}`activate-the-plugin-label`.

Now you can generate a client secret by clicking {guilabel}`Generate a client secret`.
Save this for the next section {ref}`activate-the-plugin-label`.


(activate-the-plugin-label)=

### Activate the plugin

You need to login to Plone Backend as Administrator (in Classic UI) at `http://localhost:8080/Plone`.

At the bottom of the menu on the left, choose {guilabel}`admin > Site Setup`.
Select the {guilabel}`Add-ons` control panel.
Then install `pas.plugins.authomatic` by clicking the {guilabel}`Install` button for {guilabel}`Authomatic PAS Plugin`.

Now configure the plugin by adding the GitHub configuration as JSON.
Navigate to {guilabel}`Users > Authomatic (OAuth2/OpenID)` from anywhere in the Site Setup.

Copy the following JSON configuration, and replace two values from GitHub.
The client ID will be the value for `consumer_key`.
The client secret will be the value for `consumer_secret`.
Replace the existing JSON configuration in the control panel with your new configuration.

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

Click {guilabel}`Save`, and all is set.
Test it by logging out of your Plone site, then try logging back in.
You should be prompted to log in with GitHub.
