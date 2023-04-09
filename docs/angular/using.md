---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using And Customizing The Angular Plone Components

## Preparing The Plone Backend

We need a Plone server running the latest version of {doc}`Plone REST API <plone6docs:plone.restapi/docs/source/index>`.

We will use a [Plone pre-configured Heroku instance](https://github.com/collective/training-sandbox).

Once deployed, create a Plone site, then go to the {menuselection}`Site Setup --> Add-ons` and {guilabel}`Install` Plone RESTAPI.

It will also be helpful for development to turn off [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing).
There are many ways to do that.  For example, in Google Chrome we can install an [extension Allow CORS: Access-Control-Allow-Origin](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf?hl=en-US) that takes care of it. For Firefox you can use the [CORS Everywhere add-on](https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/)

## Adding The @plone/restapi-angular Dependency

```shell
npm install @plone/restapi-angular --save
```

The `@plone/restapi-angular` and its own dependencies have been installed in our `./node_modules` folder.

```{note}
the `--save` option ensures the dependency is added in our `package.json`.
```

We are now ready to use the Plone Angular SDK.

## Connecting The Project To The Plone Backend

In `src/app/app.module.ts`, load the Plone module and set the backend URL:

```ts
import { RESTAPIModule } from '@plone/restapi-angular';

...

@NgModule({
  ...
  imports: [
    ...
    RESTAPIModule,
  ],
  providers: [
    {
      provide: 'CONFIGURATION', useValue: {
        BACKEND_URL: 'http://whatever.herokuapp.com/Plone',
      }
    },
  ],
  ...
```

```{warning}
Make sure to use `http` and not `https` because the Heroku web configuration is not set up properly for that.
```

We have to set up the default Plone views for traversal in `src/app/app.component.ts`:

```ts
 import { Component } from '@angular/core';
 import { PloneViews } from '@plone/restapi-angular';

 @Component({
 ...
 })
 export class AppComponent {

 constructor(
  public views:PloneViews,
 ) {
   this.views.initialize();
 }
}
```

We need to insert the Plone view in our main page. Let's change `src/app/app.component.html` this way:

```html
<traverser-outlet></traverser-outlet>
```

Now, traversing is active, so we can visit the following links:

- `http://localhost:4200/front-page`
- `http://localhost:4200/news`
- `http://localhost:4200/events`

Despite our very bad looking rendering, any content stored in our Plone backend can be requested locally.

The same goes for default views, like:

- `http://localhost:4200/@@sitemap`
- `http://localhost:4200/news/@@search?SearchableText=News`

We are also able to use Plone components provided by the SDK.
Let's change again `src/app.component.html`:

```html
<plone-global-navigation></plone-global-navigation>
<plone-breadcrumbs></plone-breadcrumbs>
<traverser-outlet></traverser-outlet>
```

Now we get the main navigation bar and the breadcrumbs. Note the navigation is performed client-side (the page is not reloaded).
