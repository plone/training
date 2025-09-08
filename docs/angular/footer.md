---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Adding Quick Links In the Footer

We want to display useful links in the footer, and each link should have an icon.

We want those icons to be managed in Plone.

## Customizing The Link Content Type

We will use the Bootstrap font icon.

We need to customize the Link default content type so it can handle an icon identifier.

Go to the Plone site setup page / Dexterity  content types, and select Link.

Then in the Fields tab, we add a new textline field named 'icon'.

Now we can go back to the Plone site home, add a new folder named `Quicklinks`, and add few links.

For each of them, we will choose an icon name from <https://getbootstrap.com/docs/3.4/components/#glyphicons-glyphs>

And we will exclude the `Quicklinks` folder from navigation.

## Displaying The Links

Let's implement the Footer component able to display those links.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

First we generate the component:

```shell
ng generate component footer
```

```{note}
We do not need to add it to `entryComponents` in the module as it is not a traversing component.
```

We get the links using the `resource` service:

`src/app/footer/footer.component.ts`:

```ts
import { Component, OnInit } from '@angular/core';
import { Services } from '@plone/restapi-angular';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit {

  links: any[] = [];

  constructor(public services: Services) { }

  ngOnInit() {
    this.services.resource.find(
      { portal_type: 'Link' },
      '/quicklinks',
      { fullobjects: true }
    ).subscribe(res => {
      this.links = res.items;
    })
  }
}
```

{file}`src/app/footer/footer.component.html`:

```html+ng2
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
```

{file}`src/app/footer/footer.component.scss`:

```scss
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
```

{file}`src/app/app.component.html`:

```html+ng2
<footer>
  <div class="container-fluid">
    <div class="row">
      <app-footer></app-footer>
    </div>
  </div>
</footer>
```
````
