---
myst:
  html_meta:
    "description": "Introduction to Plone stack for deployment"
    "property=og:description": "Introduction to Plone stack for deployment"
    "property=og:title": "Introduction to Plone stack for deployment"
    "keywords": "Plone, deployment, stack"
---

# Introduction to Plone stack

The basic Plone stack consists of several parts.

This training showcases the stack of a modern Plone 6 site with a ReactJS powered frontend.
If you need to deploy a Plone Classic UI site with server side template HTML rendering, the frontend part can be omitted.

This architecture allows horizontal scaling where it is most needed, specifically for the rendering of HTML and JSON.

In this training we skip installation of a reverse caching proxy between the web server and Plone, nor do we show how to set up an edge caching service.

## Web server

The web server listens on ports 80 and 443, and proxies requests to the Plone frontend and Plone backend.

The web server's job is to route and rewrite HTTP requests to the frontend and backend, and is responsible for TLS termination.
We recommend either Nginx or Traefik, but other capable web servers work, too.

## Plone frontend

The Node HTTP server running on port 3000 hosts the default user interface for Plone.
This process needs to have access to the Plone backend service.

## Plone backend

The WSGI process running on port 8080 is the HTTP server with Plone API.

Even though it's possible to run it without a specialized database, it's better that you point to either a ZEO server or a relational database.
Supported relational databases are PostgreSQL, MySQL/MariaDB, and Oracle.
If a ZEO server is used—and only then—a separate shared file system is needed to store binary data as blobs.

This process needs to have access to the database service.

## Database

The storage as a specialized database layer.
It can be simple file storage, which does not scale.
It could be either a ZEO server or a relational database for scalable production setups.
It stores content and binary data in a relational database.

# Basic setup

All services will run on the same server.

## Without a specialized database

Web server → Plone frontend → Plone backend (file storage).

```{note}
This is recommended only for demo sites and trying out Plone.
```

## With a specialized database

Web server → Plone frontend → Plone backend → Database

# Multiple server setup

Different configurations are possible.
In a multiple server setup, load can be distributed and redundancy can be added through horizontal scaling.

## Web server and frontend

### Both on one machine

The web server is externally accessible on ports 80 and 443.

This configuration hosts both the web server and the Plone frontend processes.

### Both separated on own machines

The web server is on its own machine.

The frontend is on other machine(s), thus it can scale.

## Plone backend

This machine hosts the Plone backend processes, listening on port 8080, and may scale.

## Database server

The database server hosts either a ZEO server or a relational database.
Most hosting providers offer managed relational database services with proper backup and replication.
You should consider this as a primary option if you're not familiar with database management.
If you do not have this option, we recommend that you use PostgreSQL.
