---
myst:
  html_meta:
    "description": "Advanced Components, Slots & Block Model v3"
    "property=og:description": "Advanced Components, Slots & Block Model v3"
    "property=og:title": "Advanced Components, Slots & Block Model v3"
    "keywords": "Plone, Volto, Training, Volto Light Theme, Integrate, block"
---

# Advanced Components, Slots & Block Model v3

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

The link wraps the title inside the summary, and a CSS overlay stretches its clickable area across the whole card.

Passing `item` lets the underlying link inspect the content type.
For visitors who are not logged in, a File links to its download URL, and a Link item links to its target URL.
Passing `href={item['@id']}` skips that, and those items link to their own page instead.
Use `href` when you genuinely have only a URL.

Pass `null` to make the card non-interactive, which is what listing templates do in edit mode.

### Card Variations

The layout of a card depends on where it is rendered:

- **Vertical** (default): the image is on top.
- **Horizontal**: the image is on the left or on the right, when the surrounding block is aligned left or right, as a Teaser block can be.
- **Contained**: inside a container block, such as a Grid, the summary gets side padding, and the card takes its background color from the current theme.
- **Listing**: inside a `.card-listing` wrapper, the image is on the left, with a fixed width set by `--card-listing-image-size`, 220px by default.

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
import config from '@plone/volto/registry';
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
`Card.Summary` forwards them to its children, so a Summary rendered inside it receives them without you wiring anything up.
Using them is what gives the card an accessible name and a real link—see the next section.

## Creating Custom Summary Components

The Summary component displays content metadata in listings, teasers, and cards.
VLT includes these implementations, and registers all but the first for their content types:

- `DefaultSummary`: the kicker, title, and description. It is the fallback for all other types.
- `NewsItemSummary`, for News Items: the publication date and the kicker, then the title and description.
- `EventSummary`, for Events: the start and end dates and the kicker, then the title and description.
- `FileSummary`, for Files: the file size, file type, and kicker, then the title and description.
- `PersonSummary`, for the Person type: the kicker, title, and description, plus the email address, phone number, and room.

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

1. Go to http://localhost:3000/controlpanel/dexterity-types.
2. Select the **Add** button in the toolbar.
3. In the **Add new content type** form, fill in:
   - **Title**: Robot
   - **Description**: A robot available for booking
4. Select **Save**.
5. Select **Robot** in the list of content types.
6. In the **Behaviors** tab, enable:
   - **Kicker field**, which adds a field named `head_title`. The Robotarium uses it to store the robot's charge level.
   - **Preview Image**, so that robots can show a photo in listings.
   - Any other behaviors you want.
7. Select **Save**.

```{note}
The form asks only for a title and a description. Plone derives the type's id from the title by normalizing it, so **Robot** becomes `robot`, and a title like **Charging Station** would become `charging_station`.

That id is what the REST API returns as the content's `@type`, and it is the value you register components against later in this chapter.
It is worth confirming rather than assuming: open http://localhost:3000/++api++/ followed by the path of a robot you created, and check its `@type`.

Plone's built-in types predate this rule and keep their historical ids, which is why VLT registers its news summary against `News Item`, with a space and capitals, rather than `news_item`.
```

### Step 2: Create a Custom Summary Component

Create {file}`src/components/Summary/RobotSummary.tsx`:

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

```{note}
The example reuses the kicker (`head_title`) to hold the charge level, so that it needs no new field.
A real Robotarium would add a proper numeric field to the Robot type instead, and reserve the kicker for what it is meant for: a line of text above the title.
```

### Step 3: Add Styles for the Robot Summary

The charge is the one thing VLT has no styling for, so it is the one thing this partial has to describe: a labelled row above a slim track whose fill is as wide as the charge.

Create {file}`src/theme/_robotSummary.scss`:

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

**Nothing is scoped to the listing.** A Summary is rendered in listings, in teasers, and in bare cards, and the same component should look the same in all of them. Scoping these rules to the fleet listing, with a selector such as `.robots .card .card-summary .robot-charge`, would style the listing and leave the same robot in a teaser looking like a different component. Selecting on what the Summary itself renders keeps the contexts in step.

