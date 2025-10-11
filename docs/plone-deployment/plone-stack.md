---
myst:
  html_meta:
    "description": "Introduction to the Plone deployment stack"
    "property=og:description": "Explore the components and configurations for deploying a modern Plone 6 site."
    "property=og:title": "Introduction to the Plone deployment stack"
    "keywords": "Plone, Deployment, Stack, Configuration, Guide"
---
# Introduction to Plone Stack

Explore the intricate components of the Plone stack, tailored for deploying a modern Plone 6 site with a ReactJS-powered frontend.
For deployments focusing on Plone Classic UI with server-side HTML rendering, the frontend component is excluded.
This guide won't cover the integration of a web accelerator or the setup of an edge caching service.

## Components of the Plone Stack

### Web server

The web server, accessible externally on ports 80 and 443, handles the routing and rewriting of HTTP requests to the Plone frontend and backend, and is tasked with TLS termination. While {term}`nginx` and {term}`Traefik` are recommended, other web servers can also be employed. This training will exclusively utilize Traefik.

To understand the rewrite rules used in Traefik, please read our reference about {term}`Zope`'s {doc}`virtual-host`.

### Web Accelerator

{term}`Varnish`, a web accelerator, is positioned between the external web server and internal services to cache dynamically generated content. For a detailed Plone setup with Varnish, refer to the [volto-caching](https://github.com/collective/volto-caching) repository.

### Plone Frontend

Hosted on a Node.js HTTP-server running on port 3000, the Plone frontend constitutes the default user interface. It serves a sever side rendered html version of the webpage and delivers the javascript bundles for the dynamic web application runnin gin the browser. It requires access to the Plone Backend and is exposed through the webserver and Accelerator. 

### Plone Backend

Operating on port 8080, the Plone Backend, Python  WSGI process, serves as the Application server hosting the Plone REST API. It delivers the content to the frontend Server and Browsers, stores it persistently in a backendd database or on filesystrem, and provides management API and security, like moving/copying content, advanced worfklows, security, etc.  

It's optimal to pair it with a specialized database like ZEO server or a relational database

### Database

The database layer can range from a simple ZODB with file storage to more scalable options like a ZEO server or a relational database via RelStorage, supporting PostgreSQL, MySQL/MariaDB, and Oracle. In the most simple version, the Plone backend can open a database on the local filesystem. But in this setup you are limited to only one backend. If you use ZEO, multiple Plone backends open a connection to the ZEO server, which manages the ZODB files. A separate shared file system like NFS is essential for storing binary data and sharing it to the backends with a ZEO setup. 

This training will focus on using a PostgreSQL instance. With a relational database, the backends connect through the RelStorage Adapter to the Database, where the ZODB is mapped in a very basic way to a number of specialised tables and fields to hold all data. 

Storing binary data (blobs) in a relational database or keeping them seperate in a blob storage is an advanced discussion and has different trade offs when looking at
performance and high availability.

## Deployment Configurations

### Basic Setup

#### Without Specialized Database

```
Web server → Plone Frontend → Plone Backend (file storage)
```

```{note}
Ideal for demo sites and Plone trials.
```

#### With Specialized Database

```
Web server → Plone Frontend → Plone Backend → Database
```

```{note}
Solution to be presented in this training.
```

#### With Specialized Database and Caching

```
Web server → Web Accelerator → Plone Frontend → Plone Backend → Database
```

### Multi-server Setup

In a multi-server environment, load distribution and redundancy are achieved through various configurations, enabling horizontal scaling.

```{figure} _static/request_flow.png
:alt: Flow of a request to `https://example.com`

Flow of a request to https://example.com
```

#### Web server and Web Accelerator Layer

Externally accessible machine hosting both the web server and web accelerator on ports 80 and 443.

#### Plone Application Layer (Frontend and Backend)

Hosts scalable Plone Frontend and Backend processes, enhancing performance and responsiveness.

#### Database Layer

Can host a ZEO server or a relational database. Managed relational database services with backup and replication are
recommended for those unfamiliar with database management, with PostgreSQL being a preferred choice.

### Scaling and High Availability

The components of the CMS Stack as described above, can all run in a parallelized, distributed, and optionally high available setup. There are however extra requirements for some of the building blocks. The ingress web server (Traefik) can run multiple instances, but needs a way to sync TLS certificates and route information. The Varnish server can be run multiple times, but purge requests for changed/stale contenct, will need to be multiplied to all cache instances.

The Plone frontend and backend servers can and should run with multiple instances in a larger setup to offer enough throughput. Lastly, the database should be dimensioned large enough to support al storage/retrieve requests from the Backends. When high availability is required, the database layer should be set up with Relstorage and a Relational Database that is configured accordingly (for example primary/secondary with active failover, or a a three node DB cluster). 

