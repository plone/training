
The Plone Playbook
------------------

Checkout
^^^^^^^^

Requirements
^^^^^^^^^^^^

Quick review of contents
^^^^^^^^^^^^^^^^^^^^^^^^

Vagrant
```````

Sample configurations
`````````````````````

The playbook kit contains several sample configuration files.

sample-very-small.yml

    Targets a server with 512MB of memory and one CPU core.
    Sets up one ZEO client with two threads with very small object caches.
    No load balancer.
    Varnish cache is file-based.

sample-small.yml

    Targets a server with 1GB of memory and one CPU core.
    Sets up one ZEO client with two threads with small object caches.
    No load balancer.
    Varnish cache is file-based.

sample-medium.yml

    Targets a server with 2GB of memory and two CPU cores.
    Sets up two ZEO clients, each with one thread with a medium object cache.
    Uses load balancer to manage the queue to the ZEO clients.
    Varnish cache is memory-based.

sample-multiserver.yml

    A configuration that demonstrates how to run multiple Zope/Plone installs with different versions and virtual hosting.

The first four samples are meant to be immediately useful.
Just copy and customize.
The multiserver sample is just a demonstration of several customization techniques.
Read it for examples, but don't expect to use it without substantial customization.

Why no ``sample-large.yml``?
Because a larger server installation is always going to require more thought and customization.
We'll discuss those customization points later.
The ``sample-medium.yml`` file will give you a starting point.
