---
myst:
  html_meta:
    "description": "Advanced Components, Site Customization & Block Model v3"
    "property=og:description": "Advanced Components, Site Customization & Block Model v3"
    "property=og:title": "Advanced Components, Site Customization & Block Model v3"
    "keywords": "Plone, Volto, Training, Volto Light Theme, Integrate, block"
---

# Advanced Components, Site Customization & Block Model v3

## Understanding the Card Primitive

The Card primitive is VLT's reusable component for displaying content in card layouts. It has three configurable slots: image, summary, and actions.

### Card Structure

```jsx
<Card item={robot}>
  <Card.Image item={robot} />
  <Card.Summary>
    <h2>ARM-7 Bench Arm</h2>
    <p>Six-axis arm for precision bench work.</p>
  </Card.Summary>
  <Card.Actions>
    <Button>Book this unit</Button>
  </Card.Actions>
</Card>
```

### Making a Card Clickable

A card becomes a link when you give it either an `item` or an `href`. The two are mutually exclusive, and `item` is the one to reach for when you have a content object:

```jsx
<Card item={robot}>...</Card>            // preferred: a Plone content object
<Card href="/workshop/hours">...</Card>  // for arbitrary destinations
```

Passing `item` lets the underlying `UniversalLink` inspect the content type, so a File links to its download URL and an Image to its view, rather than to the object's default page.
Passing `href={item['@id']}` skips that, and those types end up linking to the wrong place.
Use `href` when you genuinely have only a URL.

Pass `null` to make the card non-interactive, which is what listing templates do in edit mode.

### Card Variations

- **Vertical layout** (default): Image on top
- **Horizontal layout**: Image on left or right
- **Contained**: With background color from theme
- **Listing**: Image displayed on left with specific size (controlled by `--card-listing-image-size`, default 220px)

### Card.Image Slot

Point the slot at a content object and it resolves the image from that item:

```tsx
<Card.Image item={robot} />
```

A `src` prop works too, for an image that is not a content object. To control how the image is rendered, pass your own component:

```tsx
<Card.Image
  item={robot}
  imageComponent={PreviewImageComponent}
/>
```

### Card.Summary Slot

Recommended structure using VLT's Summary component:

```tsx
import DefaultSummary from '@kitconcept/volto-light-theme/components/Summary/DefaultSummary';

const Summary = config.getComponent({
  name: 'Summary',
  dependencies: [item['@type']],
}).component || DefaultSummary;

<Card.Summary>
  <Summary item={item} HeadingTag="h2" />
</Card.Summary>
```

`Card` generates an id for the card's accessible name and builds a link component for the item, then passes both down to its slots as the `a11yLabelId` and `LinkToItem` props.
Slots forward them to their children, so a Summary rendered inside `Card.Summary` receives them without you wiring anything up.
Using them is what gives the card an accessible name and a real link—see the next section.

## Creating Custom Summary Components

The Summary component displays content metadata in listings, teasers, and cards. VLT includes built-in implementations:

- `DefaultSummary`: Kicker, title, and description
- `NewsItemSummary`: Publication date, kicker, title, description
- `EventSummary`: Start/end date, kicker, title, description
- `FileSummary`: File size and type
- `PersonSummary`: Contact details for the Person content type

### The Summary Contract

Every Summary receives the same props. Getting this shape right matters, because three of them are easy to miss:

```ts
type DefaultSummaryProps = {
  item: Partial<ObjectBrowserItem>;   // the content object
  LinkToItem?: React.ElementType;     // wraps the title in the card's link
  HeadingTag?: React.ElementType;     // the heading level to render
  a11yLabelId?: string;               // id that names the card
  hide_description?: boolean;
};
```

`item` is the content object. The other three are **siblings of `item`, not fields inside it**. A common mistake is to read them from `item`, where they will always be `undefined`.

`DefaultSummary` shows the pattern to follow:

```tsx
const DefaultSummary = (props) => {
  const {
    item,
    LinkToItem = React.Fragment,
    HeadingTag = 'div',
    a11yLabelId,
  } = props;

  return (
    <>
      {item?.head_title && <div className="headline">{item.head_title}</div>}
      <HeadingTag className="title" id={a11yLabelId}>
        <LinkToItem>{item.title ? item.title : item.id}</LinkToItem>
      </HeadingTag>
      {/* ... */}
    </>
  );
};
```

