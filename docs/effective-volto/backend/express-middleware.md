---
myst:
  html_meta:
    "description": "Writing Express middleware"
    "property=og:description": "Writing Express middleware"
    "property=og:title": "Writing Express middleware"
    "keywords": "Volto, Plone, Express, JavaScript, Backend"
---

# Writing Express middleware

When working with Volto projects, we consider the backend to be Plone. But we
actually have another backend, the Volto Nodejs HTTP server, which is based on
the popular [Express](https://expressjs.com/) web framework. Volto, the SSR
server is an Express app, and we can extend that app with new capabilities.

Express extensions are usually written a **Express middleware** for routes
(URL matchers) and Volto already comes with several of them, useful in
proxy-ing some of Plone's browser views (for example the `@@images` or
`robots.txt`, `sitemap.xml.gz`, etc).

Here's, as an example, the Sitemap middleware:

```
import express from 'express';
import { generateSitemap } from '@plone/volto/helpers';

export const sitemap = function (req, res, next) {
  generateSitemap(req).then((sitemap) => {
    if (Buffer.isBuffer(sitemap)) {
      res.set('Content-Type', 'application/x-gzip');
      res.set('Content-Encoding', 'gzip');
      res.set('Content-Disposition', 'attachment; filename="sitemap.xml.gz"');
      res.send(sitemap);
    } else {
      // {"errno":-111, "code":"ECONNREFUSED", "host": ...}
      res.status(500);
      // Some data, such as the internal API address, may be sensitive to be published
      res.send(`Sitemap generation error: ${sitemap.code ?? '-'}`);
    }
  });
};

export default function () {
  const middleware = express.Router();

  middleware.all('**/sitemap.xml.gz', sitemap);
  middleware.id = 'sitemap.xml.gz';
  return middleware;
}
```

Notice that this code should not get into the client bundle, so you should
load it conditionally by placing it in a separate module.


```
export default applyConfig(config) {
  if (__SERVER__) {
    const makeMiddleware = require('./mymiddleware');
    const middleware = makeMiddleware();
    config.settings.expressMiddleware.push(middleware);
  }

  return config;
}
```

An example of a Volto addon that implements an Express middleware is the
[volto-corsproxy](https://github.com/eea/volto-corsproxy/).
