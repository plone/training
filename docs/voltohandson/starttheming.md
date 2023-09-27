---
myst:
  html_meta:
    "description": "Learn the basics about theming in Volto"
    "property=og:description": "Learn the basics about theming in Volto"
    "property=og:title": "Theming"
    "keywords": "Plone, Volto, Training, Theme, Theming"
---

(voltohandson-default-font-label)=

# Theming

To develop our theme, we can use [Semantic UI](https://react.semantic-ui.com/) variables and theme overrides to achieve our theme, or we can use Volto's `custom.overrides`. We also can mix elements of both as needed. There is no right or wrong way of doing it, and we will be using the Semantic UI theming engine in both cases.

```{image} _static/theming_engine.png
:align: center
:alt: Theming engine diagram
```

## Basic font family

[plone.org](plone.org) uses the "Assisstant" font instead of the Volto default "Poppins". You can use Semantic UI variables for customizing the font, as it's a valuable feature.

Create a file called `site.variables`in the following path `src/addons/<your-addon-name>/theme/globals/` (which you will have to create first).

Now you need to restart Volto to make Volto aware of the new file. From now on changes in this file will be automatically applied upon save and you will see the results in your browser.

```{note}
Everytime you add a new file to your project you will have to restart your development process to make Volto aware of your new file.
```

Edit the new file and add this:

```less
@fontName: "Assisstant";
```

You can set it to any Google font available, and the online version of the font will be used.
You can also set other variables concerning the font used, such as the sizes available.
In case you want to use more than one font or a font that is self-hosted,
you should define it as usual in CSS and set the variable `importGoogleFonts` appropriately. As `Assisstant` is Google Font we will set

```less
@importGoogleFonts: true;
```

```{tip}
You can find the list with the global Semantic UI variables available in `omelette/theme/themes/default/globals/site.variables`.
```

## custom.overrides

Create a file named `src/addons/<your-addon-name>/theme/extras/custom.overrides` which will contain all the CSS concerning our local theme.
This is a file containing LESS declarations. It's loaded more quickly than the theme ones, because it's outside the theme. You should restart Volto to make Volto aware of the new file.
