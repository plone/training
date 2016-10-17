What Doesn't It Do
^^^^^^^^^^^^^^^^^^

Storage Options
```````````````

Amazon recently introduced ``Elastic File System`` an effectively unlimited
size cloud file storage that can be mounted simultaneously on multiple
servers. It provides high availability and durability and should be
significantly faster than either S3 or even standard SSD EBS mounts. For these
reasons it would make an ideal storage option for a shared blob directory and
possibly also ZEO filestorages.

Integrating this new storage option into the recipes and documentation should
be a high priority going forward. There are probably some other fun new AWS
services that would be useful to integrate.


Proxy Cache Purging
```````````````````

Plone provides some very nice proxy caching configuration, but that
configuration is managed TTW and stored persistently in the ZODB. If you have
multiple proxy caches which could be going online or offline automatically or
changing IP addresses, then having persistent configuration of caches to purge
is not ideal.

It would be very useful to add support in plone.app.caching for reading a list
of proxy servers from an environment variable or other mechanism that can
easily be managed as part of the configuration phase.


Other Stuff?
````````````

Probably, play around with it and let me know.
