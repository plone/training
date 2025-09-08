---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Override A default Plone Component Template

We need to change the template of the global navigation.

First we need to generate a new component

```console
ng generate component global-navigation
```

The CLI creates a new folder containing the component implementation, and it declares it in `src/app/app.module.ts`.

Our global navigation needs to inherit from Plone's own:

`src/app/global-navigation/global-navigation.component.ts`:

```ts
import { Component } from '@angular/core';
import { GlobalNavigation } from '@plone/restapi-angular';

@Component({
  selector: 'app-global-navigation',
  templateUrl: './global-navigation.component.html',
  styleUrls: ['./global-navigation.component.scss']
})
export class GlobalNavigationComponent extends GlobalNavigation {}
```

And now we can set the template we need:

`src/app/global-navigation/global-navigation.component.html`:

```html+ng2
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
```

Style it in {file}`src/app/global-navigation/global-navigation.component.scss`:

```scss
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
```

## Update The App Component Markup

Now we can fix the main component markup in `src/app/app.component.html`:

```html
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
```

Note we use our custom global navigation component (`app-global-navigation`)
but we keep the Plone default breadcrumbs component (`plone-breadcrumbs`) as its markup is fine.

We need to style it a little bit, let's add that in {file}`src/styles.scss`:

```scss
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
```
