---
myst:
  html_meta:
    "description": "Troubleshoot Plone Deployment issues"
    "property=og:description": "Troubleshoot Plone Deployment issues"
    "property=og:title": "Troubleshoot Plone Deployment issues"
    "keywords": "Plone, Deployment, Stack, Configuration, Guide, Troubleshoot"
---

# Troubleshoot deployment issues

This page offers some tips to troubleshoot the Plone Deployment Training.

## Docker `Could not create directory.`

Docker requires sufficient virtual disk space to install and build images.
A typical error message may be `Could not create directory.` or anything else that mentions writing to the image.
To resolve this, use an appropriate `docker system prune` option, such as `docker system prune -a`.

```{seealso}
[`docker system prune`](https://docs.docker.com/engine/reference/commandline/system_prune/)
```

You can also configure settings for Docker Desktop.
Under {menuselection}`Prefences --> Resources --> Advanced`, you can configure appropriate settings for virtual disk limit and memory.

```{seealso}
-   [Change Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)
```


## Docker memory usage

Docker requires sufficient memory to install and build images.
2GB of RAM is usually sufficient.
See the previous section for settings details.


## Frontend containers restart every minute

If your frontend containers built successfully, but restart every 60 seconds after an initial deployment, you can view the frontend container's log files with the following command.

```shell
cd devops
make stack-logs-frontend
```

```console
==> Stack my-plone-volto-project-com: Logs for frontend in context prod 
...
my-volto-project-com_frontend.1.3u0sqs69nmwh@kwk    | Command failed with signal "SIGTERM"
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | 
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | > project-dev@1.0.0-alpha.0 start:prod /app
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | > pnpm --filter @plone/volto start:prod
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | 
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | 
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | > @plone/volto@18.8.2 start:prod /app/core/packages/volto
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | > NODE_ENV=production node build/server.js
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | 
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | API server (API_PATH) is set to: https://my.plone.volto.project.com
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | Proxying API requests from https://my.plone.volto.project.com/++api++ to http://backend:8080/Plone
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | 🎭 Volto started at 0.0.0.0:3000 🚀
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    |  ELIFECYCLE  Command failed.
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | /app/core/packages/volto:
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    |  ERR_PNPM_RECURSIVE_RUN_FIRST_FAIL  @plone/volto@18.8.2 start:prod: `NODE_ENV=production node build/server.js`
my-volto-project-com_frontend.1.4e3ajerpdxpm@kwk    | Command failed with signal "SIGTERM"
...
```

If deploying for the first time, the frontend containers might not be healthy due to the absence of a configured Plone site on the backend.
Or if you've wiped the swarm for an initial redeployment using, for example, `docker service rm $(docker service ls -q)` on the server, then the existing site is gone and needs recreation as well.

Create a new Plone site in the backend container with the following command.

```shell
make stack-create-site
```
