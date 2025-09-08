---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Displaying News On The Home Page

We want to display the 3 most recent news on the home page.

First we need a Home component. Let's initialize it properly.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

> We use the CLI:
>
> ```shell
> ng generate component home
> ```
>
> Then we add  `HomeComponent` in  `entryComponents` in the module.
>
> We declare it as a view for the `Plone Site` type in `AppComponent`:
>
> ```ts
> import { HomeComponent } from './home/home.component';
>
> ...
>
> this.services.traverser.addView('view', 'Plone Site', HomeComponent);
> ```
````

We want this component to display the 3 most recent news.
The `resource` service from `@plone/restapi-angular` provides a `find` method to do that.

Here is the `HomeComponent` implementation:

```ts
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
```

We could display those news with a basic layout like this:

```html+ng2
<ul>
  <li *ngFor="let item of news">
    <a [traverseTo]="item['@id']">{{ item.title }}</a>
  </li>
</ul>
```

Titles are not enough, it would be better to display images.

The `find` method returns "light" search results, with only few metadata.

By adding the `fullobjects: true` parameter, it will retrieve the actual News Item objects,
including the image:

```ts
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
```

```html+ng2
<ul>
  <li *ngFor="let item of news">
    <a [traverseTo]="item['@id']">{{ item.title }}</a>
    <img [src]="item.image.download" />
  </li>
</ul>
```

It does work, but what about turning it into a nice slideshow?

First let's implement the logic.
We need to manage the currently displayed news,
and we need the news to provide a `state` property set to `'active'` or `'inactive'`.

```ts
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
```

Now let's try it with our basic layout:

```html+ng2
<div *ngIf="current > -1">
  <a [traverseTo]="news[current]['@id']">{{ news[current].title }}</a>
  <img [src]="news[current].image.download" />
</div>
<span (click)="goTo(current+1)">Next</span>
```

Good, now let's render it with animations.

We need to import the animation module in `app.module.ts`:

```ts
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
...
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ...
```

We need to declare the states and transition in the component decorator:

```ts
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
```

And we need update the markup in `home.component.html`:

```html+ng2
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
```

... and the style in {file}`home.component.scss`:

```scss
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
```

And we are done!