**The colors come from tokens.** The track mixes the theme's foreground color with transparency, so it stays visible on any block theme, and the fill follows `--accent-color`, so it changes with the design.

**The typography comes from VLT.** The label uses VLT's `headtitle2()` mixin, one of the theme's text styles for small labels, instead of a font size of its own.

Import the partial at the end of {file}`src/theme/_main.scss`:

```scss
@import './robotSummary';
```

### Step 4: Register the Summary Component

In {file}`src/config/settings.ts`:

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

1. Add a Robot to your site, for example **ARM-7 Bench Arm**.
2. Fill in the title, a short description, and the kicker with a plain number such as `87`.
3. Add the robot to a Listing or Teaser block.
4. `RobotSummary` renders the title, the description, and a charge level of 87%.

## Creating Custom Listing Variations with Card Actions

Listing variations customize how a Listing block displays its content. This section builds a `RobotsTemplate` that presents the fleet and uses the Card.Actions slot for a booking button.

### Card.Actions Slot

```{important}
`Card.Actions` only renders what a template puts in it, and **none of VLT's built-in listing variations put anything there**.
Registering an `Actions` component is not enough on its own: the List, List with images, and Grid variations, and the Teaser block, all ignore the slot, so a card rendered by any of them shows no actions.

That is why the fleet listing below needs its own template. If you register an Actions component and see nothing, check which variation the listing is using before suspecting the registration.
```

The Card.Actions slot provides interactive elements beyond the main card link:

- "Book this unit" for a robot that is available
- "Download specifications" for its documentation
- "Reserve a slot" for a robot that is currently out

The card's link overlay covers the whole card, so the actions have to sit above it. Otherwise, selecting an action would open the card's link instead.
The stylesheet in Step 5 takes care of that.

### Step 1: Create RobotActions Component

Create {file}`src/components/Actions/RobotActions.tsx`:

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

Update {file}`src/config/settings.ts`:

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

Create {file}`src/components/blocks/Listing/RobotsTemplate.tsx`:

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
                <Card.Image
                  className="item-image"
                  item={item}
                  showPlaceholderImage={true}
                  placeholderSrc={placeholderSrc}
                  imageComponent={PreviewImageComponent}
                  sizes={`(max-width: ${config.settings.layout.tabletBreakpoint}px) 100vw, ${Math.trunc(config.settings.layout.defaultContainerWidth / 2)}px`}
                />
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

- Uses `config.getComponent()` to fetch the Summary and Actions components registered for each content type
- Renders actions only for content types that have an Actions component registered
- Always renders the image slot, so a robot without a photo shows a placeholder, and every card in a row has the same shape
- Passes `null` to `Card` in edit mode, or when the Summary sets `hideLink`, so that the card is not a link there
- Passes `item` to `Card` rather than a bare URL, so that content types with their own link behavior, such as File, resolve correctly
- Renders a `<ul>` of `<li>` elements, matching VLT's own listing templates, so assistive technology announces the number of items

```{important}
Write a variation by starting from the VLT variation closest to what you want—here that is `GridTemplate`, since the fleet is a two-column card grid—and change only what has to change.

The image props illustrate why. `sizes` tells the browser how wide the image will actually render, so that it downloads the right scale; omit it and the cards look soft for no visible reason. It is not obvious from the outside, and it comes for free by following the shape of the template you are adapting.

The same applies to the stylesheet in Step 5.
```

The fleet deviates from `GridTemplate` in one deliberate place.
`GridTemplate` renders `Card.Image` only when an item has an image, or when a placeholder is registered for its content type.
`RobotsTemplate` always renders it, with `showPlaceholderImage`, so a robot without a photo shows Volto's default placeholder image instead of an empty space.

To show a robot-specific placeholder instead, add an image to your add-on, for example {file}`src/assets/robot-placeholder.svg`, and register it for the `robot` type in {file}`src/config/settings.ts`:

```typescript
import robotPlaceholderImage from '../assets/robot-placeholder.svg';

export default function install(config: ConfigType) {
  // ... previous configuration ...

  config.settings.placeholderImages = {
    ...config.settings.placeholderImages,
    robot: robotPlaceholderImage,
  };

  return config;
}
```

