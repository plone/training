---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Creating A Custom View For The Talk Content Type

## Create The Talk Content Type In The Backend

We need to go to our Plone backend, then in {menuselection}`Site Setup --> Dexterity content types`,
we add a new content type named Talk.

We add a text field named `speaker`.

And we select the following behaviors:

- Lead image
- Rich text

Then we create a new folder named "Talks" where we add a few talks, and we publish them all (including the folder).

## Create A View Component For Talks

We could use the default view to display talks, but it would only display the title and the text,
and we would like to also display the image and the speaker.

Let's generate a new component with the CLI

```shell
ng generate component talk
```

To turn it into a valid view component, there are 3 steps:

- declare it in the module's `entryComponents`,
- inherit from a Plone view component,
- register the view for traversal.

In `app.module.ts`, we can see the CLI has already added `TalkComponent` in `declarations` which is mandatory
for any Angular component.

But as a view component is dynamically instantiated (depending on the traversed path), we also need to add it in `entryComponents`:

```ts
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
```

Now let's change `src/app/talk/talk.component.ts` to inherit from `ViewView`:

```ts
import { Component } from '@angular/core';
import { ViewView } from '@plone/restapi-angular';

@Component({
  selector: 'app-talk',
  templateUrl: './talk.component.html',
  styleUrls: ['./talk.component.scss']
})
export class TalkComponent extends ViewView {}
```

And lastly, let's associate this component to the `talk` content type as its default view in `src/app/app.component.ts`:

```ts
...
import { Services } from '@plone/restapi-angular';
import { TalkComponent } from './talk/talk.component';

@Component({
...
})
export class AppComponent {
  constructor(
    public views: PloneViews,
    public services: Services,
  ) {
    this.views.initialize();
    this.services.traverser.addView('view', 'talk', TalkComponent);
  }
}
```

The view is now properly set up, let's work on the template in `src/app/talk/talk.component.html`:

```html+ng2
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
```

## Enable Comments

We want to allow visitors to post comments about the talks.

In the Plone backend, in {menuselection}`Site Setup --> Discussion`, we activate comments globally and we allow anonymous comments.

In {menuselection}`Site Setup --> Content Settings`, we select the Talk type, and we allow comments.

Now in `src/app/talk/talk.component.html` we just append:

```html+ng2
<plone-comments></plone-comments>
```
