---
myst:
  html_meta:
    "description": "Installing Volto Light Theme"
    "property=og:description": "Installing Volto Light Theme"
    "property=og:title": "Installing Volto Light Theme"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---


# Installing Volto Light Theme

Follow the steps below to install and configure VLT in your project. VLT provides a clean and modern design with ready-to-use blocks and components.

### Step 1: Install Volto Light Theme

To install VLT, navigate to the {file}`frontend/packages/volto-my-project` folder and run the following command:

```shell
pnpm install @kitconcept/volto-light-theme
```

While in your project package folder, add VLT to the `addons` list in your {file}`package.json`, as follows:

```json
"addons": ["@kitconcept/volto-light-theme"],
```

### Step 2: install block add-ons

Volto Light Theme comes with several pre-configured add-ons that provide basic blocks for your website. If you'd like to include them, you can add them in the `addons` section in your {file}`package.json`, but this is not required.

Here is the list of recommended addons to install, including VLT, which should be the last element:

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

### Step 3: configure Volto Light Theme as the theme provider

To leverage a cohesive set of styles, components, and design patterns that align with Volto's best practices, you need to set VLT as your theme provider.

Open the {file}`volto.config.js` file in your {file}`frontend` folder, and modify it as shown below:

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

You'll need to restart your Plone frontend to see the changes.

That's it! Your project should now be using Volto Light Theme with its additional blocks and components.