The key is the content type id, the same one you registered the Summary and Actions components against.
VLT's Teaser block and its own listing variations read the same setting, so a robot without a photo shows the same placeholder there.

```{note}
Do not put the placeholder in a folder named {file}`icons`.
Volto loads SVG files from {file}`icons` folders as inline icons rather than as image files, so they cannot be used as the source of an image.
```

### Step 4: Register RobotsTemplate

Update {file}`src/config/blocks.ts`:

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

The Listing block adds the id of the selected variation to its classes, so the block renders as `.block.listing.robots`, which the stylesheet in the next step targets.

### Step 5: Add Styles

The fleet is a two-column card grid, which is what VLT's own `grid` variation already is.
The stylesheet repeats that variation's rules for `robots`, and adds the two things the grid variation has no equivalent for: the card surface, and the actions row.

Create {file}`src/theme/blocks/_listing.scss`:

```scss
// The rules below mirror `.block.listing.grid` in VLT's
// `theme/blocks/_listing.scss` and `theme/_layout.scss`.

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
        // Raise the actions above the card's link overlay, which covers the
        // whole card, so that the buttons receive clicks. VLT does the same
        // for additional links inside a card.
        position: relative;
        z-index: 1;
        // The last of the stretching boxes: `auto` here is what pins the
        // actions to the bottom of a card that is taller than its content.
        margin-top: auto;
        padding: $spacing-medium $spacing-small 0 $spacing-small;
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

Import the partial in {file}`src/theme/_main.scss`, next to the other block partials:

```scss
@import './blocks/listing';
```

### Step 6: Test the Fleet Listing

1. Add a few robots, such as **ARM-7 Bench Arm**, **ROVER-2 Terrain Scout**, **QUAD-4 Walker**, and **DRONE-1 Surveyor**, each with a description, a charge level in the kicker, and an image.
2. Add a Listing block to a page.
3. Select the **Robot Fleet** variation in the block settings.
4. Configure the block to list the Robot content type.
5. Each robot appears with its image, summary, charge level, and a Book button, and selecting a Book button does not open the robot's page.
6. Add a robot without an image. Its card shows the placeholder, and has the same shape as the others.

(light-theme-slots-label)=

## Working with Slots

VLT provides slots for extending the layout without component shadowing. This section adds a practical example: a sign-up form for **Signal**, the Robotarium's workshop bulletin, in the `preFooter` slot.

### Available Slots

Volto renders four slots itself, and VLT's header and footer add the others.
Several of them already contain components when you start:

| Slot | Where it renders | Rendered by | Registered by default |
| --- | --- | --- | --- |
| `aboveApp` | Around the whole app | Volto | `plone-components-css`, in the CMS UI only |
| `aboveContent` | Above the content | Volto | — |
| `belowContent` | Below the content | Volto | `tags`, `relatedItems` |
| `aboveListingItems` | Inside a Listing block, above the items | Volto and VLT | — |
| `aboveHeader` | Above the header | VLT | `Theming`, `StickyMenu` |
| `belowHeader` | Below the header | VLT | — |
| `headerTools` | Top right of the header, and in the mobile menu | VLT | `Anontools` |
| `preFooter` | Top of the footer | VLT | `footerLogos`, `MobileStickyMenu` |
| `footer` | Main footer area | VLT | `coreFooter`, only with the `kitconcept.footer` behavior |
| `postFooter` | Bottom of the footer | VLT | `PostFooterFollowUsLogoAndLinks`, `Colophon` |
| `followUs` | Social media links, inside `postFooter` | VLT | `FollowUs`, from `@plonegovbr/volto-social-media` |
| `footerLinks` | Footer links, inside `postFooter` | VLT | — |

The `followUs` slot only renders when the site has social media links, and `footerLinks` only when it has footer links.

### Step 1: Create the Signal Sign-up Component

Create {file}`src/components/SignalSignup/SignalSignup.tsx`:

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

Create {file}`src/theme/_signalSignup.scss`:

```scss
// VLT pads every non-empty container in the footer, with
// `#footer > .container:not(:empty)`. The sign-up band brings its own padding
// and its own background, so that padding would show up as a gap in the
// footer's gradient above it. Both selectors have the same specificity, and
// this one wins because it loads later.
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

