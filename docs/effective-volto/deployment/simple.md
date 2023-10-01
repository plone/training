---
myst:
  html_meta:
    "description": "Simple deployment of a Volto application"
    "property=og:description": "Simple deployment of a Volto application"
    "property=og:title": "Simple deployment"
    "keywords": "Volto, Plone, frontend, React, deployment"
---

# [DEPRECATED] Old (pre-seamless mode) deployment

Volto is a Node application that runs on your machine/server and listens to a port. Once you are ready to deploy it, you should build it running:

```bash
yarn build
```

```{note}
It is recommended that you deploy your Plone 6 Volto frontend part using Seamless mode.
This allows you to build once, deploy everywhere, using runtime environment variables whenever necessary to configure your app.
```

Once the build is complete, the bundle is created in `./build` folder.
Then in order to launch your application you can run:

```bash
yarn start:prod
```
or
```bash
NODE_ENV=production node build/server.js
```

This will start Volto in the PORT and `RAZZLE_API_PATH` by default (`PORT=3000`, `RAZZLE_API_PATH=http://localhost:8080/Plone`).
If you are using Seamless mode, the `RAZZLE_API_PATH` will be auto-configured using the HOST headers present in the request.
You can specify your own at runtime by issuing the run command with these variables present:

```bash
PORT=4000 RAZZLE_API_PATH=https://plone.org/api yarn start:prod
```

The simplest deployment is to start this node process in your server by any mean of your choice (systemd, process manager, etc) and manage its lifecycle through it.

The Official Plone 6 Volto documentation has page on `pm2`: https://6.docs.plone.org/volto/deploying/pm2.html

## Reverse proxies

You need to make available to your users both Volto and the API in public URLs. It's heavily recommended you serve both from the same DNS name, eg. Volto-> `https://mywebsite.com` and API-> `https://mywebsite.com/api` in order to avoid any CORS problem.

```{warning}
Avoid dealing with CORS in production at all costs. Period.
```

For SSL support is recommended to use a reverse proxy of your choice that points to Volto port and an API rewrite eg. `++api++` in your server. This is the nginx configuration for Seamless mode:

```nginx
upstream backend {
    server host.docker.internal:8080;
}
upstream frontend {
    server host.docker.internal:3000;
}

server {
  listen 80;
  server_name myservername.org;

  client_max_body_size 1G;

  access_log /dev/stdout;
  error_log /dev/stdout;

  # [seamless mode] Recomended as default configuration, using seamless mode new plone.rest traversal
  # yarn build && yarn start:prod
  location ~ /\+\+api\+\+($|/.*) {
      rewrite ^/\+\+api\+\+($|/.*) /VirtualHostBase/http/myservername.org/Plone/++api++/VirtualHostRoot/$1 break;
      proxy_pass http://backend;
  }

  # Legacy deployment example, using RAZZLE_LEGACY_TRAVERSE Volto won't append ++api++ automatically
  # Recommended only if you can't upgrade to latest `plone.restapi` and `plone.rest`
  # yarn build && RAZZLE_API_PATH=http://myservername.org/api RAZZLE_LEGACY_TRAVERSE=true yarn start:prod
  # location ~ /api($|/.*) {
  #     rewrite ^/api($|/.*) /VirtualHostBase/http/myservername.org/Plone/VirtualHostRoot/_vh_api$1 break;
  #    proxy_pass http://backend;
  # }

  location ~ / {
      location ~* \.(js|jsx|css|less|swf|eot|ttf|otf|woff|woff2)$ {
          add_header Cache-Control "public";
          expires +1y;
          proxy_pass http://frontend;
      }
      location ~* static.*\.(ico|jpg|jpeg|png|gif|svg)$ {
          add_header Cache-Control "public";
          expires +1y;
          proxy_pass http://frontend;
      }

      proxy_set_header        Host $host;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;
      proxy_redirect http:// https://;
      proxy_pass http://frontend;
  }
}
```

### Understanding CORS errors

If you're getting [CORS errors](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors#identifying_the_issue) you need to understand the nature of these errors: the backend server (usually Plone) needs to be configured to "know" the final domain where the content is fetched. This is done for security purposes, to protect the information in the backend server from being loaded by client browsers on unknown domains. So make sure that the backend server is properly configured for your purposes. When using Plone with Docker, check the [CORS](https://github.com/plone/plone.docker#for-basic-usage) documentation section, otherwise the [CORS section of plone.rest](https://github.com/plone/plone.rest#cors).

For more information {doc}`../architecture/CORS`.
