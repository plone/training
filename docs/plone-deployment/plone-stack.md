---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Intro To Plone Stack

## Webserver

Listening on ports 80 and 443, proxy requests to the Plone Frontend and Plone Backend.

## Plone Frontend

Node server running on port 3000, hosts the default user interface for Plone. This process needs to have access to the Plone Backend service.

## Plone Backend

WSGI process running on port 8080, is the the server with Plone API. Even though it is possible to run it without a specialized database, we recommend you to point to either a ZEO server or a relational database.

## Database

Specialized database layer. It could be either a ZEO server or a relational database.


# Simple Setup

All services running on the same server

## Without a specialized database

Webserver -> Plone Frontend -> Plone Backend 

## With a specialized database

Webserver -> Plone Frontend -> Plone Backend -> Database

# Multi-server

## Webserver and Frontend

Externally accessible on ports 80 and 443

Hosts webserver and Plone Frontend processes.

## Plone Backend

Hosts Plone Backend processes, listening on port 8080

## Database server

Hosts either a Zeo server or a relational database.
Most hosting providers offer managed relational database services with proper backup and replication, you should consider this as a primary option if you are not familiar with database management.

