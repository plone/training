(volto-theming-label)=

# Theming in Volto

::::{sidebar} Volto chapter

:::{figure} _static/volto.svg
:alt: Volto Logo
:::

This chapter is about the React frontend Volto.

Solve the same tasks in Plone Classic in chapter {doc}`theming`
::::

:::{sidebar} Get the code! ({doc}`More info <code>`)
Code for the beginning of this chapter:

```
git checkout overrides
```

Code for the end of this chapter:

```
git checkout theming
```
:::

To develop our theme, we can use Semantic UI. There are two cases:

- Some attributes like the overall font that are covered by Semantic UI variables.
- The other case is styling of for example listing news that needs some custom CSS rules.

We start with the first case and change the font to another Google font, Lato.

The overall font is defined in Volto and can be found in {file}`omelette/theme/themes/default/globals/site.variables`. So create an empty file {file}`site.variables` in {file}`theme/globals/` and set your font.

```css
@fontName : 'Lato';
@emSize: 18px;
```

Semantic UI does not provide a less variable for increasing the letter-spacing.
So we add a CSS rule for it.
We use {file}`site.overrides` as this rule should apply site wide.
Create an empty file {file}`theme/globals/site.overrides` and set the letter-spacing:

```css
#main {
    letter-spacing: .05em;
}
```

We can use variables and theme overrides to achieve our theme, or we can use Volto’s {file}`custom.overrides`, or we can mix elements of both as needed.
There is no right or wrong way of doing it, and we will be using the Semantic UI theming engine in both cases.

There are these two files {file}`theme/extras/custom.overrides` and {file}`theme/extras/custom.variables`.
Use these tp style everything that does not belong to default Volro, e.g. not belonging to the header, navigation, breadcrumbs, etc..
It's a convention to put styling of your additional non-default components in {file}`custom.overrides` and {file}`custom.variables`.

In chapter {ref}`volto-sponsors-component-label` we will create a custom component to show the sponsors.
We style this component in {file}`theme/extras/custom.overrides`

```css
.ui.segment.sponsors {
  background-color: rgb(177, 192, 219);
}
```

You should use the power of `less` and use variables such as:

```css
.ui.segment.sponsors {
  background-color: @lightGrey;
}
```

## Changing the favicon

Find the favicon.ico in {file}`public/` and replace it with a custom favicon.

:::{note}
As you already know, the Node app Volto needs to be restarted after adding new files.
:::
