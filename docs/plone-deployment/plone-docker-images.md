---
myst:
  html_meta:
    "description": "Plone Docker images for deployment"
    "property=og:description": "Plone Docker images for deployment"
    "property=og:title": "Plone Docker images for deployment"
    "keywords": "Plone, deployment, Docker, images"
---

# Plone Docker Images

For Plone 6, the community is revamping our Docker images -- and offering more base options.

## plone/plone-frontend

Repository available at [https://github.com/plone/plone-frontend/](https://github.com/plone/plone-frontend/)

Installs the Plone 6 default user-experience (Using the React-powered frontend: Volto).

Should be used to showcase the default Plone 6 experience, as new projects will probably implement their own Docker images (with a similar Dockerfile)

## plone/plone-backend

Repository available at [https://github.com/plone/plone-backend/](https://github.com/plone/plone-backend/)

Installs the Plone 6 backend using a pip-based installation.
This approach makes it easier and faster to extend this image in your own project.

One example of such extension would be

```Dockerfile
FROM plone/plone-backend:6.0.0b3

RUN ./bin/pip install "pas.plugins.authomatic"
```

## plone/plone-zeo

Repository available at [https://github.com/plone/plone-zeo/](https://github.com/plone/plone-zeo/)

Installs a ZEO database server.
