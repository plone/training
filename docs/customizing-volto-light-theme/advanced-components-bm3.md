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
<Card href="/path/to/item">
  <Card.Image src="/path/to/image" />
  <Card.Summary>
    <h2>Title</h2>
    <p>Summary text goes here.</p>
  </Card.Summary>
  <Card.Actions>
    <Button>Action 1</Button>
  </Card.Actions>
</Card>
```

### Card Variations

- **Vertical layout** (default): Image on top
- **Horizontal layout**: Image on left or right
- **Contained**: With background color from theme
- **Listing**: Image displayed on left with specific size (controlled by `--card-listing-image-size`, default 220px)

### Card.Image Slot

Display an image using a `src` prop or use a Plone image object:

```tsx
<Card.Image image={image} />
```

Custom image component:

```tsx
<Card.Image
  src="/path/to/image"
  imageComponent={MyCustomImageComponent}
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

## Creating Custom Summary Components

The Summary component displays content metadata in listings, teasers, and cards. VLT includes built-in implementations:

- `DefaultSummary`: Kicker, title, and description
- `NewsItemSummary`: Publication date, kicker, title, description
- `EventSummary`: Start/end date, kicker, title, description
- `FileSummary`: File size and type

### Step 1: Create Product Content Type

First, create a custom "Product" content type through the Plone UI:

1. Go to http://localhost:3000/controlpanel/dexterity-types
2. Click "Add New Content Type"
3. Fill in:
   - **Type Name**: Product
   - **Short Name**: product (auto-filled)
   - **Description**: A product with pricing information