Import the partial at the end of {file}`src/theme/_main.scss`:

```scss
@import './signalSignup';
```

### Step 3: Register the Component to the Slot

In {file}`src/config/settings.ts`:

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

The Signal sign-up now appears at the top of the footer on every page, after any footer logos, which shows how slots let you extend the layout without shadowing core components.

(light-theme-swap-components-label)=

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

That is the whole change. VLT's header resolves the navigation through the registry when it renders, so it picks up your component. Every other role keeps its `vlt` default, and VLT's own navigation stays registered under `vlt`, so reverting is a one-line edit, not a file deletion.

The same two steps swap any of the nine roles.

### Why Prefer This Over Shadowing

- **Explicit.** The active component is named in configuration, not implied by a file's path.
- **Composable.** Several implementations can coexist under different names, and you choose which one renders.
- **Decoupled.** You bind to a role name, not to an internal module path that can move between VLT releases.
- **Safe.** If a setting names a component that was never registered, VLT falls back to its own implementation rather than rendering nothing.
- **Typed.** The keys of `config.settings.vlt.components` are a fixed set, so a misspelled role is a compile error rather than a silent no-op.

```{note}
Your add-on's configuration must run after VLT's, so that `config.settings.vlt` exists when you assign to it.
It does, because VLT is listed in your add-on's `addons`, and Volto applies the add-ons that an add-on declares before the add-on itself.
```

(light-theme-block-model-v3-label)=

## Block Model v3 (opt-in)

Block Model v3 gives every block the same two containers in view mode and in edit mode, so a block looks the same while you edit it as it does on the published page.
VLT 8 ships it as an opt-in.
The Robotarium keeps the default, Block Model v2, and this section explains what changes when you switch.

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

The outer container uses padding rather than margin for vertical spacing, so that its background has no gaps.
In edit mode, VLT renders the same two containers, and adds the editing controls after the inner container.

### Enable Block Model v3

VLT sets `config.settings.blockModel = 2`, and copies that value to each block it has migrated: `slate`, `title`, `gridBlock`, and the Button block, `__button`.
Those blocks keep the value they had when VLT's configuration ran, which is before your add-on runs.
To switch, set the flag, and copy it to those blocks again.

In your project's {file}`src/config/settings.ts`:

```typescript
export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Enable Block Model v3 globally
  config.settings.blockModel = 3;

  // Re-apply it to the blocks VLT has migrated.
  // The Button block only exists if its add-on is installed.
  for (const type of ['slate', 'title', 'gridBlock', '__button']) {
    if (config.blocks.blocksConfig[type]) {
      config.blocks.blocksConfig[type].blockModel = config.settings.blockModel;
    }
  }

  return config;
}
```

```{important}
A block that stays on v2 still renders, but without the two containers, so it can look different from its neighbors.
Enable v3 only when every block your site uses supports it.
Block repositories that support it show a "BMv3 ready" badge.
```

(light-theme-block-categories-label)=

### Block Categories

Under v3, VLT's stylesheet sets the width of a block's inner container, and the space before the next block, according to the block's category.
The category is set at `config.blocks.blocksConfig[type].category`, and it becomes a `category-${category}` class on the outer container.
Vertical spacing between blocks comes from the **upper** block: its content sits flush with the top of its container, and the bottom padding creates the space before the next block.

VLT already assigns categories to the blocks it has migrated, so you do not need to repeat them:

| Category | Assigned to | Width of the inner container | Spacing adjustments, by the category of the neighboring block |
| --- | --- | --- | --- |
| `inline` | `slate` | narrow | no space before `separator`, more space before `action` or `heading` |
| `title` | `title` | default | no top padding on a `cards` block that follows |
| `action` | `__button` | the width chosen for the block | no space before `separator`, more space before `cards` or `inline` |
| `cards` | `gridBlock` | default | more space before `action` or `inline` |

VLT's stylesheet also has rules for a few categories that no block in VLT or in the recommended add-ons assigns yet, such as `heading` and `separator`.

