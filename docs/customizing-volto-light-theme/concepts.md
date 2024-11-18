---
myst:
  html_meta:
    "description": "Concepts"
    "property=og:description": "Concepts"
    "property=og:title": "Concepts"
    "keywords": "Plone, Volto, Training"
---

# Volto Light Theme Concepts

## Introduction

Volto Light Theme (VLT) is a customizable theme built for the Volto frontend of the Plone CMS. It provides a foundation that aims to solve many common design challenges, while remaining flexible enough for customization. It's particularly valuable because it is based on real-world experience, while simultaneously embodying the Volto vision for the future. This module will help you understand the core concepts in VLT and create a mental map of its parts.

## Core Concepts

### **Base Styling**

VLT is designed with simplicity and a minimal aesthetic in mind. Consistency, accesibility, and intuitiveness are what drive the development and improvements for VLT.

### **Customizable Variables**

VLT offers a set of CSS custom properties (variables) that allow developers to customize various design elements, such as:

- Colors
- Spatial relationships
- Layouts

These variables can be easily overridden in your project to match the desired visual identity.

### **Colors**

The color system is designed so that colors work in couples: a `background color` and a `foreground color`. The `foreground color` is often called `text color` in other systems, but since we want to use this value for more than text—like icons or borders—this works better as a generic term. Colors that do not specify `foreground` in the name are meant to be background colors.

The main color properties for a project using VLT are the following:

```
--primary-color: #fff;
--primary-foreground-color: #000;

--secondary-color: #ecebeb;
--secondary-foreground-color: #000;

--accent-color: #ecebeb;
--accent-foreground-color: #000;
```

#### **Semantic color properties**

As an additional layer on top of the main color properties, we have set in place some semantic custom properties for the basic layout sections. As a default they use the values from the main color variables, but they can be detached if desired by setting new color values. However, we feel that leaving these color relationships as they are helps create a cohesive final design. The semantic layer of properties includes the following:

```
  // Header
  --header-background: var(--primary-color);
  --header-foreground: var(--primary-foreground-color);

  //Footer
  --footer-background: var(--secondary-color);
  --footer-foreground: var(--secondary-foreground-color);

  // Fat Menu
  --fatmenu-background: var(--accent-color);
  --fatmenu-foreground: var(--accent-foreground-color);

  // Breadcrumbs
  --breadcrumbs-background: var(--accent-color);
  --breadcrumbs-foreground: var(--accent-foreground-color);

  // Search bar
  --search-background: var(--accent-color);
  --search-foreground: var(--accent-foreground-color);

  // Link color
  --link-foreground-color: var(--link-color);
```

### **Block width**

VLT now uses a standard block width definition as well. Currently, this is done via a `widget` component, `BlockWidthWidget`, that will be ported to Volto core in the near future. This component stores the value of the custom property `--block-width` so that it can be used by the StyleWrapper when injecting styles into the markup.

The three-width layout system considers the following variables:

```
  --layout-container-width: #{$layout-container-width}; // for major elements like headers, & large Blocks like the `volto-slider-block`. 
  --default-container-width: #{$default-container-width}; // a balanced content presentation for most Blocks.
  --narrow-container-width: #{$narrow-container-width}; // optimal readability.
```

The default values map the container width `SCSS` variables, which have existed in the VLT ecosystem since versions < 6.0.0-aplha.0:

```
// Container widths
$layout-container-width: 1440px !default;
$default-container-width: 940px !default;
$narrow-container-width: 620px !default;
```

### **Block alignment**

As part of the effort to generalize behaviors, another VLT `widget` is the `BlockAlignmentWidget`, which also takes adventage of the StyleWrapper by setting the `--block-alignment` property.

The three default options are:

```
  --align-left: start;
  --align-center: center;
  --align-right: end;
```

## Conclusion

VLT provides a robust foundation for Plone CMS frontend development through this framework of customizable variables and standardized block controls. Through these core concepts, VLT strikes a balance between maintaining consistency and flexibility, allowing developers to create cohesive designs while still having the freedom to customize elements to match their specific project needs.