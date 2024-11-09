---
myst:
  html_meta:
    "description": "Learn to translate static strings in Volto"
    "property=og:description": "ILearn to translate static strings in Volto"
    "property=og:title": "Internationalization"
    "keywords": "Volto, Training, internationalization, multilingual, i18n, intl, translations"
---


# Internationalization

Though https://plone.org/ is currently an exception to this, many Plone sites are available in more than one language. For the sake of this training you can make our version of https://plone.org/ available in at least another language than english.

## Set up site to be multilingual

### Enable languages in the Plone backend
First step to making the site multilingual is to choose what languages to include from the [language controlpanel](http://localhost:3000/controlpanel/language). For in this example we will choose English (which is usually already there) and Euskara (as a nod to the 2023 Conference in the Basque Coutnry).

Then continue by installing the "Multilingual Support" (plone.app.multilingual) Addon from the [addons controlpannel](http://localhost:3000/controlpanel/addons). This will create the language root folders for the chosen languages under [http://localhost:3000/en](http://localhost:3000/en) and [http://localhost:3000/en](http://localhost:3000/eu).

### Enable languages in the frontend and add necessary folder structure

Next you need to set up your desired languages in your frontend as well. Do this by adding the following line to your addons config `index.js` to have the languages configured in your frontend:

```js
  config.settings.supportedLanguages = ['en', 'eu'];
  config.settings.isMultilingual = false;
```

And finally set up the folder structure to contain translated strings. Inside of your addons `locales` folder create folders with the short id for your used languages, with a file called `volto.po` in each. So in this case:
`/locales/en/LC_MESSAGES/volto.po` and `/locales/eu/LC_MESSAGES/volto.po`.

## Adding first translatable strings

The first parts of the site to translate would be the ones from the "Plone release" content type, you just created. Go to the `plonerelease.jsx` file and import the following at the top: `import { FormattedMessage } from 'react-intl';`

To translate a static string replace it with the `<FormattedMessage/>` component like this:

```jsx
  <FormattedMessage id="Version" defaultMessage="Version" />
```
(translation_process)=

To then be able to tranlate that to another language open your addons root in your terminal and run `yarn i18n` this will now at an entry for that string to the respective `volto.po` files. Opening the one inside of `eu/LC_MESSAGES/` you will find that it now contains the following:

```
#: components/Views/plonerelease
# defaultMessage: Version
msgid "Version"
msgstr ""
```

To add a translation, now add the translation (in this case "Bertsioa") behind `mgstr`. Next you need to run `yarn i18n` inside the projects root. This should now add your messages to the respective `<lang>.json`.

This is sufficiant for the translations to be displayed.

## Translate non JSX strings

In many cases it is necessary to translate strings that are not in the react jsx code. For example in the `schema.js` for the release block. In this case you need to import `import { defineMessages } from 'react-intl';
` in the file. Create a messages object above the actual function like this:

```js
const messages = defineMessages({

});
```
In there you can now add your translatable stings as follows:

```js
const messages = defineMessages({
  button: {
    id: 'button',
    defaultMessage: 'button',
  },
});
```

These can now be used in the actual code:

```js
{
  id: 'button',
  title: props.intl.formatMessage(messages.button),
  fields: ['buttonTitle', 'buttonLink'],
},
```

Repeat the same process as for the [above example](translation_process) to sync it into your `.po` file, translate it and sync it with the roots json file.

## Translations in customizations

Translations in customizations work a bit different than in new components. Lets take `header.jsx` as example:

Replace "Try Now" with `<FormattedMessage id="Try now" defaultMessage="Try now" />`. But this is not quite enough. You also need to go to the addons config `index.js` you now also need to `import { defineMessages } from 'react-intl'` and add:

```js
const messages = defineMessages({

});
```

In there you need to add all translatable strings from your customizations as well. Finally repeat the process for [syncing translation](translation_process).
