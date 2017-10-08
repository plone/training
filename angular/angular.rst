=====================
Angular SDK For Plone
=====================

In this part you will:

* Create a static site with Angular,
* Display contents stored in Plone and retrieved using the REST API,
* Use the Angular default Plone components and views,
* Extend those components.

Topic covered:

* Plone Angular SDK.

What Is Angular
===============

`Angular <https://angular.io/>`_ is a JavaScript framework released in 2016.

- It is component-oriented.
- It is shipped with RxJS, the Reactive Programming library.
- It works with TypeScript, a superset of EcmaScript 6, which allows a cleaner coding.
- It provides a powerful CLI to build projects.

For these reasons it is a very good framework which is both powerful and easy to use.

.. note::

   Angular was initially known as Angular 2 as AngularJS was its ancestor.
   Angular and AngularJS are very different.

   Their names are quite close, when looking for packages,
   verify carefully which Angular it is compliant with.

What Is The Plone Angular SDK
=============================

The `Plone Angular SDK <https://www.npmjs.com/package/@plone/restapi-angular>`_ is an Angular
package (named ``@plone/restapi-angular`` as it belongs to the Plone NPM organization).

It is a high-level integration layer between Angular and the `Plone REST API <https://plonerestapi.readthedocs.io/en/latest/introduction.html>`_.

It provides:

- services to dialog with the Plone backend,
- ready-to-use components (for instance ``<plone-navigation>`` or ``<plone-breadcrumbs>``),
- traversing.

Traversing
----------

Traversing is a key feature when working with a CMS.
Angular core, like the other major JS frameworks, uses routing.
Routing works perfectly for applications, but it is not suitable for web sites (as the site structure is not predictable).

The Traversal service implemented by `Angular traversal <https://github.com/makinacorpus/angular-traversal>`_ replaces the default Angular routing.

It uses the current location to determine the backend resource (the **context**) and the desired rendering (the **view**).

The view is the last part of the current location and is prefixed by ``@@``.
If no view is specified, it defaults to ``view``.

The rest of the location is the resource URL.

Example: ``/news/what-about-traversal/@@edit``

When traversing to the location, the resource will be requested from the backend,
and the result will become the current context, accessible from any component in the app.

According to the value of the ``@type`` property of the context, the appropriate component will be used to render the view.

