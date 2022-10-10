---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(mockup-writing-documentation)=

# Writing Documentation For Mockup

The documentation for Mockup is automatically generated from comments in pattern code.

The structure is as follows:

```
/* PATTERN TITLE
 *
 * Options:
 *    OPTION_TITLE(TYPE): DESCRIPTION
 *    OPTION2_TITLE(TYPE): DESCRIPTION2
 *
 * Documentation:
 *   # Markdown title
 *
 *   Markdown structured description text
 *
 *   # Example
 *
 *   {{ EXAMPLE_ANCHOR }}
 *
 *   # Example2
 *
 *   {{ EXAMPLE2_ANCHOR }}
 *
 * Example: EXAMPLE_ANCHOR
 *    <div class="pat-PATTERN_NAME"></div>
 *
 * Example2: EXAMPLE2_ANCHOR
 *    <section class="pat-PATTERN_NAME"></section>
 *
 * License:
 *   License text, if it differs from the package's license, which is
 *   declared in package.json.
 *
 */
```
