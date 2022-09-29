# Configure a released Volto Add-on in your project

1. If you already have a Volto project, update `package.json`:

```json
"addons": [
    "@kitconcept/volto-blocks-grid"
],

"dependencies": {
    "@kitconcept/volto-blocks-grid": "*"
}
```

2. Run `yarn` to download the released package.
3. Run the project, the add-on should be loaded and configured