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
[`docker system prune`](https://docs.docker.com/reference/cli/docker/system/prune/)
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

## Entering a Docker container and run classic local zope commands for debugging or special purposes

A step by step instruction how to enter a running Docker container with a bash and execute commands in context of your `docker-entrypoint.sh` config.

### Prerequisites

- A running docker based deployment on a server or the local machine.
- ssh access to the host machine

### List running containers

in the host machine shell:

```shell
docker ps
```

example output:

```shell
CONTAINER ID   IMAGE                                      COMMAND                  CREATED        STATUS                  PORTS      NAMES
3dxxxxxxea   ghcr.io/me/my-plone-frontend:main          "pnpm start:prod"        1 minute ago   Up 1 minute (healthy)   3000/tcp   my-plone_frontend.2.6hydqi2lubxxxxxxxxxxc4s4p
9dxxxxxxa5   ghcr.io/me/my-plone-frontend:main          "pnpm start:prod"        1 minute ago   Up 1 minute (healthy)   3000/tcp   my-plone_frontend.1.dha3otj0laxxxxxxxxxxljj6e
a8xxxxxx20   ghcr.io/me/my-plone-varnish:main           "/usr/local/bin/dock…"   1 minute ago   Up 1 minute                        my-plone_varnish.1.dj0w1s6sfsxxxxxxxxxxoue6u
d8xxxxxx9c   ghcr.io/me/my-plone-backend:main           "/app/docker-entrypo…"   1 minute ago   Up 1 minute (healthy)   8080/tcp   my-plone_backend.2.tqs1rkqhrtxxxxxxxxxxlrvti
21xxxxxx2e   ghcr.io/me/my-plone-backend:main           "/app/docker-entrypo…"   1 minute ago   Up 1 minute (healthy)   8080/tcp   my-plone_backend.1.ba353y9lfnxxxxxxxxxxjxubq
dexxxxxx32   ghcr.io/kitconcept/cluster-purger:latest   "/app/docker-entrypo…"   1 minute ago   Up 1 minute (healthy)              my-plone_purger.1.0oe71ob3ruxxxxxxxxxxc5m4j
82xxxxxx8d   ghcr.io/kitconcept/cluster-purger:latest   "/app/docker-entrypo…"   1 minute ago   Up 1 minute (healthy)              my-plone_purger.2.7jat5at9fexxxxxxxxxxtnmrs
c9xxxxxxae   postgres:14.15                             "docker-entrypoint.s…"   1 minute ago   Up 1 minute                        my-plone_db.1.dpawmbod09xxxxxxxxxxjrlvw
27xxxxxxcc   traefik:v2.11                              "/entrypoint.sh --pr…"   1 minute ago   Up 1 minute             80/tcp     my-plone_traefik.1.pe7oq21mdyxxxxxxxxxxf78qb
```

### Enter a shell in the particular container

To enter a shell in the particular container using one of the container [ID]s listed above:
```shell
docker exec -it [ID] bash
```

#### Alternatives as oneliners

If you want to enter the first backend container you can try filtering IDs as onliner (works only when only one stack is running in a swarm):

``` shell
docker exec -it `-qf 'name=_backend'|head -n1` bash
```
This will usually open the bash in the /app dir of the backend container.

If you have multiple stacks in swarms on the same server you can run a oneliner (where `my-plone` ist the name of the stack):

``` shell
docker exec -it `docker ps -qf 'name=my-plone_backend'|head -n1` bash
```

### Execute a command using the given environment variables

The default shell is not initialized with the environment variables set via `docker-entrypoint.sh` by default.

#### Example: run classic ZOPE command in the backend

To execute an available classic ZOPE command in the backend without permanently adding the environment variables setup to the session, prefix the command with execution of the `/app/docker-entrypoint.sh` file.

``` shell
./docker-entrypoint.sh ./bin/[local command]
```

Where [local command] can be one of those you can list in `/app/bin/`

- `addzopeuser` can create an emergency user
- `zodbconvert`
- `plone-exporter` or `plone-exporter`

```{seealso}
[How can plone-exporter be called manually inside a docker based Plone 6.x Volto deployment?](https://github.com/plone/plone.exportimport/issues/51)
- It covers how to manually run the `plone_exporter` command inside the backend container with a relstorage.conf
```

```{note}
If you do not need to setup further resources like config files as with the `zodbconvert` command, you can call a command from its path inside the container with this syntax:
```
If you have multiple stacks in swarms on the same server you can run a oneliner including the command in `path_to_command` (where `my-plone` ist the name of the stack):

``` shell
docker exec `docker ps -qf 'name=my-plone_backend'|head -n1` ./docker-entrypoint.sh path_to_command
```

### Copy a file into or from the container

In the server host root:

``` shell
sudo docker cp `docker ps | grep backend.1 | cut -d " " -f 1`:/absolute_path_in_container/filename `local_destination_path/`
```
or

``` shell
sudo docker cp `local_source_path/file` `docker ps | grep backend.1 | cut -d " " -f 1`:/absolute_path_in_container/
```

Add the recursive folder path options as needed.

### Running maintenance commands in a worker container of a seperate instance

#### Example to run the `zodbconvert` commands in a local worker container

```{seealso}
[postgres2zodb | Zodbconvert script to convert relstorage to filestorage and back](https://github.com/plone/postgres2zodb)
- It covers to automate the command inside a backend worker container with a relstorage.conf file
```