---
myst:
  html_meta:
    "description": "CORS"
    "property=og:description": "CORS"
    "property=og:title": "CORS"
    "keywords": "Volto, Plone, CORS, browser"
---

# CORS

(CORS)=

From MDN:

> Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism that allows a server to indicate any origins (domain, scheme, or port) other than its own from which a browser should permit loading resources. CORS also relies on a mechanism by which browsers make a "preflight" request to the server hosting the cross-origin resource, in order to check that the server will permit the actual request. In that preflight, the browser sends headers that indicate the HTTP method and headers that will be used in the actual request.

An example of a cross-origin request: the front-end JavaScript code served from `https://domain-a.com` uses XMLHttpRequest to make a request for `https://domain-b.com/data.json`.

Plone 6 Volto and Plone 6 backend communicate with each other using XHR requests, and since the fronted is a pure JavaScript application, it has to comply with CORS rules.
This is valid at all times, no matter if you are in development or in a production enviroment. But if you use Volto Seamless mode for deployment (where the plone.restapi endpoints are exposed under the same domain as the frontend) then the browser is not affected by CORS issues, as the requests come from the same domain.

Plone has a way to configure the CORS headers in order to allow domains to access it.

```
zcml-additional =
  <configure xmlns="http://namespaces.zope.org/zope"
            xmlns:plone="http://namespaces.plone.org/plone">
  <plone:CORSPolicy
    allow_origin="http://localhost:3000,http://127.0.0.1:3000"
    allow_methods="DELETE,GET,OPTIONS,PATCH,POST,PUT"
    allow_credentials="true"
    expose_headers="Content-Length,X-My-Header"
    allow_headers="Accept,Authorization,Content-Type,X-Custom-Header,Origin,Lock-Token"
    max_age="3600"
    />
  </configure>
```

However, the recommendation is that you forget that CORS exists and "play well" to avoid the scenario where configuring and enabling CORS headers is the way to proceed.

These scenarios are:

- Our frontend and backend are in the same domain (thus, avoiding the cross-domain issue), or
- Using the internal proxy provided by Volto's Node.js SSR server

During development, the last one is the one you are going to use.
The default backend will live in `http://localhost:8080/Plone` and the frontend in `http://localhost:3000`. If your Plone site is not named `Plone` (so its url is something like `http://localhost:8080/mysite`, you can still use Seamless mode by creating a file called `.env.development` in the Volto project root with something like this:

```
RAZZLE_DEV_PROXY_API_PATH=http://localhost:8080/mysite
```

In production, you'll probably will be using Volto's Seamless mode, so you won't be defining any custom `API_PATH` but using `++api++` traversal, and reverse proxying it through your webserver.
