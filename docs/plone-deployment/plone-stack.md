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
This guide won’t cover the integration of a web accelerator or the setup of an edge caching service.

## Components of the Plone Stack

### Webserver

The webserver, accessible externally on ports 80 and 443, handles the routing and rewriting of HTTP requests to the Plone frontend and backend, and is tasked with TLS termination. While {term}`Nginx` and {term}`Traefik` are recommended, other webservers can also be employed. This training will exclusively utilize Traefik.

### Web Accelerator

{term}`Varnish`, a web accelerator, is positioned between the external webserver and internal services to cache dynamically generated content. For a detailed Plone setup with Varnish, refer to the [volto-caching](https://github.com/collective/volto-caching) repository.

### Plone Frontend

Hosted on a Node HTTP-server running on port 3000, the Plone frontend constitutes the default user interface and requires access to the Plone Backend and the webserver.

### Plone Backend

Operating on port 8080, the Plone Backend, a WSGI process, serves as the HTTP server hosting the Plone API. It’s optimal to pair it with a specialized database like ZEO server or a relational database via RelStorage, supporting PostgreSQL, MySQL/MariaDB, and Oracle. A separate shared file system is essential for storing binary data if ZEO is employed.

### Database

The database layer can range from a simple ZODB with file storage to more scalable options like a ZEO server or a relational database. This training will focus on using a PostgreSQL instance.

## Deployment Configurations

### Basic Setup

#### Without Specialized Database

```
Webserver -> Plone Frontend -> Plone Backend (file storage).
```

```{note}
Ideal for demo sites and Plone trials.
```

#### With Specialized Database

```
Webserver → Plone Frontend → Plone Backend → Database
```

```{note}
Solution to be presented in this training.
```

#### With Specialized Database and Caching

```
Webserver → Web Accelerator → Plone Frontend → Plone Backend → Database
```

### Multi-server Setup

In a multi-server environment, load distribution and redundancy are achieved through various configurations, enabling horizontal scaling.

```{figure} _static/request_flow.png
:alt: Flow of a request to https://example.com

Flow of a request to https://example.com
```

#### Webserver and Web Accelerator Layer

Externally accessible machine hosting both the webserver and web accelerator on ports 80 and 443.

#### Plone Application Layer (Frontend and Backend)

Hosts scalable Plone Frontend and Backend processes, enhancing performance and responsiveness.

#### Database Layer

Can host a ZEO server or a relational database. Managed relational database services with backup and replication are
recommended for those unfamiliar with database management, with PostgreSQL being a preferred choice.