The `id={a11yLabelId}` and the `<LinkToItem>` wrapper are not decoration.
Together they give the card an accessible name and put a real link in the heading, which is how a keyboard or screen reader user reaches the item.
A Summary that omits them renders a card that looks right but cannot be navigated.

### Step 1: Create the Robot Content Type

The Robotarium lends robots, so it needs a content type for them. Create it through the Plone UI:

1. Go to http://localhost:3000/controlpanel/dexterity-types
2. Click "Add New Content Type"
3. Fill in:
   - **Type Name**: Robot
   - **Description**: A robot available for booking
4. Click "Add"
5. In the "Behaviors" tab, enable:
   - **Kicker field**, which adds `head_title`. We will use it to store the robot's charge level.
   - **Preview Image**, so robots can show a photo in listings.
   - Any other behaviors you want, such as Dublin Core metadata.
6. Click "Save"

```{note}
The form asks only for a name and a description. Plone derives the type's id from the name by normalizing it, so **Robot** becomes `robot`, and a name like **Charging Station** would become `charging_station`.

That id is what the REST API returns as the content's `@type`, and it is the value you register components against later in this chapter. It is worth confirming rather than assuming: open a robot you created and check the `@type` in `http://localhost:8080/Plone/<path>`, or look at the URL of the type you just added in the control panel.

Plone's built-in types predate this rule and keep their historical ids, which is why VLT registers its news summary against `News Item`, with a space and capitals, rather than `news_item`.
```

### Step 2: Create a Custom Summary Component

Create `src/components/Summary/RobotSummary.tsx`:

```tsx
import * as React from 'react';
import { FormattedNumber } from 'react-intl';
import type { DefaultSummaryProps } from '@kitconcept/volto-light-theme/components/Summary/DefaultSummary';

const RobotSummary = (props: DefaultSummaryProps) => {
  const {
    item,
    LinkToItem = React.Fragment,
    HeadingTag = 'div',
    a11yLabelId,
  } = props;
  const { title, description, head_title } = item;
  const charge = parseFloat(head_title);

  return (
    <>
      <HeadingTag className="title" id={a11yLabelId}>
        <LinkToItem>{title ? title : item.id}</LinkToItem>
      </HeadingTag>
      {description && <p className="description">{description}</p>}
      {head_title && !isNaN(charge) && (
        <div className="robot-charge">
          <div className="charge-label">
            <span>Charge</span>
            <span className="charge">
              <FormattedNumber value={charge / 100} style="percent" />
            </span>
          </div>
          {/* The bar repeats the value the label already states, so it is
              hidden from assistive technology rather than announced twice. */}
          <div className="charge-track" aria-hidden="true">
            <div
              className="charge-level"
              style={{ width: `${Math.min(Math.max(charge, 0), 100)}%` }}
            />
          </div>
        </div>
      )}
    </>
  );
};

RobotSummary.hideLink = false;
export default RobotSummary;
```

The `HeadingTag` default is `'div'` rather than a fixed heading level. The caller decides the level, because the right one depends on where the listing sits in the page's heading outline.

**Note**: We are reusing the kicker (`head_title`) to hold the charge level, so that the example needs no new field. A real Robotarium would add a proper numeric field to the Robot type instead, and reserve the kicker for what it is meant for: a line of text above the title.

### Step 3: Add Styles for the Robot Summary

The charge is the one thing VLT has no styling for, so it is the one thing this partial has to describe: a labelled row above a slim track whose fill is as wide as the charge.

Create `src/theme/_robotSummary.scss`:

```scss
.robot-charge {
  margin-top: $spacing-small;

  .charge-label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    @include headtitle2();
  }

  .charge-track {
    overflow: hidden;
    height: 5px;
    border-radius: 999px;
    background: color-mix(
      in oklab,
      var(--theme-foreground-color) 12%,
      transparent
    );
  }

  .charge-level {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(
      90deg,
      color-mix(in oklab, var(--accent-color) 60%, #fff),
      var(--accent-color)
    );
  }
}

// Cards that carry a charge read as instrument panels, so give them an edge.
.card:has(.robot-charge) {
  border: 1px solid oklch(1 0 0 / 0.28);
}
```

Three decisions here are worth carrying to your own work.

**Nothing is scoped to the listing.** A Summary is rendered in listings, in teasers, and in bare cards, and the same component should look the same in all of them. Scoping these rules to the fleet listing—`.robots .card .card-summary .robot-charge`—would style the listing and leave the same robot in a teaser looking like a different component. Selecting on what the Summary itself renders keeps the contexts in step.

Import in `src/theme/_main.scss`:

```scss
@import './blocks/button';
@import './blocks/cover';
@import './blocks/grid';
@import './blocks/slider';
@import './blocks/teaser';
@import './robotSummary';
```

### Step 4: Register the Summary Component

In `src/config/settings.ts`:

```typescript
import RobotSummary from '../components/Summary/RobotSummary';