4. Click "Add"
5. In the "Behaviors" tab, enable:
   - "Kicker" (we'll use this field to store the price)
   - "Preview image"
   - Any other desired behaviors (Dublin Core, etc.)
6. Click "Save"

### Step 2: Create a Custom Summary Component

Create `src/components/Summary/ProductSummary.tsx`:

```tsx
import { FormattedNumber } from 'react-intl';

const ProductSummary = ({ item }) => {
  const {
    title,
    description,
    HeadingTag = 'h3',
    head_title,
    currency = 'EUR',
  } = item;
  const price = parseFloat(head_title);

  return (
    <>
      <HeadingTag className="product-title">
        {title ? title : item.id}
      </HeadingTag>
      {description && <p className="product-description">{description}</p>}
      {head_title && !isNaN(price) && (
        <div className="product-price">
          <span className="price">
            <FormattedNumber
              value={price}
              style="currency"
              currency={currency}
            />
          </span>
        </div>
      )}
    </>
  );
};

ProductSummary.hideLink = false;
export default ProductSummary;
```

**Note**: We use the `head_title` field (kicker) to store price information. The price is formatted using `FormattedNumber` for proper currency display with EUR as default. In a real project, you would create custom fields for price and currency.

### Step 3: Add Styles for Product Summary

Create `src/theme/_productSummary.scss`:

```scss
.products .card .card-summary {
  padding-bottom: 0 !important;
  .product-price {
    font-size: 1.25rem;
    color: var(--accent-color);
    margin-top: 0.5rem;

    .price {
      background: var(--theme-high-contrast-color);
      padding: 0.25rem 0.75rem;
      border-radius: 4px;
    }
  }

  .product-title {
    margin-top: 0;
  }
}
```

Import in `src/theme/_main.scss`:

```scss
@import './blocks/hero';
@import './blocks/relatedItems';
@import './productSummary';
@import './site';
```

### Step 4: Register the Summary Component

In `src/config/settings.ts`:

```typescript
import ProductSummary from '../components/Summary/ProductSummary';

export default function install(config: ConfigType) {
  // ... previous config ...

  config.registerComponent({
    name: 'Summary',
    component: ProductSummary,
    dependencies: ['product'],
  });

  return config;
}
```

### Step 5: Test the Product Summary

1. Create a Product item in your site
2. Fill in the title, description, and kicker field (e.g., "$99.99")
3. Add the Product to a Listing or Teaser block
4. The custom ProductSummary will display the price, title, and description

## Creating Custom Listing Variations with Card Actions

Listing variations customize content display in Listing blocks. Let's create a ProductTemplate demonstrating the Card.Actions slot for interactive buttons.

### Card.Actions Slot

The Card.Actions slot provides interactive elements beyond the main card link:
- "Add to Cart" or "Get Now" buttons for products
- "Download" buttons for files
- "Register" buttons for events

### Step 1: Create ProductActions Component

Create `src/components/Actions/ProductActions.tsx`:

```tsx
const ProductActions = ({ item }) => {
  return (
    <>
      <button className="rent-now-button button">Rent now</button>
    </>
  );
};

export default ProductActions;
```

### Step 2: Register ProductActions

Update `src/config/settings.ts`:

```typescript
import ProductActions from '../components/Actions/ProductActions';

export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Register ProductActions component
  config.registerComponent({
    name: 'Actions',
    component: ProductActions,
    dependencies: ['product'],
  });

  return config;
}
```

### Step 3: Create ProductTemplate Listing Variation

Create `src/components/blocks/Listing/ProductTemplate.tsx`:

```tsx
import React from 'react';
import PropTypes from 'prop-types';
import ConditionalLink from '@plone/volto/components/manage/ConditionalLink/ConditionalLink';
import Card from '@kitconcept/volto-light-theme/primitives/Card/Card';
import { flattenToAppURL, isInternalURL } from '@plone/volto/helpers/Url/Url';
import config from '@plone/volto/registry';
import DefaultSummary from '@kitconcept/volto-light-theme/components/Summary/DefaultSummary';
import cx from 'classnames';

const ProductTemplate = ({ items, linkTitle, linkHref, isEditMode }) => {
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
      <div className="items">
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

          return (
            <div
              className={cx('listing-item', {
                [`${item['@type']?.toLowerCase()}-listing`]: item['@type'],
              })}
              key={item['@id']}
            >
              <Card href={showLink ? item['@id'] : null}>
                {item.image_field !== '' && (
                  <Card.Image
                    className="item-image"
                    item={item}
                    imageComponent={PreviewImageComponent}
                  />
                )}
                <Card.Summary>
                  <Summary item={item} HeadingTag="h2" />
                </Card.Summary>
                <Card.Actions>
                  {Actions && <Actions item={item} />}
                </Card.Actions>
              </Card>
            </div>
          );
        })}
      </div>

      {link && <div className="footer">{link}</div>}
    </>
  );
};

ProductTemplate.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkTitle: PropTypes.string,
  linkHref: PropTypes.any,
  isEditMode: PropTypes.bool,
};

export default ProductTemplate;
```

**Key Features:**
- Uses `config.getComponent()` to fetch registered Summary/Actions components by content type
- `showLink` ensures cards are only clickable when appropriate
- `isEditMode` disables navigation during editing
- Dynamically renders Actions only for content types that have them registered

### Step 4: Register ProductTemplate

Update `src/config/blocks.ts`:

```typescript
import ProductTemplate from '../components/blocks/Listing/ProductTemplate';

export default function install(config: ConfigType) {
  // ... previous configuration ...

  // Register ProductTemplate listing variation
  config.blocks.blocksConfig.listing.variations = [
    ...(config.blocks.blocksConfig.listing.variations || []),
    {
      id: 'products',
      title: 'Products',
      template: ProductTemplate,
    },
  ];

  return config;
}
```

### Step 5: Add Styles

Create `src/theme/blocks/_listing.scss`:

```scss
.block.listing {
  &.products {
    max-width: var(--default-container-width) !important;
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
          padding-bottom: 20px !important;
        }
      }
    }
    .headline {
      @include block-title();
      margin-right: 0 !important;
      margin-left: 0 !important;
    }
    .listing-item {
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
        flex-grow: 1;
        .card-inner {
          background: var(--theme-high-contrast-color);
          .image-wrapper {
            img {
              width: 100%;
              margin: 0;
              aspect-ratio: var(--image-aspect-ratio, $aspect-ratio) !important;
            }
          }
          .card-summary {
            padding: 0 $spacing-large $spacing-large $spacing-large;
            margin-top: $spacing-medium;

            .headline {
              padding: 0 !important;
              margin-bottom: $spacing-small;
              letter-spacing: 1px;
              text-transform: uppercase;
              @include headtitle1();
              @include word-break();
            }

            h2 {
              margin: 0 0 $spacing-small 0;
              @include text-heading-h3();
            }
            p {
              margin-bottom: 0;
              @include body-text();
            }
            p:empty {
              display: none;
            }
          }

          .product-price {
            display: flex;
            justify-content: end;
            padding: $spacing-small;

            .price {
              font-size: 2.5rem;
              width: 30%;
            }
          }
        }

        .actions-wrapper {
          display: flex;
          justify-content: end;
          padding: 0 $spacing-large $spacing-medium $spacing-large;
          .rent-now-button {
            width: 30%;
            padding: 0.75rem 1rem;
            margin: 1rem;
            background-color: var(--accent-color);
            color: white;
            border: none;
            cursor: pointer;
            transition: opacity 0.2s;

            &:hover {
              opacity: 0.9;
            }
          }
        }
      }
    }
  }
}
```

Import in `src/theme/_main.scss`:

```scss
@import './blocks/hero';
@import './blocks/relatedItems';
@import './blocks/listing';
@import './productSummary';
@import './site';
```

### Step 6: Test the Product Listing

1. Create Product items with title, description, kicker (price), and images
2. Add a Listing block to a page
3. Select "Products" variation in block settings
4. Configure to show Product content type
5. Products display with image, summary, and "Get now" button

## Working with Slots

VLT provides slots for extending the layout without component shadowing. Let's create a practical example: a newsletter signup component in the preFooter slot.

### Available Slots

- `aboveHeader`: Content above header
- `belowHeader`: Content below header
- `headerTools`: Header tools at top-right (includes Anontools by default)
- `preFooter`: Before footer
- `postFooter`: After footer
- `footer`: Main footer area
- `footerLinks`: Footer links section
- `followUs`: Social media section

### Step 1: Create Newsletter Signup Component

Create `src/components/NewsletterSignup/NewsletterSignup.tsx`:

```tsx
import React, { useState } from 'react';

const NewsletterSignup = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real implementation, this would submit to a newsletter service
    console.log('Newsletter signup:', email);
    alert(`Thanks for signing up with ${email}!`);
    setEmail('');
  };

  return (
    <div className="newsletter-signup">
      <div className="newsletter-container">
        <h2 className="newsletter-title">Stay Updated</h2>
        <p className="newsletter-description">
          Subscribe to our newsletter for the latest updates and news.
        </p>
        <form onSubmit={handleSubmit} className="newsletter-form">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            className="newsletter-input"
          />
          <button type="submit" className="newsletter-button">
            Subscribe
          </button>
        </form>
      </div>
    </div>
  );
};

export default NewsletterSignup;
```

### Step 2: Add Styles

Create `src/theme/_newsletterSignup.scss`:

```scss
.newsletter-signup {
  background-color: var(--secondary-color);
  color: var(--secondary-foreground-color);
  padding: 4rem 2rem;

  .newsletter-container {
    max-width: var(--default-container-width);
    margin: 0 auto;
    text-align: center;
  }

  .newsletter-title {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .newsletter-description {
    font-size: 1.125rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .newsletter-form {
    display: flex;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
    flex-wrap: wrap;
    justify-content: center;

    .newsletter-input {
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

    .newsletter-button {
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
@import './blocks/hero';
@import './blocks/relatedItems';
@import './blocks/listing';
@import './productSummary';
@import './site';
@import './newsletterSignup';
```

### Step 3: Register the Component to the Slot

In `src/config/settings.ts`:

```typescript
import NewsletterSignup from '../components/NewsletterSignup/NewsletterSignup';

export default function install(config: ConfigType) {
  // ... previous config ...

  config.registerSlotComponent({
    name: 'NewsletterSignup',
    slot: 'preFooter',
    component: NewsletterSignup,
  });

  return config;
}
```

The newsletter signup component will now appear before the footer on all pages, demonstrating how slots enable you to extend the layout without shadowing core components.

## Site Customization Behaviors

VLT provides backend behaviors for site customization that you activated earlier. These behaviors enable fields for customizing the site without code changes.

### Header Customization Options

Through the Plone UI, you can customize:
- **Site logo**: Main logo in the top left
- **Complementary logo**: Second logo on the right side
- **Fat menu**: Enabled by default, can be disabled
- **Intranet header**: Alternative header for intranet sites
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
- Full width (extends edge to edge)
- Handles background colors and theme variables
- Uses padding (not margin) for vertical spacing
- CSS Classes: `.block.${type}.category-${category}`

**Secondary/Inner Container:**
- Controls content width constraints
- Provides consistent inter-block spacing
- Supports content alignment through CSS Grid
- CSS Class: `.block-inner-container`

### Enable Block Model v3

In your project's `src/config/settings.ts`:

```typescript
export default function install(config: ConfigType) {
  // Enable Block Model v3
  config.settings.blockModel = 3;
  config.blocks.blocksConfig.slate.blockModel = config.settings.blockModel;
  config.blocks.blocksConfig.title.blockModel = config.settings.blockModel;
  config.blocks.blocksConfig.__button.blockModel = config.settings.blockModel;
  // Define block categories for spacing
  config.blocks.blocksConfig.slate.category = 'inline';
  config.blocks.blocksConfig.title.category = 'title';
  config.blocks.blocksConfig.__button.category = 'action';

  return config;
}
```

### Block Categories

Block categories determine spacing relationships between adjacent blocks. Categories are available at `config.blocks.blocksConfig.[$type].category`.

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

---
