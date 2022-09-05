---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Integrating A Theme

## Integrate Bootstrap

Add the bootstrap dependency:

```shell
npm install bootstrap-sass@~3.3.7 --save
```

Create a file to manage our SCSS variables: `src/variables.scss`

```scss
$blue: #50c0e9;
$lightgrey: #f9f9f9;
```

Import Bootstrap in our main style sheet`src/styles.scss`

```scss
@import "variables.scss";

$icon-font-path: "../node_modules/bootstrap-sass/assets/fonts/bootstrap/";
@import "../node_modules/bootstrap-sass/assets/stylesheets/_bootstrap.scss";
```
