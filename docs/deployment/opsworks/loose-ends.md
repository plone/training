---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# What Doesn't It Do

## Storage Options

Amazon introduced `Elastic File System` an effectively unlimited size cloud file storage that can
be mounted simultaneously on multiple servers.

It provides high availability and durability and should be significantly faster than either {term}`S3` or even standard SSD EBS mounts.

For these reasons it would make an ideal storage option for a shared blob directory and possibly also ZEO filestorages.

Integrating this new storage option into the recipes and documentation should be a high priority going forward.
The interface for Elastic File System is {term}`NFS` v4, which the stack already supports, so it may even be trivial to integrate.

There are probably some other fun new {term}`AWS` services that would be useful to integrate.

## Proxy Cache Purging

Plone provides some very nice proxy caching configuration, but that configuration is managed
{term}`TTW` (Through-The-Web) and stored persistently in the {term}`ZODB`.

If you have multiple proxy caches which could be going online or offline automatically or changing IP addresses,
then having persistent configuration of caches to purge is not ideal.

It would be very useful to add support in [plone.app.caching](https://github.com/plone/plone.app.caching)
for reading a list of proxy servers from an environment variable or other mechanism that can be managed as part of the configuration phase.

## Chef 12

The latest OpsWorks codebase requires Chef 12.
The Python cookbooks are currently only tested on Chef 11.

Running OpswWrks on Ubuntu Xenial instances requires using the latest Chef 12 version.

```{note}
This will likely require extensive testing and upgrades to dependency cookbooks.
```
