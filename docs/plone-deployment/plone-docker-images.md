---
myst:
  html_meta:
    "description": "Plone Docker images for deployment"
    "property=og:description": "Plone Docker images for deployment"
    "property=og:title": "Plone Docker images for deployment"
    "keywords": "Plone, deployment, Docker, images"
---

# Plone Docker Images

For Plone 6, the community has overhauled its Docker images, and offers more base options.

## plone/plone-frontend

Its repository is available at https://github.com/plone/plone-frontend/.

It installs the Plone 6 default user experience, using the React-powered frontend Volto.

It should be used to showcase the default Plone 6 experience, as new projects will probably implement their own Docker images using a similar Dockerfile.

## plone/plone-backend

Its repository is available at https://github.com/plone/plone-backend/.

It installs the Plone 6 backend using a `pip`-based installation.
This approach makes it easier and faster to extend this image in your own project.

One example of such extension would be the following.

```Dockerfile
FROM plone/plone-backend:6.0.0

RUN ./bin/pip install "pas.plugins.authomatic"
```

## plone/plone-zeo

Its repository is available at https://github.com/plone/plone-zeo/.

It installs a ZEO database server.
