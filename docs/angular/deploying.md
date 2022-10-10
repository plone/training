---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Deployment

The development bundle served by `ng serve` is not optimized for production.

To get a production-ready bundle, we use the following command:

```shell-session
$ ng build --prod
```

The resulting bundle is generated in the `./dist` folder.

It is just a set of static files and can be served by any HTTP server.

Let's say we deploy it on <http://example.com> and we use Nginx to serve the files.

If we visit <http://example.com>, we will see our home page, and if we click on `News`,
we will obtain <http://example.com/news> thanks to angular-traversal.

But if decide to refresh the page at this point, we will get a 404, because our Nginx server will search for `/news/index.html` which does not exist.

So we need to fix our Nginx VHOST to preserve the client-side routing:

```
location / {
  try_files   $uri $uri/ /index.html;
}
```

This way, any existing file (like `index.html`, `vendor.xxx.bundle.js`, etc.) is served directly, but for anything else, we just return `index.html` so the client-side routing will take over.
