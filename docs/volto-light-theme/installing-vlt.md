---
myst:
  html_meta:
    "description": "Installing Volto Light Theme"
    "property=og:description": "Installing Volto Light Theme"
    "property=og:title": "Installing Volto Light Theme"
    "keywords": "Plone, Volto, Training"
---

# Installing Volto Light Theme

First for installing volto light theme.

Go to your addon project. It is present in frontend/packages/volto-my-project and install volto-light-theme


```
pnpm install @kitconcept/volto-light-theme

```

After installing vlt you will see this diff with some additional but this one is most important.

```
diff --git a/frontend/packages/volto-my-project/package.json b/frontend/packages/volto-my-project/package.json
index e256491..373386e 100644
--- a/frontend/packages/volto-my-project/package.json
+++ b/frontend/packages/volto-my-project/package.json
@@ -26,7 +26,9 @@
     "release-major-alpha": "release-it major --preRelease=alpha",
     "release-alpha": "release-it --preRelease=alpha"
   ,
-  "dependencies": {},
+  "dependencies": {
+    "@kitconcept/volto-light-theme": "^5.0.1"
+  },
   "peerDependencies":
     "react": "18.2.0",
     "react-dom": "18.2.0"

```