export default function install(config: ConfigType) {
  // ... previous config ...

  config.registerComponent({
    name: 'Summary',
    component: RobotSummary,
    dependencies: ['robot'],
  });

  return config;
}
```

### Step 5: Test the Robot Summary

1. Add a Robot to your site, for example **ARM-7 Bench Arm**
2. Fill in the title, a short description, and the kicker with a plain number such as `87`
3. Add the robot to a Listing or Teaser block
4. `RobotSummary` renders the title, description, and a charge level of 87%

## Creating Custom Listing Variations with Card Actions

Listing variations customize content display in Listing blocks. Let's build a `RobotsTemplate` that presents the fleet and uses the Card.Actions slot for a booking button.

### Card.Actions Slot

```{important}
`Card.Actions` only renders what a template puts in it, and **none of VLT's built-in listing variations put anything there**. Registering an `Actions` component is not enough on its own: List, List with images, Grid, and the Teaser block all ignore the slot, so a card rendered by any of them shows no actions.

That is why the fleet listing below needs its own template. If you register an Actions component and see nothing, check which variation the listing is using before suspecting the registration.
```

The Card.Actions slot provides interactive elements beyond the main card link:
- "Book this unit" for a robot that is available
- "Download spec sheet" for its documentation
- "Reserve a slot" for a robot that is currently out

### Step 1: Create RobotActions Component

Create `src/components/Actions/RobotActions.tsx`:

```tsx
const RobotActions = ({ item }) => {
  return (
    <button type="button" className="book-unit-button button">
      Book {item.title}
    </button>
  );
};

export default RobotActions;
```

The button carries `type="button"` so it does not submit a surrounding form, and names the robot it belongs to. In a fleet listing, four buttons all reading "Book" are indistinguishable to someone moving through the page control by control; "Book ARM-7 Bench Arm" is not.

### Step 2: Register RobotActions

Update `src/config/settings.ts`:

```typescript
import RobotActions from '../components/Actions/RobotActions';

export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Register RobotActions component
  config.registerComponent({
    name: 'Actions',
    component: RobotActions,
    dependencies: ['robot'],
  });

  return config;
}
```

### Step 3: Create RobotsTemplate Listing Variation

Create `src/components/blocks/Listing/RobotsTemplate.tsx`:

```tsx
import React from 'react';
import PropTypes from 'prop-types';
import ConditionalLink from '@plone/volto/components/manage/ConditionalLink/ConditionalLink';
import Card from '@kitconcept/volto-light-theme/primitives/Card/Card';
import { flattenToAppURL, isInternalURL } from '@plone/volto/helpers/Url/Url';
import config from '@plone/volto/registry';
import DefaultSummary from '@kitconcept/volto-light-theme/components/Summary/DefaultSummary';
import cx from 'classnames';

const RobotsTemplate = ({ items, linkTitle, linkHref, isEditMode }) => {
  let link = null;
  let href = linkHref?.[0]?.['@id'] || '';
  const PreviewImageComponent = config.getComponent('PreviewImage').component;

  if (isInternalURL(href)) {
    link = (
      <ConditionalLink to={flattenToAppURL(href)} condition={!isEditMode}>
        {linkTitle || href}
      </ConditionalLink>
    );
  } else if (href) {
    link = <a href={href}>{linkTitle || href}</a>;
  }

  return (
    <>
      <ul className="items">
        {items.map((item) => {
          const Summary =
            config.getComponent({
              name: 'Summary',
              dependencies: [item['@type']],
            }).component || DefaultSummary;

          const Actions = config.getComponent({
            name: 'Actions',
            dependencies: [item['@type']],
          }).component;

          const showLink = !Summary.hideLink && !isEditMode;
          const placeholderSrc =
            config.settings.placeholderImages?.[item['@type']];

          return (
            <li
              className={cx('listing-item', {
                [`${item['@type']?.toLowerCase()}-listing`]: item['@type'],
              })}
              key={item['@id']}
            >
              <Card item={showLink ? item : null}>
                {(item.image_field !== '' || placeholderSrc) && (
                  <Card.Image
                    className="item-image"
                    item={item}
                    showPlaceholderImage={true}
                    placeholderSrc={placeholderSrc}
                    imageComponent={PreviewImageComponent}
                    sizes={`(max-width: ${config.settings.layout.tabletBreakpoint}px) 100vw, ${Math.trunc(config.settings.layout.defaultContainerWidth / 2)}px`}
                  />
                )}
                <Card.Summary>
                  <Summary item={item} />
                </Card.Summary>
                <Card.Actions>
                  {Actions && <Actions item={item} />}
                </Card.Actions>
              </Card>
            </li>
          );
        })}
      </ul>

      {link && <div className="footer">{link}</div>}
    </>
  );
};

