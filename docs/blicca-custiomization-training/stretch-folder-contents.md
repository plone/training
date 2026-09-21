---
myst:
    html_meta:
        "description": "Stretch goal: customize the row actions of the Blicca folder contents, open edit in a modal, and add an image cropping action."
        "property=og:description": "Stretch goal: customize the row actions of the Blicca folder contents, open edit in a modal, and add an image cropping action."
        "property=og:title": "Stretch goal: folder contents row actions"
        "keywords": "Plone, Blicca, pat-structure, folder contents, action menu, menuOptions, modal, image cropping"
---

(blicca-stretch-folder-contents-label)=

# Stretch goal: folder contents row actions

This chapter is for fast participants, and it is a real customer request.
The folder contents view, the `pat-structure` pattern, shows an action menu in every row: Open, Edit, and a dropdown with Cut, Copy, Paste, and more.
The customer wants two changes:

- Edit opens in a modal, instead of leaving the folder contents.
- Images get an additional action that opens the image cropping editor of [plone.app.imagecropping](https://github.com/plone/plone.app.imagecropping), also in a modal.

It combines {ref}`blicca-replace-pattern-label` with a look under the hood of a Backbone-based pattern.

## Why the `menuOptions` option is not enough

The pattern has an option `menuOptions`, and it looks like the answer.
It is not.
Mockup builds the menu per row in {file}`src/pat/structure/js/actionmenu.js`:

```js
const ActionMenu = function (menu) {
    // If an explicit menu was specified as an option to AppView, this
    // constructor will not override that.
    if (menu.app.menuOptions !== null) {
        return menu.app.menuOptions;
    }
    const model = menu.model.attributes;
    ...
    result.openItem.url = model.getURL + viewAction;
    result.editItem.url = model.getURL + "/edit";
    return result;
};
```

With `menuOptions` set, the generator returns your static definition for every row.
The per-row logic is skipped: the Open and Edit links get no URL, and Paste, Move, and "Set as default page" no longer depend on the item.
You could remove actions that way, but you can't add a per-item link.

## The recipe

The menu is generated in the `initialize` method of the `ActionMenuView`.
That is where we hook in.
Module federation shares only a few core modules between the Plone bundle and our add-on, so our add-on ships its own copy of the structure app.
We can patch the `ActionMenuView` of that copy, but only if our copy of the pattern is the one that runs.
This is the blacklist recipe from {ref}`blicca-replace-pattern-label`.

Add `structure` to {file}`static/pattern-blacklist.js`:

```js
window.__patternslib_patterns_blacklist = (
    window.__patternslib_patterns_blacklist || []
).concat(["markspeciallinks", "structure"]);
```

Create {file}`resources/structure/structure.js`:

```js
import $ from "jquery";
import mockupParser from "@patternslib/patternslib/src/core/mockup-parser";
import Structure from "@plone/mockup/src/pat/structure/structure";
import ActionMenuView from "@plone/mockup/src/pat/structure/js/views/actionmenu";
import utils from "@plone/mockup/src/core/utils";

// Mockup resolves menu icons while rendering the row, without awaiting the
// first fetch. Warm the icon cache for our new icon, so that the first row
// already shows it instead of the title text.
utils.resolveIcon("crop");

const original_initialize = ActionMenuView.prototype.initialize;
ActionMenuView.prototype.initialize = function (options) {
    original_initialize.call(this, options);

    // this.menuOptions is the generated menu for THIS row: Paste, Move and
    // "Set as default page" are already filtered, the URLs are resolved.
    const item = this.model.attributes;

    // 1. Open the edit form in a modal.
    this.menuOptions.editItem.css = "pat-plone-modal";

    // 2. Add the cropping editor for images, also in a modal.
    if (item.portal_type === "Image") {
        this.menuOptions.cropItem = {
            url: `${item.getURL}/@@croppingeditor`,
            title: "Crop image",
            category: "button",
            icon: "crop",
            css: "pat-plone-modal",
            modal: false,
        };
    }

    // Re-bind the click handlers, in case you add or remove entries with a
    // ``method``. Methods must exist in src/pat/structure/js/actions.js.
    this.events = this.generate_events();
    this.delegateEvents();
};

export default Structure.extend({
    name: "blicca-structure",
    trigger: ".pat-structure",
    parser: null,

    async init() {
        // Take over the options of the original, ``data-pat-structure``.
        this.options = $.extend(
            true,
            {},
            this.defaults,
            mockupParser.getOptions(this.el, "structure"),
        );
        return this.constructor.__super__.init.call(this);
    },
});
```

Import it in {file}`resources/overrides.js`, next to the `markspeciallinks` replacement.

Each menu entry has the same shape: `url`, `title`, `category`, `icon`, `css`, and `modal`.
The category `button` renders the entry next to Open and Edit, `dropdown` puts it into the gear menu.
The `css` classes end up on the link, so `pat-plone-modal` opens it in a modal.
Entries with a `method` call a method of `src/pat/structure/js/actions.js`, such as `cutClicked` or `moveTopClicked`.

```{note}
The `modal: true` flag looks like the official way, but it has no effect in Mockup 5.6.
The view appends the modal class after it has built the class list of the entry.
Set the `css` class yourself, as the comment in the view suggests.
```

## The pnpm caveat

The structure app imports `pat-select2`, and with it the patched select2 fork that Mockup installs from git.
Our {file}`pnpm-workspace.yaml` removes that fork on purpose, see {ref}`blicca-setup-label`.
For this stretch goal, allow it:

- Remove the `"select2": "-"` line from `overrides`.
- Set `"@plone/mockup": true` in `allowBuilds`.
- Add `blockExoticSubdeps: false`.

Then run `pnpm install` and `pnpm run build` again.
Mockup's postinstall script tries to patch select2, and doesn't find it in the pnpm store.
The unpatched fork only differs in how already selected items are highlighted in the related items widget, which the folder contents don't use.

## A lighter alternative: a pattern on the action menu

The prototype patch changes the generated menu itself.
If all you need is to decorate the rendered menu, add a class here, add a link there, a small pattern as in {ref}`blicca-own-pattern-label` does the job.
No blacklist, no copy of the structure app, no change to the pnpm configuration.

The hook is the registry scan that Mockup runs on every rendered row, so that the tooltips and modals on the buttons initialize.
Since Mockup 5.6.14, the row view, {file}`src/pat/structure/js/views/tablerow.js`, scans the row once it is attached to the document, and the table view scans all newly inserted rows:

```js
this.el.model = this.model;

const menuview = new ActionMenuView({ app: this.app, model: this.model });
$(".actionmenu-container", this.$el).append(await menuview.render());

// Patterns inherit configuration from ancestors, so initialize only
// after attachment. TableView scans newly inserted rows; rows rendered
// again after context-info updates are already in the document.
if (this.el.isConnected) {
    registry.scan(this.$el);
}
```

The registry is shared with our add-on, so a pattern of ours with a matching trigger runs for every row, and again whenever the rows re-render on paging, sorting, or a folder change.
The row keeps the Backbone model of the item on its DOM element, so the pattern can read `portal_type` and `getURL` from there.

```{note}
Before Mockup 5.6.14, the `ActionMenuView` scanned the menu itself, at the end of its `render()` method, while the menu was still detached from the table.
A trigger like `.pat-structure .actionmenu` did not match there, and `closest("tr")` found nothing.
The pattern below works with both versions: its trigger matches the menu element itself, and it waits a tick before it looks for the row.
```

Create {file}`resources/folder-contents-actions/actions.js`:

```js
import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import registry from "@patternslib/patternslib/src/core/registry";
import utils from "@plone/mockup/src/core/utils";

class Pattern extends BasePattern {
    static name = "blicca-folder-contents-actions";
    // Match the menu element itself: before Mockup 5.6.14 the menu was
    // scanned while still detached from the table, so a descendant selector
    // of ".pat-structure" would not match there.
    static trigger = ".btn-group.actionmenu";

    async init() {
        // Wait a tick, so that the menu is appended to its row on Mockup
        // versions that scan the menu before attaching it.
        await new Promise((resolve) => setTimeout(resolve));
        const row = this.el.closest(".pat-structure tr");
        // pat-structure stores the Backbone model of the item on its row.
        const item = row?.model?.attributes;
        if (!item) {
            return;
        }

        // 1. Open the edit form in a modal.
        const edit = this.el.querySelector("a.editItem");
        if (edit) {
            edit.classList.add("pat-plone-modal");
            registry.scan(edit);
        }

        // 2. Add the cropping editor for images, also in a modal.
        if (item.portal_type === "Image" && edit) {
            const crop = document.createElement("a");
            crop.className = "btn btn-sm action cropItem pat-plone-modal";
            crop.href = `${item.getURL}/@@croppingeditor`;
            crop.title = "Crop image";
            crop.setAttribute("aria-label", "Crop image");
            crop.innerHTML = await utils.resolveIcon("crop");
            edit.after(crop);
            registry.scan(crop);
        }
    }
}

registry.register(Pattern);
export default Pattern;
```

Import it in {file}`resources/overrides.js` instead of the structure replacement, and rebuild.
`registry.scan(link)` initializes the modal pattern on the changed link, and `utils.resolveIcon()` fetches an icon from Plone's icon resolver by its registered name.

Use one variant or the other, not both: with both active, the image row gets two crop buttons.
The solution branches are `stretch-folder-contents` for the prototype patch, and `stretch-folder-contents-pattern` for this variant.

## Checkpoint

Open the folder contents of a folder with an image.
Edit opens in a modal for every item, and the image row has a crop button that opens the cropping editor in a modal.
Change into a subfolder and back: the rows re-render, and your changes are there again.
With the prototype patch, also cut an item with the gear menu: the folder rows now offer Paste, so the re-bound click handlers work.

```{note}
The cropping action needs `plone.app.imagecropping` installed in your project.
Without it, the link returns a 404 error.
```

```{warning}
The structure app pulls a lot of code into your bundle, around 90 KB for the structure chunk alone, plus its dependencies.
Keep such a customization in the customer's add-on, and check the bundle size before you ship it.
```
