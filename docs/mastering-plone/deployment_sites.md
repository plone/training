---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(deployment-sites-label)=

# Buildout II: Getting Ready for Deployment

```{todo}
Installation without buildout
```


(deployment-starzel-label)=

## The Starzel buildout

Have a look at the buildout some of the trainers use for their projects: <https://github.com/starzel/buildout>

It has some notable features:

- It extends to config- and version-files on github shared by all projects that use the same version of Plone:

  ```cfg
  [buildout]
  extends =
      https://raw.githubusercontent.com/starzel/buildout/5.1.2/linkto/base.cfg
  ```

- It allows to update a project simply by changing the version it extends.

- It allows to update all projects of one version by changing remote files (very useful for HotFixes).

- It is minimal work to setup a new project.

- It has presets for development, testing, staging and production.

- It has all the nice development-helpers we use.

Another noteable buildout to look for inspiration:

- <https://github.com/4teamwork/ftw-buildouts>

(deployment-setup-label)=

## A deployment setup

A 'normal' deployment setup could look like this:

```text
ZEO-Server   ->   ZEO-Server (ZRS)

   / | \

ZEO Clients (as many as you want)

   \ | /

Load balancer (nginx or haproxy)

     |

   Cache (varnish)

     |

Webserver (nginx)
```

Deploying Plone and production-setups are outside the scope for this training.

```{seealso}
- <https://6.docs.plone.org/deployment/index.html>
- {doc}`../plone-deployment/index`
```

(deployment-tools-label)=

## Other tools we use

There are plenty of tools that make developing and managing sites much easier. Here are only some of the ones you might want to check out:

- Fabric (managing sites)
- Sentry (error monitoring)
- Ansible (managing and provisioning machines)
- Greylog, ELK (logging)
- Nagios, Zabbix (server monitoring)
- jenkins, gitlab-ci, travis, [drone.io](https://www.drone.io/) (Continuous Integration)
- piwik (statistics)
- gitlab (code repository and code review)
- redmine, taiga, assembla (project-management and ticket-system)