RobotsTemplate.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkTitle: PropTypes.string,
  linkHref: PropTypes.any,
  isEditMode: PropTypes.bool,
};

export default RobotsTemplate;
```

**Key Features:**
- Uses `config.getComponent()` to fetch registered Summary/Actions components by content type
- `showLink` ensures cards are only clickable when appropriate
- `isEditMode` disables navigation during editing
- Dynamically renders Actions only for content types that have them registered
- Renders a `<ul>` of `<li>` elements, matching VLT's own listing templates, so assistive technology announces the item count
- Passes `item` to `Card` rather than a bare URL, so content types with their own link behavior, such as File, resolve correctly
- Passes `sizes` and the placeholder props to `Card.Image`, exactly as VLT's own variations do

```{important}
Write a variation by starting from the VLT variation closest to what you want—here that is `GridTemplate`, since the fleet is a two-column card grid—and change only what has to change.

The two additions above are a good illustration of why. `sizes` tells the browser how wide the image will actually render, so that it downloads the right scale; omit it and the cards look soft for no visible reason. `showPlaceholderImage` and `placeholderSrc` keep the grid from collapsing on an item that has no image. Neither is obvious from the outside, and both come for free by following the shape of the template you are adapting.

The same applies to the stylesheet in the next step.
```

### Step 4: Register RobotsTemplate

Update `src/config/blocks.ts`:

```typescript
import RobotsTemplate from '../components/blocks/Listing/RobotsTemplate';

export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Register RobotsTemplate listing variation
  config.blocks.blocksConfig.listing.variations = [
    ...(config.blocks.blocksConfig.listing.variations || []),
    {
      id: 'robots',
      title: 'Robot Fleet',
      template: RobotsTemplate,
    },
  ];

  return config;
}
```

### Step 5: Add Styles

The fleet is a two-column card grid, which is what VLT's own `grid` variation already is—so the stylesheet is that variation's rules, repeated for `robots`, plus the two things the grid variation has no equivalent for: the card surface, and the actions row.

Create `src/theme/blocks/_listing.scss`:

```scss
// The Robot Fleet variation is a two-column card grid, which is exactly what
// VLT's own `grid` variation already is. These rules mirror `.block.listing.grid`
// in VLT's `theme/blocks/_listing.scss` and `theme/_layout.scss`; the only
// additions are the card surface and the actions row, which the grid variation
// has no equivalent for.

// VLT constrains most listing variations per item, and the grid variation as a
// whole. A card grid needs the second treatment, so repeat for `robots` what
// VLT does for `& > .block.listing.grid`. View mode only — in edit mode
// `.block-editor-listing .items` is already the constrained element, and adding
// a second cap on the block is what makes the fleet listing sit off-center there.
#page-document .blocks-group-wrapper > .block.listing.robots {
  @include default-container-width();
  @include adjustMarginsToContainer($default-container-width);
}

