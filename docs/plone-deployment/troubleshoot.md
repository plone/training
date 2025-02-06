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

## Entering a Docker container and run classic local zope commands for debugging


A step by step instruction how to enter a running Docker container with a bash and execute commands in context of your config is included in this ticket:
```{seealso}
[How can plone-exporter be called manually inside a docker based Plone 6.0 Volto deployment?](https://github.com/plone/plone.exportimport/issues/51)
- It covers how to manually run the `plone_exporter` command inside the backend container with a relstorage.conf
**TODO:** Wrapping this up generically and replace this hint with regular docs.
```
