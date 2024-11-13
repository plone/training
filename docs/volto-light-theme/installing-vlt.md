---
myst:
  html_meta:
    "description": "Installing Volto Light Theme"
    "property=og:description": "Installing Volto Light Theme"
    "property=og:title": "Installing Volto Light Theme"
    "keywords": "Plone, Volto, Training"
---


# Installing Volto Light Theme

Follow the steps below to install and configure **Volto Light Theme** in your project. Volto Light Theme provides a clean and modern design with ready-to-use blocks and components.

### Step 1: Install Volto Light Theme

To install the **Volto Light Theme** in your project, navigate to the `frontend/packages/volto-my-project` folder and run the following command:

```shell
pnpm install @kitconcept/volto-light-theme
```

### Step 2: Add Addons (Optional)

Volto Light Theme comes with several pre-configured add-ons that provide basic blocks for your website. If you'd like to include them, you can add them to the `addons` section in your {file}`package.json`.

Here is the list of available addons you can include:

```json
  "addons": [
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-button-block",
    "@kitconcept/volto-heading-block",
    "@kitconcept/volto-highlight-block",
    "@kitconcept/volto-introduction-block",
    "@kitconcept/volto-separator-block",
    "@kitconcept/volto-slider-block",
    "@kitconcept/volto-light-theme"
  ],
```

If you don’t need any of these addons, you can skip adding them to the `addons` list.

### Step 3: Configure Volto Light Theme as the Theme Provider

To leverage a cohesive set of styles, components, and design patterns that align with Volto’s best practices, you need to set the Volto Light Theme as your theme provider.

Open the `volto.config.js` file in your `frontend` folder and modify it as shown below:

```diff
diff --git a/frontend/volto.config.js b/frontend/volto.config.js
index 56feec6..41aa96b 100644
--- a/frontend/volto.config.js
+++ b/frontend/volto.config.js
@@ -1,7 +1,7 @@
 const addons = ['volto-my-project'];
-const theme = '';
+const theme = '@kitconcept/volto-light-theme';

 module.exports = {
   addons,
-  theme
+  theme,
 };
 ```


That's it! Your project should now be using Volto Light Theme with the additional blocks and components.