Your own blocks can have a category too.
Reuse one of the four only if both its width rule and its spacing fit the block.
The Cover block is a self-contained unit, like the cards in a Grid, but `cards` fixes the inner container at the default width.
Under v3, that rule is more specific than the Cover's own `max-width`, so the Block Width control would stop working.

When none of the categories fits, add your own.
Name it for the family of blocks it describes rather than for the block that prompted it, and give it rules, because a category only means something if your stylesheets act on the `category-*` class it produces.
The Robotarium adds a `showcase` category, for full-width sections that bring their own background and padding, such as the Cover.

Add these two lines to {file}`src/config/blocks.ts`, after the Cover registration from the previous chapter:

```typescript
config.blocks.blocksConfig.cover.category = 'showcase';
config.blocks.blocksConfig.cover.blockModel = config.settings.blockModel;
```

They are worth adding even with the flag left at `2`: the Cover then follows whatever `config.settings.blockModel` holds, and `BlockWrapper` in its view reads the same value.
Under v2, the category has no effect, because only v3 renders the `category-*` class.

```{warning}
The file matters here, and so does the position within it.

{file}`src/index.ts` calls `installSettings` before `installBlocks`, so at the time {file}`config/settings.ts` runs, `config.blocks.blocksConfig.cover` does not exist yet, and the lines above would throw an error there.
They have to run after the block is registered, and after the flag is set, which {file}`config/blocks.ts` satisfies on both counts.
```

Then give the category its rules.
Create {file}`src/theme/_categories.scss`:

```scss
// Block Model v3 spacing for the `showcase` category: full-width sections
// with their own background and padding, such as the Cover block.
// VLT writes its category rules for `:not(.blocks-group-wrapper) > .block`,
// which matches the blocks that Block Model v3 renders, and these rules
// follow the same pattern.
:not(.blocks-group-wrapper) > .block.category-showcase {
  // A showcase keeps its padding inside its own background, so the space
  // before the next block goes on the outer container.
  padding-bottom: $block-vertical-space;

  // Leave more space before text and buttons, and none before a separator.
  &:has(+ .category-inline),
  &:has(+ .category-action) {
    padding-bottom: $spacing-xlarge;
  }

  &:has(+ .category-separator) {
    padding-bottom: 0;
  }
}
```

Import the partial at the end of {file}`src/theme/_main.scss`:

```scss
@import './categories';
```

Unlike `cards`, `showcase` sets no width, so the Cover's own stylesheet still decides it, and the Block Width control keeps working.

### The `volto-bm3-compat` add-on

`@kitconcept/volto-bm3-compat` provides the `BlockWrapper` component that you used in the Cover view.
It lets one view work under both block models, rendering the wrappers that v2 needs and leaving them out under v3.
VLT depends on it and declares it as an add-on, and you also listed it in your project add-on in the first chapter, because your view imports from it.

## Checkpoint

- The Signal sign-up form appears at the top of the footer on every page.
- A Listing block set to the **Robot Fleet** variation shows each charge level as a labelled bar, the Book buttons line up along the bottom of the cards whatever the description lengths, selecting a Book button does not open the robot's page, a robot without a photo shows a placeholder, and tabbing through the page reaches every robot title as a link.
- The same robot in a Teaser block renders the same title, description, and charge bar as it does in the fleet listing.
- If—and only if—you enabled Block Model v3, a Text block renders inside a `.block-inner-container` and looks the same in edit mode as in view mode, and the Cover renders with the `category-showcase` class and still follows its Block Width control. With the flag left at `2`, as the Robotarium leaves it, blocks render as before.

## Further Reading

- [Swap structural components](https://volto-light-theme.readthedocs.io/how-to-guides/swap-structural-components.html)
- [Slots reference](https://volto-light-theme.readthedocs.io/reference/slots.html)
- [Card primitive reference](https://volto-light-theme.readthedocs.io/reference/card.html)
- [Summary components](https://volto-light-theme.readthedocs.io/how-to-guides/summary.html)
- [Block Model v3](https://volto-light-theme.readthedocs.io/conceptual-guides/block-model-v3.html)