.block.listing.robots {
  &.next--has--same--backgroundColor.next--is--same--block-type,
  &.next--is--__button {
    .listing-item:last-child {
      padding-bottom: 0 !important;
      border-bottom: none !important;
    }
  }

  .items {
    display: flex;
    flex-wrap: wrap;

    @media only screen and (max-width: $largest-mobile-screen) {
      flex-direction: column;

      .listing-item {
        padding-bottom: $spacing-small !important;
      }
    }
  }

  .listing-item {
    // Cards in a row are as tall as the tallest of them, and the actions have
    // to sit on the bottom edge of each. That needs an unbroken chain of
    // stretching boxes from the row down to `.card-inner` — an `align-self` on
    // the actions alone does nothing while these are all still block boxes.
    display: flex;
    align-items: normal;
    border-bottom: none;
    margin: 0 !important;

    @media only screen and (min-width: $tablet-breakpoint) {
      width: 50%;
      padding-top: 10px;
      padding-bottom: 10px !important;

      &:nth-child(2n) {
        padding-left: 10px !important;
      }

      &:nth-child(2n + 1) {
        padding-right: 10px !important;
      }

      &:last-child,
      &:nth-last-child(2):not(:nth-child(2n)) {
        padding-bottom: 0 !important;
      }

      &:first-child,
      &:nth-child(2) {
        padding-top: 0 !important;
      }
    }

    &:last-child:nth-child(2n + 1) {
      @media only screen and (min-width: $largest-mobile-screen) {
        margin-left: 0 !important;
      }
    }

    .card {
      display: flex;
      flex-direction: column;
      flex-grow: 1;

      // VLT gives the grid variation's cards the theme's secondary surface from
      // `use-theme-colors()`; `.robots` is not `.grid`, so say it here.
      background-color: var(--theme-high-contrast-color);

      .card-inner {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        padding-bottom: $spacing-medium !important;

        .image-wrapper img {
          margin: 0;
        }

        .card-summary {
          display: flex;
          flex-direction: column;
          flex-grow: 1;
          padding: $spacing-medium $spacing-small 0 $spacing-small;

          .title {
            margin: 0 0 $spacing-small 0 !important;
            @include text-heading-h3();
          }

          // As in the reference design: the charge bar sits on the bottom edge
          // of the summary, so the bars line up across a row however long the
          // descriptions are.
          .robot-charge {
            padding-top: $spacing-small;
            margin-top: auto;
          }
        }
      }

      // The fleet's own addition: the Card.Actions slot, which none of VLT's
      // variations fill.
      .actions-wrapper {
        // The last of the stretching boxes: `auto` here is what pins the
        // actions to the bottom of a card that is taller than its content.
        margin-top: auto;
        padding: $spacing-small $spacing-small 0 $spacing-small;
        text-align: right;

        .book-unit-button {
          padding: 8px 20px;
          border: 1px solid var(--accent-color);
          background: var(--accent-color);
          color: var(--accent-foreground-color);
          cursor: pointer;
          transition:
            background 0.2s ease,
            color 0.2s ease,
            border-color 0.2s ease;
          @include body-text-bold();

          // The inverse of the filled state, matching how the Button block
          // inverts on hover. Both values are read from the theme's foreground,
          // which is always a color — `--theme-color` may be a gradient.
          &:hover,
          &:focus {
            border-color: var(--theme-foreground-color);
            background: none;
            color: var(--theme-foreground-color);
          }
        }
      }
    }
  }
}
```

Import in `src/theme/_main.scss`:

```scss
@import './blocks/button';
@import './blocks/cover';
@import './blocks/grid';
@import './blocks/listing';
@import './blocks/slider';
@import './blocks/teaser';
@import './robotSummary';
```

### Step 6: Test the Fleet Listing

1. Add a few robots, such as **ARM-7 Bench Arm**, **ROVER-2 Terrain Scout**, **QUAD-4 Walker**, and **DRONE-1 Surveyor**, each with a description, a charge level in the kicker, and an image
2. Add a Listing block to a page
3. Select the **Robot Fleet** variation in the block settings
4. Configure the block to list the Robot content type
5. Each robot appears with its image, summary, charge level, and a Book button

## Working with Slots

VLT provides slots for extending the layout without component shadowing. Let's create a practical example: a sign-up form for **Signal**, the Robotarium's workshop bulletin, in the preFooter slot.

### Available Slots

Volto core renders three slots, and VLT's header, footer, and listing add the rest:

| Slot | Where | Arrives with |
| --- | --- | --- |
| `aboveApp` | Outermost, around the whole app | `plone-components-css` |
| `aboveContent` | Above the content view | — |
| `belowContent` | Below the content view | **`tags` and `relatedItems`** |
| `aboveHeader` | Above the header | — |
| `belowHeader` | Below the header | — |
| `headerTools` | Header, top right | Anontools |
| `preFooter` | Before the footer | — |
| `footer` | Main footer area | VLT's footer |
| `postFooter` | After the footer | — |
| `footerLinks` | Footer links section | VLT's footer links |
| `followUs` | Social media section | — |
| `aboveListingItems` | Inside a Listing block, above the items | — |

```{important}
Most slots start empty, but `belowContent` does not.
Volto registers `tags` and `relatedItems` into it by default, so every content view already renders a tag list and a related-items list before you add anything.

