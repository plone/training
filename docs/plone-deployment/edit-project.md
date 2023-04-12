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


## Add OAuth support

As an example of adding an add-on for this training, we will add a new authentication method, login with GitHub.

We will do this twice: once for Classic UI, and again for Volto.

```{important}
You should use two web browsers, one for logging in as an Administrator and the other for logging in as your GitHub username via OAuth.
Always stay logged in as an Administrator in your primary web browser, and use your secondary web browser for OAuth authentication. 
```


(create-a-github-oauth-application-label)=

### Create a GitHub OAuth application

Both Plone user interfaces require the creation of a GitHub OAuth application.
Follow the GitHub documentation [Creating an OAuth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app).

You can configure the GitHub OAuth application to use only one Plone user interface at a time, but you can switch back and forth by changing the values.
We will start with Classic UI configuration.
After we get OAuth via GitHub working in Classic UI, we will switch to Volto.


(classic-ui-github-oauth-app-configuration-label)=

#### Classic UI GitHub OAuth app configuration

Use the following values when creating your GitHub OAuth application.

Application name
: `plone-conference`

Homepage URL
: `http://localhost:8080/Plone`

Application description
: `Plone Conference`

Authorization callback URL
: `http://localhost:8080/Plone/authomatic-handler/`


(get-your-github-client-id-and-secret-label)=

### Get your GitHub client ID and secret

After creating the GitHub OAuth application, you will have a client ID.
Save this for the next section {ref}`activate-the-plugin-label`, where its value will be used for the `consumer_key`.

Now you can generate a client secret by clicking {guilabel}`Generate a client secret`.
Save this for the next section {ref}`activate-the-plugin-label`, where its value will be used for the `consumer_secret`.

These two values will work for both Plone user interfaces.


### Install `pas.plugins.authomatic` add-on

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


(activate-the-plugin-label)=

### Activate and configure the add-on

In your primary browser, login to Plone Classic UI as Administrator at `http://localhost:8080/Plone/login/`.

At the bottom of the menu on the left, choose {guilabel}`admin > Site Setup`.
Select the {guilabel}`Add-ons` control panel.
Then install `pas.plugins.authomatic` by clicking the {guilabel}`Install` button for {guilabel}`Authomatic PAS Plugin`.

Now configure the plugin by adding the GitHub configuration as JSON.
Navigate to {guilabel}`Users > Authomatic (OAuth2/OpenID)` from anywhere in the Site Setup.

Copy the following JSON configuration, and replace the two values from GitHub.
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
Test it in your secondary browser by visiting `http://localhost:8080/Plone/login/`.
You should be prompted to log in with GitHub.


### Configure the OAuth user permissions

You can assign the OAuthed user to groups and grant permissions.
This is useful if you expect this user to perform the same functions as an Administrator.

Back in the primary browser as Administrator, visit the control panel {guilabel}`Users > Users`.
For the {guilabel}`User name` row, check appropriate permissions.
For the purpose of this training, check {guilabel}`Manager`, then click {guilabel}`Apply changes`.


### Change the GitHub OAuth application configuration for Volto

Now that we have OAuth via GitHub working in Classic UI, let's switch to using Volto.

We can reuse the client ID and secret from {ref}`get-your-github-client-id-and-secret-label` and that we entered into the `pas.plugins.authomatic` add-on's control panel configuration in {ref}`activate-the-plugin-label` as is.

We will repeat some of the above steps, but with a few differences.


#### Volto GitHub OAuth app configuration

Following what we did previously in {ref}`classic-ui-github-oauth-app-configuration-label`, we will change two values, {guilabel}`Homepage URL` and {guilabel}`Authorization callback URL`.
Use the following values.

Application name
: `plone-conference`

Homepage URL
: `http://localhost:3000/`

Application description
: `Plone Conference`

Authorization callback URL
: `http://localhost:3000/login-authomatic`

Click {guilabel}`Update application` to save the changes.


### Install `volto-authomatic` add-on

Go to the folder `frontend`, and edit the file `package.json`.

Append `@plone-collective/volto-authomatic` to the list `addons`.

```json
"addons": [
  "@plone-collective/volto-authomatic"
],
```

Append the key/value pair `"@plone-collective/volto-authomatic": "*"` to the dictionary `dependencies`.

```json
"dependencies": {
  "@plone-collective/volto-authomatic": "*"
}
```

To activate the settings, run `make build-frontend` in the root folder of the project.

Finally, restart the frontend with `make start-frontend`.

```{seealso}
[`volto-authomatic`](https://github.com/collective/volto-authomatic)
```

Test it in your secondary browser by visiting `http://localhost:3000/login/`.
You should be prompted to log in with GitHub.
