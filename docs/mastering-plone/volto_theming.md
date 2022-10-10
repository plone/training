---
myst:
  html_meta:
    "description": "How to make simple customizations"
    "property=og:description": "How to make simple customizations"
    "property=og:title": "Theming in Plone 6"
    "keywords": ""
---

(volto-theming-label)=

# Theming in Volto

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend 
:class: logo
```

Solve the same tasks in Plone Classic UI in chapter {doc}`theming`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout overrides
```

Code for the end of this chapter:

```shell
git checkout theming
```
````

In this part we will:

- Override the default font
- See how to apply style rules to custom components

Topics covered:

- Small customizations of the default theme Pastanaga via CSS


While developing a theme with Semantic UI, two cases appear:

- Some attributes, like the overall font, are covered by Semantic UI variables.
- Other attributes need custom CSS rules.

We start with the first case and change the font to another Google font, Lato.
The overall font is defined in Volto and can be found in {file}`omelette/theme/themes/default/globals/site.variables`. So create an empty file {file}`site.variables` in {file}`theme/globals/` and set your font.

```css
@importGoogleFonts : true;
@fontName : 'Lato';
@emSize: 18px;
```

Volto expects the font files to be present in our app.
While developing we tell Volto to load Google fonts from Google with `@importGoogleFonts : true;`.

Semantic UI does not provide a less variable for increasing the letter-spacing.
So we add a CSS rule for it.
We use {file}`site.overrides` as this rule should apply site wide.
Create a file {file}`theme/globals/site.overrides` and set the letter-spacing:

```css
#main {
    letter-spacing: .05em;
}
```

We can use variables and theme overrides to achieve our theme, or we can use Volto’s {file}`custom.overrides`, or we can mix elements of both as needed.
There is no right or wrong way of doing it, and we will be using the Semantic UI theming engine in both cases.

There are two files {file}`theme/extras/custom.overrides` and {file}`theme/extras/custom.variables` for everything not belonging to default Volto, e.g. header, navigation, breadcrumbs, etc..
It's a convention to put styling of additional non-default components in {file}`custom.overrides` and {file}`custom.variables`.

In chapter {ref}`volto-sponsors-component-label` we will create a custom component to show the sponsors of our conference.
We style this component in {file}`theme/extras/custom.overrides`

```css
.ui.segment.sponsors {
  background-color: rgb(177, 192, 219);
}
```

Relying on the Semantic UI based Pastanaga theme, we use variables such as:

```css
.ui.segment.sponsors {
  background-color: @lightGrey;
}
```