Because the last registration wins, and add-on configuration runs after core's, you displace a built-in by re-registering its name with a component that renders nothing:

    config.registerSlotComponent({
      slot: 'belowContent',
      name: 'relatedItems',
      component: () => null,
    });

Check what a slot already contains before you register into it.
```

### Step 1: Create the Signal Sign-up Component

Create `src/components/SignalSignup/SignalSignup.tsx`:

```tsx
import React, { useState } from 'react';

const SignalSignup = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real implementation, this would submit to a mailing service
    console.log('Signal sign-up:', email);
    alert(`Thanks, ${email}. You are on the Signal list.`);
    setEmail('');
  };

  return (
    <div className="signal-signup">
      <div className="signal-container">
        <h2 className="signal-title">Signal</h2>
        <p className="signal-description">
          Workshop notes, new arrivals, and downtime warnings. One message a month.
        </p>
        <form onSubmit={handleSubmit} className="signal-form">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            aria-label="Email address"
            placeholder="you@example.com"
            required
            className="signal-input"
          />
          <button type="submit" className="signal-button">
            Sign up
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignalSignup;
```

### Step 2: Add Styles

Create `src/theme/_signalSignup.scss`:

```scss
// VLT pads the footer's first child with `#footer > :first-child:not(:empty)`
// (1,1,0). The sign-up band brings its own padding and its own background, so
// that padding shows up as a gap in the footer's gradient above it.
#footer > .pre-footer:has(.signal-signup) {
  padding: 0;
}

