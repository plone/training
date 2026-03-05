---
myst:
  html_meta:
    "description": "Guide to start your Plone project on your local machine"
    "property=og:description": "Guide to start your Plone project on your local machine"
    "property=og:title": "Guide to start your Plone project on your local machine"
    "keywords": "Plone, deployment, Ansible, Docker, GitHub, local development"
---

# Start the project

{term}`Cookieplone` equips you with essential tools to initiate a local development environment. {doc}`project-new` offers two methods to launch your project: manually starting the backend and frontend servers, or utilizing a Docker Compose stack.

## Run local servers

This method requires two terminal sessions, as both backend and frontend operate in "foreground mode". It's optimal for local development due to its swift change and restart cycle. However, accessing each server on their internal ports can lead to CORS issues in real-world deployments.

### Start the backend

Navigate to the project's root folder and execute:

```shell
make backend-start
```

This command initiates the backend server. Upon successful startup, you'll observe:

```console
... INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```

The above indicates that the server is operational and awaiting requests on port 8080. Visit http://localhost:8080 to explore.

```{figure} _static/start_backend_localhost.png
:alt: Backend server initiation at `http://localhost:8080`

Backend server initiation at `http://localhost:8080`
```


### Start the frontend

In a new terminal at the project root, execute:

```shell
make frontend-start
```

The frontend initiation takes longer, due to the initial code base compilation for both the Node.js server for the browser JavaScript bundles. A successful startup displays:

```console
🎭 Volto started at 0.0.0.0:3000 🚀
```

The above signifies that the frontend server is active on port 3000. Access it via http://localhost:3000.

```{figure} _static/start_frontend_localhost.png
:alt: Frontend server initiation at `http://localhost:3000`

Frontend server initiation at `http://localhost:3000`
```

```{note}
Default credentials: **admin/admin**.
```

## Stop the servers

In both terminals, press {kbd}`Ctrl-C`.

## Run Docker Compose

Docker Compose is suitable for reviewing your development progress or exploring the project. It comprises four services: {term}`Traefik` web server, frontend, backend, and a PostgreSQL database, mimicking a production environment.

```{note}
A secondary backend route, `/ClassicUI`, mirrors `http://localhost:8080/Plone`. It's secured with basic authentication, default credentials being **admin/admin**.
```

### Start the Stack

Ensure port 80 is free, then initiate the stack with:

```shell
make stack-start
```

Docker will download necessary images, build Frontend and Backend images, and initiate all services. Upon completion, a message prompts you to visit [http://pybr25.localhost](http://pybr25.localhost).

### Checking the Stack Status

Verify the stack's operational status with:

```shell
make stack-status
```

Initially, the frontend may display an **(unhealthy)** status due to the absence of a created Plone site.

### Create a new Plone site

Initiate a new Plone site within the Docker Compose stack by executing:

```shell
make stack-create-site
```

Re-run `make stack-status`, and both backend and frontend should now display a **(healthy)** status.

### Accessing the site

Your website is accessible at http://pybr25.localhost.

```{figure} _static/start_stack_localhost.png
:alt: Accessing the site at `http://pybr25.localhost`

Accessing the site at `http://pybr25.localhost`
```

### Updating the code base

For codebase modifications, re-run `make stack-start` to rebuild the affected containers, ensuring your site's behavior aligns with the updates.

### Stop the stack

To stop the stack while preserving site data, execute:

```shell
make stack-stop
```

### Removing the stack

To dismantle the stack and erase all site data, use:

```shell
make stack-rm
```
