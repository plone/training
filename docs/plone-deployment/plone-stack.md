---
myst:
  html_meta:
    "description": "Introduction to Plone stack for deployment"
    "property=og:description": "Introduction to Plone stack for deployment"
    "property=og:title": "Introduction to Plone stack for deployment"
    "keywords": "Plone, deployment, stack"
---

# Introduction to Plone stack

The basic Plone stack consists out of different parts.

This training show the stack for a modern Plone 6 site with a ReactJS powered frontend.
If it comes you need to deploy a Plone Classic UI site, with server side HTML rendering, the frontend part is omitted.

This architecture allows horizontal scaling where it is with most needed, on the rendering of HTML and JSON.

In this training we skip installing a reverse caching proxy between webserver and Plone nor we show setting up an edge caching service.

## Webserver

Listening on ports 80 and 443, proxy requests to the Plone Frontend and Plone Backend.

The webserver job is to route and rewrite HTTP requests to the frontend and backend and is responsible for TSL termination.
We recommend either Nginx or Traefik, but other capable webservers work too.

## Plone Frontend

Node HTTP-server running on port 3000, hosts the default user interface for Plone.
This process needs to have access to the Plone Backend service.

## Plone Backend

WSGI process running on port 8080, is the HTTP-server with Plone API.

Even though it's possible to run it without a specialized database, it's better you to point to either a ZEO server or a relational database.
Supported relational databases are Postgresql, MySQL/MariaDB and Oracle.
If a ZEO-server is used - and only then - a separate shared file system is needed to store binary data (blobs).

This process need to have access to the database service.

## Database

The storage as a specialized database layer.
It can be a simple file storage, which does not scale.
It could be either a ZEO server or a relational database for scalable production setups.
It stores content and binary data (relational database).

# Basic Setup

All services running on the same server.

## Without a specialized database

Webserver -> Plone Frontend -> Plone Backend (file storage).

```{note}
This is recommended only for demo sites and trying out Plone.
```

## With a specialized database

Webserver → Plone Frontend → Plone Backend → Database

# Multi-server Setup

Different constallations are possible.
In a multiserver setup load can distributed and reduncacy can be added through horizontal scaling.

## Webserver and Frontend

### Both on one machine

Externally accessible on ports 80 and 443

Hosts web server and Plone Frontend processes.

### Both separated on own machines

- Webserver on own machine.
- Frontend on other machine(s) thus it can scale.

## Plone Backend

Hosts Plone Backend processes, listening on port 8080, made to scale.

## Database server

Hosts either a Zeo server or a relational database.
Most hosting providers offer managed relational database services with proper backup and replication, you should consider this as a primary option if you're not familiar with database management.
If you do not have this option we recommend to use Postgresql.