.. note::

   We can also use another criteria than ``@type`` by registring a custom marker
   (the package comes with an ``InterfaceMarker`` which marks context according the ``interfaces`` attribute,
   which is supposed to be a list.

   (At the moment, the Plone REST API does not expose this attribute).

A New Integration Approach For Plone
====================================

Creating pure frontend applications to publish Plone-managed information rather than customizing the Plone web interface has several benefits:

- those web sites look better and fit the expectations of today's visitors and customers,
- they are faster and can work offline, which makes them more suitable for mobile,
- frontend development is more approachable than Plone development, and a constantly growing amount of web developers master this kind of technology.

Installing The Development Environment
======================================

First, we need NodeJS 6.10+. We recommend to use nvm to install NodeJS instead of using your OS-based version.

Install nvm on your system using the instructions and provided script at:

https://github.com/creationix/nvm#install-script

Using nvm we will look up the latest lts version of NodeJS and install it

.. code-block:: console

   nvm ls-remote --lts
   nvm install v6.10
   nvm use v6.10

NodeJS is provided with npm, its package manager, we will use it to install the Angular CLI (ng)

.. code-block:: console

   npm install -g @angular/cli@latest

.. note:: ``-g`` means the CLI will be available globally in our nvm instance.

Initializing A New Project
==========================

The CLI allows to initialize a project:

.. code-block:: console

   ng new training --style=scss

.. note:: ``--style=scss`` indicates we will use SCSS for stylesheets.

If we inspect our newly created ``./training``, we see a default Angular project structure:

- the sources are managed in the ``./src`` folder,
- the dependencies are declared in ``package.json``,
- and they are installed in the ``./node_modules`` folder.

We can serve our project locally using the CLI.

.. code-block:: console

   cd ./training
   ng serve

The result can be seen on http://localhost:4200.

This development server offers the different features we can expect for a convenient frontend developement environment
like autoreload and sourcemaps.

The CLI also allows to run the tests:

.. code-block:: console

   ng test

Using And Customizing The Angular Plone Components
==================================================

Preparing The Plone Backend
---------------------------

We need a Plone server running the latest version of `plone.restapi <http://plonerestapi.readthedocs.io>`_ .

We will use a `Plone pre-configured Heroku instance <https://github.com/collective/training-sandbox>`_.

Once deployed, create a Plone site, then go to the :menuselection:`Site Setup --> Add-ons` and :guilabel:`Install` Plone RESTAPI.

Adding The @plone/restapi-angular Dependency
--------------------------------------------

.. code-block:: console

   npm install @plone/restapi-angular --save

The ``@plone/restapi-angular`` and its own dependencies have been installed in our ``./node_modules`` folder.

.. note:: the ``--save`` option ensures the dependency is added in our ``package.json``.

We are now ready to use the Plone Angular SDK.

Connecting The Project To The Plone Backend
-------------------------------------------

In ``src/app/app.module.ts``, load the Plone module and set the backend URL:

.. code-block:: ts

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

.. warning::

   Make sure to use ``http`` and not ``https`` because the Heroku web configuration is not set up properly for that.

We have to set up the default Plone views for traversal in ``src/app/app.component.ts``:

.. code-block:: ts

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

We need to insert the Plone view in our main page. Let's change ``src/app/app.component.html`` this way:

.. code-block:: html

   <traverser-outlet></traverser-outlet>

Now, traversing is active, so we can visit the following links:

- ``http://localhost:4200/front-page``
- ``http://localhost:4200/news``
- ``http://localhost:4200/events``

Despite our very bad looking rendering, any content stored in our Plone backend can be requested locally.

The same goes for default views, like:

- ``http://localhost:4200/@@sitemap``
- ``http://localhost:4200/news/@@search?SearchableText=News``

We are also able to use Plone components provided by the SDK.
Let's change again ``src/app.component.html``:

.. code-block:: html

   <plone-global-navigation></plone-global-navigation>
   <plone-breadcrumbs></plone-breadcrumbs>
   <traverser-outlet></traverser-outlet>

Now we get the main navigation bar and the breadcrumbs. Note the navigation is performed client-side (the page is not reloaded).

Integrating A Theme
===================

Integrate Bootstrap
-------------------

Add the bootstrap dependency:

.. code-block:: console

   npm install bootstrap-sass@~3.3.7 --save

Create a file to manage our SCSS variables: ``src/variables.scss``

.. code-block:: scss

   $blue: #50c0e9;
   $lightgrey: #f9f9f9;

Import Bootstrap in our main stylesheet ``src/styles.scss``

.. code-block:: scss

   @import "variables.scss";

   $icon-font-path: "../node_modules/bootstrap-sass/assets/fonts/bootstrap/";
   @import "../node_modules/bootstrap-sass/assets/stylesheets/_bootstrap.scss";

Override A default Plone Component Template
===========================================

We need to change the template of the global navigation.

First we need to generate a new component

.. code-block:: console

   ng generate component global-navigation

The CLI creates a new folder containing the component implementation, and it declares it in ``src/app/app.module.ts``.

Our global navigation needs to inherit from Plone's own:

``src/app/global-navigation/global-navigation.component.ts``:

.. code-block:: ts

   import { Component } from '@angular/core';
   import { GlobalNavigation } from '@plone/restapi-angular';

   @Component({
     selector: 'app-global-navigation',
     templateUrl: './global-navigation.component.html',
     styleUrls: ['./global-navigation.component.scss']
   })
   export class GlobalNavigationComponent extends GlobalNavigation {}

And now we can set the template we need:

``src/app/global-navigation/global-navigation.component.html``:

.. code-block:: html+ng2

   <nav class="navbar navbar-default" role="navigation">
     <div class="container-fluid">
       <div class="navbar-header">
         <div class="navbar-brand">
           <a traverseTo="/">
             <h1>Plone conference</h1>
           </a>
         </div>
       </div>
       <div class="menu">
         <ul class="nav nav-tabs" role="tablist">
           <li *ngFor="let link of links" [ngClass]="{'active': link.active}">
             <a [traverseTo]="link.path">{{ link.title }}</a>
           </li>
         </ul>
       </div>
     </div>
   </nav>

Style it in :file:`src/app/global-navigation/global-navigation.component.scss`:

.. code-block:: scss

    @import "../../variables.scss";

    .navbar-default {
      background-color: white;
      border-radius:0;
      border-right:0;
      border-left:0;
      border-top:0;
    }

    .container-fluid > .navbar-header {
      margin-right: 30px;
      margin-left: 10px;
      margin-top:20px;
      border-radius:0;
    }

    .navbar-brand {
      float: left;
      height: 30px;
      padding: 15px 15px;
      font-size: 18px;
      line-height: 20px;
      h1 {
        float: left;
        line-height:20px;
        padding: 20px;
        font-size: 30px;
        margin-top:-23px;
        color: $blue;
        &:hover {
          background-color:white;
        }
      }
    }

    .menu {
      font-size:14px;
      float:right;
      text-transform:uppercase;
      font-weight:600;
      ul.nav-tabs li {
        color: black;
      }
    }

    .nav-tabs {
      border-bottom: 0;
      & > li {
        float: left;
        margin-bottom: 0;
        & > a {
          margin-top:20px;
          margin-bottom:20px;
          margin-right: 20px;
          line-height: 1.42857143;
          border-bottom: 3px solid transparent;
          border-radius:0;
          color: black;
          border-top:0;
          border-right:0;
          border-left:0;
          & > a:hover {
            border-color: #eee #eee $blue;
            color: $blue;
            border-radius:0;
            background-color: $lightgrey;
          }
        }
        &.active {
          & > a,
          & > a:hover,
          & > a:focus {
            color: white;
            cursor: default;
            background-color: $blue;
            border: 0;
            border-bottom-color: transparent;
            cursor:pointer;
          }
        }
      }
    }

Update The App Component Markup
-------------------------------

Now we can fix the main component markup in ``src/app/app.component.html``:

.. code-block:: html

   <header>
     <div class="container-fluid">
       <div class="row">
         <app-global-navigation></app-global-navigation>
       </div>
     </div>
     <div class="container-fluid">
       <div class="row">
         <plone-breadcrumbs></plone-breadcrumbs>
       </div>
     </div>
   </header>
   <main>
     <div class="container-fluid">
       <div class="row">
         <traverser-outlet></traverser-outlet>
       </div>
     </div>
   </main>

Note we use our custom global navigation component (``app-global-navigation``)
but we keep the Plone default breadcrumbs component (``plone-breadcrumbs``) as its markup is fine.

We need to style it a little bit, let's do that in :file:`src/styles.scss`:

.. code-block:: scss

   *[traverseTo], *[ng-reflect-traverse-to] {
     cursor: pointer;
   }

   a, a:hover, a:focus {
     color: $blue;
   }

   .breadcrumb {
     background-color: transparent;
     & > .active {
       color: black;
     }
   }

Creating A Custom View For The Talk Content Type
================================================

Create The Talk Content Type In The Backend
-------------------------------------------

We need to go to our Plone backend, then in :menuselection:`Site Setup --> Dexterity content types`,
we add a new content type named Talk.

We add a text field named ``speaker``.

And we select the following behaviors:

- Lead image
- Rich text

Then we create a new folder named "Talks" where we add a few talks, and we publish them all (including the folder).

Create A View Component For Talks
---------------------------------

We could use the default view to display talks, but it would only display the title and the text,
and we would like to also display the image and the speaker.

Let's generate a new component with the CLI

.. code-block:: console

   ng generate component talk

To turn it into a valid view component, there are 3 steps:

- declare it in the module's ``entryComponents``,
- inherit from a Plone view component,
- register the view for traversal.

In ``app.module.ts``, we can see the CLI has already added ``TalkComponent`` in ``declarations`` which is mandatory
for any Angular component.

But as a view component is dynamically instantiated (depending on the traversed path), we also need to add it in ``entryComponents``:

.. code-block:: ts

   @NgModule({
     declarations: [
       AppComponent,
       GlobalNavigationComponent,
       TalkComponent
     ],
     entryComponents: [
       TalkComponent,
     ],
     ...

Now let's change ``src/app/talk/talk.component.ts`` to inherit from ``ViewView``:

.. code-block:: ts

   import { Component } from '@angular/core';
   import { ViewView } from '@plone/restapi-angular';

   @Component({
     selector: 'app-talk',
     templateUrl: './talk.component.html',
     styleUrls: ['./talk.component.scss']
   })
   export class TalkComponent extends ViewView {}

And lastly, let's associate this component to the ``talk`` content type as its default view in ``src/app/app.component.ts``:

.. code-block:: ts

   ...
   import { Services } from '@plone/restapi-angular';
   import { TalkComponent } from './talk/talk.component';

   @Component({
   ...
   })
   export class AppComponent {
     constructor(
       public views: PloneViews,
       public plone: Services,
     ) {
       this.views.initialize();
       this.plone.traverser.addView('view', 'talk', TalkComponent);
     }
   }

The view is now properly set up, let's work on the template in ``src/app/talk/talk.component.html``:

.. code-block:: html+ng2

   <div class="col-md-6">
     <img [src]="context.image.scales.large.download" alt="Illustration" />
   </div>
   <div class="col-md-6">
     <h1>{{ context.title }}</h1>
     <p>
       <span class="glyphicon glyphicon-user"></span>
       {{ context.speaker }}
     </p>
     <div [innerHTML]="context.text.data"></div>
   </div>

Enable Comments
---------------

We want to allow visitors to post comments about the talks.

In the Plone backend, in :menuselection:`Site Setup --> Discussion`, we activate comments globally and we allow anonymous comments.

In :menuselection:`Site Setup --> Content Settings`, we select the Talk type, and we allow comments.

Now in ``src/app/talk/talk.component.html`` we just append:

.. code-block:: html+ng2

   <plone-comments></plone-comments>

Displaying News On The Home Page
================================

We want to display the 3 most recent news on the home page.

First we need a Home component. Let's initialize it properly.

..  admonition:: Solution
  :class: toggle

    We use the CLI:

    .. code-block:: console

       ng generate component home

    Then we add  ``HomeComponent`` in  ``entryComponents`` in the module.

    We declare it as a view for the ``Plone Site`` type in ``AppComponent``:

    .. code-block:: ts

        import { HomeComponent } from './home/home.component';

        ...

        this.traverser.addView('view', 'Plone Site', HomeComponent);


We want this component to display the 3 most recent news.
The ``resource`` service from ``@plone/restapi-angular`` provides a ``find`` method to do that.

Here is the ``HomeComponent`` implementation:

.. code-block:: ts

   import { Component, OnInit } from '@angular/core';
   import { ViewView } from '@plone/restapi-angular';

   @Component({
     selector: 'app-home',
     templateUrl: './home.component.html',
     styleUrls: ['./home.component.scss']
   })
   export class HomeComponent extends ViewView implements OnInit {

     news: any[] = [];

     ngOnInit() {
       this.services.resource.find(
         { portal_type: 'News Item' },
         '/',
         {
           sort_on: 'created',
           sort_order: 'reverse',
           size: 3,
         },
       ).subscribe(res => {
         this.news = res.items;
       });
     }
   }

We could display those news with a basic layout like this:

.. code-block:: html+ng2

   <ul>
     <li *ngFor="let item of news">
       <a [traverseTo]="item['@id']">{{ item.title }}</a>
     </li>
   </ul>

Titles are not enough, it would be better to display images.

The ``find`` method returns "light" search results, with only few metadata.

By adding the ``fullobjects: true`` parameter, it will retrieve the actual News Item objects,
including the image:

.. code-block:: ts

      this.services.resource.find(
        { portal_type: 'News Item' },
        '/',
        {
          sort_on: 'created',
          sort_order: 'reverse',
          size: 3,
          fullobjects: true,
        },
      )


.. code-block:: html+ng2

   <ul>
     <li *ngFor="let item of news">
       <a [traverseTo]="item['@id']">{{ item.title }}</a>
       <img [src]="item.image.download" />
     </li>
   </ul>

It does work, but what about turning it into a nice slideshow?

First let's implement the logic.
We need to manage the currently displayed news,
and we need the news to provide a ``state`` property set to ``'active'`` or ``'inactive'``.

.. code-block:: ts

   export class HomeComponent extends ViewView implements OnInit {

     news: any[] = [];
     current = -1;

     ngOnInit() {
       this.services.resource.find(
        { portal_type: 'News Item' },
        '/',
        {
          sort_on: 'created',
          sort_order: 'reverse',
          size: 3,
          fullobjects: true,
        },
      ).subscribe(res => {
        res.items.map(item => {
          item.state = 'inactive';
          this.news.push(item);
        })
        this.current = 0;
        this.news[this.current].state = 'active';
      });
    }

    goTo(index) {
      this.news[this.current].state = 'inactive';
      if (index < 0) {
        index = this.news.length - 1;
      }
      if (index == this.news.length) {
        index = 0;
      }
      this.current = index;
      this.news[this.current].state = 'active';
    }
  }

Now let's try it with our basic layout:

.. code-block:: html+ng2

   <div *ngIf="current > -1">
     <a [traverseTo]="news[current]['@id']">{{ news[current].title }}</a>
     <img [src]="news[current].image.download" />
   </div>
   <span (click)="goTo(current+1)">Next</span>

Good, now let's render it with animations.

We need to import the animation module in ``app.module.ts``:

.. code-block:: ts

   import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
   ...
     imports: [
       BrowserModule,
       BrowserAnimationsModule,
       ...

We need to declare the states and transition in the component decorator:

.. code-block:: ts

  import {
    trigger,
    state,
    style,
    animate,
    transition
  } from '@angular/animations';

  @Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
    animations: [
      trigger('flyInOut', [
        state('inactive', style({
          transform: 'translateX(-100%)'
        })),
        state('active', style({
          transform: 'translateX(0)'
        })),
        transition('inactive => active', [
          animate(200, style({ transform: 'translateX(0)' }))
        ]),
        transition('active => inactive', [
          animate(200, style({ transform: 'translateX(-100%)' }))
        ])
      ])
    ]
  })

And we need update the markup in ``home.component.html``:

.. code-block:: html+ng2

  <div class="col-md-12 slider">
    <div *ngFor="let item of news" class="slide"
      [@flyInOut]="item.state">
      <img [src]="item.image.download" />
      <div>
        <div class="title">
          <a [traverseTo]="item['@id']">{{ item.title }}</a>
        </div>
        <div class="description">
          <p>{{ item.description }}</p>
        </div>
      </div>
      <i class="next-news glyphicon glyphicon-chevron-right" (click)="goTo(current+1)"></i>
    </div>
  </div>

... and the style in :file:`home.component.scss`:

.. code-block:: scss

  @import "../../variables.scss";

  .slider {
    position: relative;
    padding: 0;
    height: 400px;
    overflow: hidden;
  }
  .slide {
    height: 300px;
    position: absolute;
    top: 0;
    width: 100%;
    img {
      width: 100%;
      height: auto
    }
    & > div {
      position: absolute;
      top: 60%;
      left: 66%;
    }
    .title, .description {
      text-transform: uppercase;
      text-decoration: none;
      color: white;
      background-color: $blue;
      padding: 1.5em;
    }
    a {
      color: white;
      font-weight: bold;
      font-size: 120%;
    }
    .next-news {
      color: white;
      position: absolute;
      font-weight: strong;
      right: 10px;
      top: 10px;
    }
  }

And we are done!


Login
=====

Let's add a login/logout link in the top-right corner.

In our ``AppComponent``, we add a boolean property to manage the login status,
and we use the ``authentication`` service to set its value:

.. code-block:: ts

  export class AppComponent {

    logged = false;

    constructor(
      ...
    ) {
      ...
      this.plone.authentication.isAuthenticated.subscribe(auth => {
        this.logged = auth.state;
      });
    }

Now, if we are not logged in yet, we display in ``app.component.html`` a link to traverse to the ``@@login`` view:

.. code-block:: html+ng2

  <div class="row">
    <div class="col-md-12">
      <a *ngIf="!logged" traverseTo="@@login" class="pull-right">Login</a>
    </div>
  </div>

Let's implement the logout link.

..  admonition:: Solution
    :class: toggle

    We add a second link with an output bound to the ``click`` event, which will call the ``logout()`` method of our component.

    .. code-block:: html+ng2

        <div class="row">
          <div class="col-md-12">
            <a *ngIf="!logged" traverseTo="@@login" class="pull-right">Login</a>
            <a *ngIf="logged" (click)="logout()" class="pull-right">Logout</a>
          </div>
        </div>


    So let's define the ``logout()`` method:

    .. code-block:: ts

        logout() {
          this.plone.authentication.logout();
        }

Now if we create private contents in Plone, they won't show unless we are logged in.

Adding Quick Links In the Footer
================================

We want to display useful links in the footer, and each link should have an icon.

We want those icons to be managed in Plone.

Customizing The Link Content Type
---------------------------------

We will use the Bootstrap font icon.

We need to customize the Link default content type so it can handle an icon identifier.

Go to the Plone site setup page / Dexterity  content types, and select Link.

Then in the Fields tab, we add a new textline field named 'icon'.

Now we can go back to the Plone site home, add a new folder named Quicklinks, and add few links.

For each of them, we will choose an icon name from https://getbootstrap.com/docs/3.3/components/#glyphicons-glyphs

And we will exclude the Quicklinks folder from navigation.

Displaying The Links
--------------------

Let's implement the Footer component able to display those links.

..  admonition:: Solution
    :class: toggle

    First we generate the component:

    ::

      $ ng generate component footer

    .. note:: We do not need to add it to ``entryComponents`` in the module as it is not a traversing component.

    We get the links using the ``resource`` service:

    ``src/app/footer/footer.component.ts``:

    .. code-block:: ts

      import { Component, OnInit } from '@angular/core';
      import { Services } from '@plone/restapi-angular';

      @Component({
        selector: 'app-footer',
        templateUrl: './footer.component.html',
        styleUrls: ['./footer.component.scss']
      })
      export class FooterComponent implements OnInit {

        links: any[] = [];

        constructor(public plone: Services) { }

        ngOnInit() {
          this.plone.resource.find(
            { portal_type: 'Link' },
            '/quicklinks',
            { fullobjects: true }
          ).subscribe(res => {
            this.links = res.items;
          })
        }
      }

    :file:`src/app/footer/footer.component.html`:

    .. code-block:: html+ng2

      <div class="col-md-12 footer-container">
        <ul>
          <li *ngFor="let link of links">
            <a [traverseTo]="link.remoteUrl">
              <i [class]="'glyphicon glyphicon-'+link.icon"></i>
              {{ link.title }}
            </a>
          </li>
        </ul>
      </div>

    :file:`src/app/footer/footer.component.scss`:

    .. code-block:: scss

      @import "../../variables.scss";

      .footer-container {
        background-color: darkgrey;
        color: white;
      }
      ul {
        display: flex;
      }
      li {
        flex-grow: 1;
        padding: 1em;
        list-style: none;
        text-align: center;
        i, a {
          display: block;
          color: white;
        }
        a:hover {
          text-decoration: none;
          color: white;
        }
        i {
          font-size: 130%;
        }
      }

    :file:`src/app/app.component.html`:

    .. code-block:: html+ng2

      <footer>
        <div class="container-fluid">
          <div class="row">
            <app-footer></app-footer>
          </div>
        </div>
      </footer>

Deployment
==========

The development bundle served by ``ng serve`` is not optimized for production.

To get a production-ready bundle, we use the following command:

.. code-block:: shell-session

  $ ng build --prod

The resulting bundle is generated in the ``./dist`` folder.

It is just a set of static files and can be served by any HTTP server.

Let's say we deploy it on http://example.com and we use Nginx to serve the files.

If we visit http://example.com, we will see our home page, and if we click on `News`,
we will obtain http://example.com/news thanks to angular-traversal.

But if decide to refresh the page at this point, we will get a 404, because our Nginx server will search for ``/news/index.html`` which does not exist.

So we need to fix our Nginx VHOST to preserve the client-side routing::

  location / {
    try_files   $uri $uri/ /index.html;
  }

This way, any existing file (like ``index.html``, ``vendor.xxx.bundle.js``, etc.) is served directly, but for anything else, we just return ``index.html`` so the client-side routing will take over.

Managing The Plone Configuration From The Angular Project
=========================================================

We have been customizing our Plone backend instance in order to comply with our project needs.

Everything has been done through the Plone web interface, which is handy but not safe
(what if our server crashes and we need to build a new one with the same configuration,
what if we want to setup a development instance, how to manage the changes, etc.).

It would be much better to manage the entire Plone configuration from our Angular project
just like the rest of our code.

Fortunately, two tools will help us to achieve that:

- `collective.themesitesetup <https://github.com/collective/collective.themesitesetup/>`_ allowing to manage a Plone configuration as part of a Plone theme,
- `plonetheme-upload <https://github.com/datakurre/plonetheme-upload>`_ allowing to push a Plone theme from a local NPM project to a remote Plone backend.

Creating A Theme To Handle The Configuration
--------------------------------------------

.. note::

   ``collective.themesitesetup`` is deployed by default on our Heroku instance.

   If you use your own backend, you will need to deploy it.

We need to go to our Plone backend, then in :menuselection:`Site Setup --> Theming` we create a new theme.
Let's name it ``plonecustom`` for instance.

As we do not really want to customize our backend theme, it will be very simple.
The only file we will need here for now is ``manifest.cfg``.
It will just be a copy of our default Barceloneta manifest:

.. code-block:: ini

   [theme]
   title = plonecustom
   description =
   rules = /++theme++barceloneta/rules.xml
   prefix = /++theme++barceloneta
   doctype = <!DOCTYPE html>
   enabled-bundles =
   disabled-bundles =

  # Resources must be registered either here in the Diazo bundle or in registry.xml
  development-css = /++theme++barceloneta/less/barceloneta.plone.less
  production-css = /++theme++barceloneta/less/barceloneta-compiled.css
  tinymce-content-css = /++theme++barceloneta/less/barceloneta-compiled.css
  development-js =
  production-js =

  [theme:genericsetup]

As you can see, we have added an extra section named ``[theme:genericsetup]``.
That's how collective.themesitesetup gets enabled.

Now we need to save our current Plone configuration into our theme.

We need to use the ``collective.themesitesetup`` export feature available here:
http://whatever.herokuapp.com/Plone/++theme++plonecustom/@@export-site-setup.

Obviously we do not need to export everything, in our current case we just want to get the comment feature related configuration and the content type configuration, so we just select ``typeinfo`` and ``plone.app.registry``.

After clicking on ``Export``, our theme will contain a new folder named ``install``.

Now we can download our theme from the Theming control panel and extract the resulting .zip file in our Angular project which now contains a folder named ``./plonecustom``.

Pushing The Plone Configuration From The Angular Project
--------------------------------------------------------

Let's add ``plonetheme-upload`` to our development dependencies:

.. code-block:: console

   npm install plonetheme-upload --dev

And let's add a new script in our :file:`package.json`:

.. code-block:: js

     "scripts": {
       ...
       "update-backend": "plonetheme-upload --enable plonecustom http://whatever.herokuapp.com/Plone"
     }

And now we can push our local ``./plonecustom`` to our Plone backend using the following command:

.. code-block:: console

   npm run update-backend

Advanced
========

.. todo:: To be completed

Moving Logic In A Service
-------------------------

Reactive Programming With RxJS
------------------------------

Enabling Offline & PWA
----------------------

.. note::

   HTTPS is mandatory.

SEO And Server-side Rendering
-----------------------------

robots.txt

Title and meta tags

Angular Universal