.signal-signup {
  background-color: var(--secondary-color);
  color: var(--secondary-foreground-color);
  padding: 4rem 2rem;

  .signal-container {
    max-width: var(--default-container-width);
    margin: 0 auto;
    text-align: center;
  }

  .signal-title {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .signal-description {
    font-size: 1.125rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .signal-form {
    display: flex;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
    flex-wrap: wrap;
    justify-content: center;

    .signal-input {
      flex: 1;
      min-width: 250px;
      padding: 0.75rem 1rem;
      border: 1px solid var(--secondary-foreground-color);
      font-size: 1rem;
      background-color: var(--primary-color);
      color: var(--primary-foreground-color);

      &:focus {
        outline: 2px solid var(--accent-color);
        outline-offset: 2px;
      }
    }

    .signal-button {
      padding: 0.75rem 2rem;
      background-color: var(--accent-color);
      color: var(--accent-foreground-color);
      border: none;
      font-size: 1rem;
      cursor: pointer;
      transition: opacity 0.2s;

      &:hover {
        opacity: 0.9;
      }

      &:focus {
        outline: 2px solid var(--accent-foreground-color);
        outline-offset: 2px;
      }
    }
  }
}
```

Import in `src/theme/_main.scss`:

```scss
@import './blocks/button';
@import './blocks/cover';
@import './blocks/grid';
@import './blocks/listing';
@import './blocks/slider';
@import './blocks/teaser';
@import './robotSummary';
@import './signalSignup';
```

### Step 3: Register the Component to the Slot

In `src/config/settings.ts`:

```typescript
import SignalSignup from '../components/SignalSignup/SignalSignup';

export default function install(config: ConfigType) {
  // ... previous config ...

  config.registerSlotComponent({
    name: 'SignalSignup',
    slot: 'preFooter',
    component: SignalSignup,
  });

  return config;
}
```

The Signal sign-up now appears before the footer on every page, demonstrating how slots let you extend the layout without shadowing core components.

## Swapping Structural Components

Slots let you *add* to the layout. Sooner or later you will want to *replace* part of it—a navigation that your design calls for, a footer that VLT's does not cover.

The old answer was to shadow the component by dropping a file into {file}`customizations`. VLT 8 offers a better one: its structural components are resolved through the registry at render time, so a project can substitute its own by registering it and naming it in configuration.

### How It Works

VLT registers each of its structural components as a utility under the name `vlt`, with a `type` naming the role:

```typescript
config.registerUtility({ name: 'vlt', type: 'navigation', method: Navigation });
```

A setting then decides which registered name renders for each role:

```typescript
config.settings.vlt = {
  components: {
    breadcrumbs: 'vlt',
    footer: 'vlt',
    header: 'vlt',
    languageSelector: 'vlt',
    logo: 'vlt',
    mobileNavigation: 'vlt',
    navigation: 'vlt',
    searchWidget: 'vlt',
    tags: 'vlt',
  },
};
```

These are the defaults, so out of the box nothing changes. The nine roles above are the ones you can swap.

### Making the Swap

Swapping a role takes two steps, and the Robotarium does not need either of them yet—the mechanism is worth knowing before you reach for it.

First, register your implementation under a name of your own, against the role's `type`, in {file}`src/config/settings.ts`:

```typescript
config.registerUtility({
  name: 'robotarium',
  type: 'navigation',
  method: MyNavigation,
});
```

Both implementations now sit in the registry, and nothing renders differently yet. The second step selects yours:

```typescript
config.settings.vlt.components.navigation = 'robotarium';
```

That is the whole change. VLT's header resolves the navigation through the registry when it renders, so it picks up your component. Every other role keeps its `vlt` default, and VLT's own navigation stays registered under `vlt`—so reverting is a one-line edit, not a file deletion.

The same two steps swap any of the nine roles.

### Why Prefer This Over Shadowing

- **Explicit.** The active component is named in configuration, not implied by a file's path.
- **Composable.** Several implementations can coexist under different names, and you choose which one renders.
- **Decoupled.** You bind to a role name, not to an internal module path that can move between VLT releases.
- **Safe.** If a setting names a component that was never registered, VLT falls back to its own implementation rather than rendering nothing.
- **Typed.** The keys of `config.settings.vlt.components` are a fixed set, so a misspelled role is a compile error rather than a silent no-op.

```{note}
Your add-on must be applied after `@kitconcept/volto-light-theme` so that `config.settings.vlt` exists when you assign to it.
Keeping VLT last in your project add-on's `addons` list, as set up in the first chapter, is enough.
```

## Site Customization Behaviors

VLT provides backend behaviors for site customization that you activated earlier. These behaviors enable fields for customizing the site without code changes.

### Header Customization Options

Through the Plone UI, you can customize:
- **Site logo**: Main logo in the top left
- **Complementary logo**: Second logo on the right side
- **Fat menu**: Enabled by default, can be disabled
- **Intranet header**: Alternative header for intranet sites
- **Site flag**: The colored pill at the top left of the header
- **Actions**: Links at the top right

### Theme Customization Options

- Navigation text color
- Fat menu and breadcrumbs text color
- Fat menu background color
- Footer font color
- Footer background color

### Footer Customization Options

- **Footer links**: Additional links with title, URL, and new tab option
- **Footer logos**: List of logos with links and customizable size (small/large) and container width (default/layout)
- **Footer colophon text**: Customizable last line of footer

## Block Model v3 (opt-in)

```{note}
Block Model v3 is a beta feature. It's recommended to only use it when all blocks in your registry are v3-compatible (indicated by banner in block's GitHub repository).
```

Block Model v3 introduces a unified container architecture that ensures consistent styling and spacing between View and Edit modes. This eliminates the previous issues where Edit mode appeared different from View mode.

### Key Benefits

- Consistent rendering across View and Edit modes
- Simplified CSS with standardized container structure
- Improved spacing control through block categories
- Reduced maintenance overhead

(bm3-two-container-label)=

### The Two-Container System

Every block in Block Model v3 follows this structure:

```
┌────────────────────────────────────────────────────────────┐
│ Main/Outer Container (.block.${type}.category-${category}) │
│ • Full width (edge to edge)                                │
│ • Background color & theme variables                       │
│ • Vertical spacing via padding on BG color changes         │
│                                                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Secondary/Inner Container (.block-inner-container)    │ │
│  │ • Content width & horizontal centering                │ │
│  │ • Default vertical spacing between blocks             │ │
│  │ • Content alignment via CSS Grid                      │ │
│  │                                                       │ │
│  │    [Block Content Here]                               │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

**Main/Outer Container:**
- Spans the full layout width
- Handles background colors and theme variables
- Uses padding (not margin) for vertical spacing
- CSS Classes: `.block.${type}.category-${category}`

**Secondary/Inner Container:**
- Controls content width constraints
- Provides consistent inter-block spacing
- Supports content alignment through CSS Grid
- CSS Class: `.block-inner-container`

### Enable Block Model v3

VLT ships with `config.settings.blockModel = 2` and copies that value onto each block it has migrated. Opting in means setting the flag and re-applying it to those blocks, because they read the value at the time VLT was configured—which is before your add-on runs.

In your project's `src/config/settings.ts`:

```typescript
export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Enable Block Model v3 globally
  config.settings.blockModel = 3;

  // Re-apply it to the blocks VLT has migrated
  for (const type of ['slate', 'title', '__button']) {
    config.blocks.blocksConfig[type].blockModel = config.settings.blockModel;
  }

  return config;
}
```

```{important}
Check each block's repository for the "BMv3 ready" banner before you flip it.
```

### Block Categories

Block categories determine spacing relationships between adjacent blocks, through the `category-${category}` class on the outer container. They are set at `config.blocks.blocksConfig.[$type].category`.

VLT already assigns categories to the blocks it has migrated, so you do not need to repeat them:

| Category | Blocks | Spacing behavior |
| --- | --- | --- |
| `inline` | `slate` | Flows as body text |
| `title` | `title` | Opens a section |
| `action` | `__button` | A call to action |
| `cards` | `gridBlock` | Self-contained visual units |

Your own blocks need a category too, and the useful instinct is to reach for one of these four before inventing a fifth. The Cover block renders a self-contained visual unit with its own background, which is what `cards` already describes, so it can reuse it.

These two lines go in {file}`src/config/blocks.ts`, **after** the Cover registration from the previous chapter. They are worth adding even with the flag left at `2`—`blockModel` simply picks up whatever `config.settings.blockModel` currently holds:

```typescript
config.blocks.blocksConfig.cover.category = 'cards';
config.blocks.blocksConfig.cover.blockModel = config.settings.blockModel;
```

```{warning}
The file matters here, and so does the position within it.

{file}`src/index.ts` calls `installSettings` before `installBlocks`, so at the time {file}`config/settings.ts` runs, `config.blocks.blocksConfig.cover` does not exist yet—putting these lines there alongside `config.settings.blockModel = 3` throws. They have to run after the block is registered, and after the flag is set, which {file}`config/blocks.ts` satisfies on both counts.
```

Add a category of your own only when a block genuinely spaces differently from all four. When you do, name it for the family it opens rather than for the block that prompted it, and remember that a category only means something if your stylesheets act on the `category-*` class it produces.

Vertical spacing between blocks is provided by the **upper block**:
- Block content should be flush with top of container
- Bottom padding creates space for following block
- Different category combinations may have specific spacing adjustments

### View Mode Structure

```tsx
<div
  style="$StyleWrapperStyles"
  className="block $type category-$category $StyleWrapperClassNames"
>
  <div className="block-inner-container">
    {View component}
  </div>
</div>
```

### Edit Mode Structure

```tsx
<div
  style="$StyleWrapperStyles"
  className="block $type category-$category $StyleWrapperClassNames"
>
  <div className="block-inner-container">
    {Edit component}
  </div>
  <div className="block-edit-helpers">
    {/* Delete block button, move block buttons, etc. */}
  </div>
</div>
```

Notice how the actual block content remains identical in both modes, while the framework containers handle all the differences in layout and editing functionality.
### The `volto-bm3-compat` add-on

Block Model v3 changes the markup a block renders into, so blocks written against the older model need their styles adapting. `@kitconcept/volto-bm3-compat` bridges that gap, and VLT declares it as an add-on of its own, so it is already in your dependency tree if you followed the install chapter.

Check the block's repository for the "BMv3 ready" banner before enabling the new model on a block you did not write.

## Checkpoint

- `config.settings.vlt.components` lists the nine swappable roles, each still set to `vlt`. Naming a component that was never registered under one of them falls back to VLT's own rather than rendering nothing.
- The Signal sign-up form appears above the footer on every page.
- A Listing block set to the **Robot Fleet** variation shows each charge level as a labelled bar, the Book buttons line up along the bottom of the cards whatever the description lengths, and tabbing through the page reaches every robot title as a link.
- The same robot in a Teaser block renders the same title, description, and charge bar as it does in the fleet listing.
- If—and only if—you enabled Block Model v3, a Slate block renders inside a `.block-inner-container` and looks the same in edit mode as in view mode. With the flag left at `2`, as the Robotarium leaves it, every block still renders through the v2 path.

## Further Reading

- [Swap structural components](https://volto-light-theme.readthedocs.io/how-to-guides/swap-structural-components.html)
- [Slots reference](https://volto-light-theme.readthedocs.io/reference/slots.html)
- [Card primitive reference](https://volto-light-theme.readthedocs.io/reference/card.html)
- [Summary components](https://volto-light-theme.readthedocs.io/how-to-guides/summary.html)
- [Site customization](https://volto-light-theme.readthedocs.io/conceptual-guides/site-customization.html)
- [Block Model v3](https://volto-light-theme.readthedocs.io/conceptual-guides/block-model-v3.html)
