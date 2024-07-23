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

## Set up theming for your addon

To make your project use the theme of your addon, you need to specify this in your projects `package.json` file (not in your addon). Just set the theme like `"theme":"<your-addon-name>"`. Next you need to set up the appropriate folders and files inside of your addon. Start by creating a directory called `theme` in your addons `src` directory. In there create the directories `globals` and `extras`. Next copy the `theme.config` file from the root projetcs `/theme` folder to your newly created one.
Finally edit your `theme.config` and change the `@siteFolder` variable to contain your addon name instead of `../../theme` to `<your-addon-name>/theme`. Remember to restart your Volto process.

## Basic font family

[plone.org](plone.org) uses the "Assistant" font instead of the Volto default "Poppins". You can use Semantic UI variables for customizing the font, as it's a valuable feature.

Create a file called `site.variables`in the following path `src/addons/<your-addon-name>/theme/globals/`.

Now you need to restart Volto once again to make it aware of the new file. From now on changes in this file will be automatically applied upon save and you will see the results in your browser.

```{note}
Everytime you add a new file to your project you will have to restart your development process to make Volto aware of your new file.
```

Edit the new file and add this:

```less
@fontName: "Assistant";
```

You can set it to any Google font available, and the online version of the font will be used.
You can also set other variables concerning the font used, such as the sizes available.
In case you want to use more than one font or a font that is self-hosted,
you should define it as usual in CSS and set the variable `importGoogleFonts` appropriately. As `Assistant` is a Google Font we will set:

```less
@importGoogleFonts: true;
```

Two more important variables that are changed in https://plone.org/ are:

```less
@largeMonitorBreakpoint: 1330px;
@emSize: 16px;
```
These two variables change the width of the default container.
Add them as well.


```{tip}
You can find the list with the global Semantic UI variables available in `omelette/theme/themes/default/globals/site.variables`.
```


