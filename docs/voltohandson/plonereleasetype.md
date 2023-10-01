---
myst:
  html_meta:
    "description": "Learn How to code a custom View for a content type"
    "property=og:description": "Learn How to code a custom View for a content type"
    "property=og:title": "Content Type Views"
    "keywords": "Plone, Volto, Training, View, Content Types"
---

# Plone Release content type

On plone.org we have a custom content type called "Plone Release". For the training you will recreate that content type and write a custom view for it.

Create the content type by going to the [content types control panel](http://localhost:3000/controlpanel/dexterity-types) of your app and adding a new content type called "Plone Release". Next amend the schema of that type by clicking on the three dots behind "Plone Release in the Types overview and choosing schema.
Add the following fields to the schema:

- "Version": Textline
- "Releasedate": Date
- "Changelog": Richtext

Add a "Plone Release" content Object with some dummy contents in each field somewhere on your page.

## Creating a dummy for the View

Now create a new folder inside of your addons `src/components` directory called "Views". In there add a new file called `PloneReleaseView.jsx`. Add some dummy markup for our View to that file:

```jsx
const PloneReleaseView = (props)=>{

return(
  <div>
    <p>I am the Plone Release View component!</p>
  </div>
)
}

export default PlonereleaseView;
```

Import and export this file in `components/index.js` to make it easier accessible throughout the project:
```jsx
...
import PloneReleaseView from './Views/PloneReleaseView'

export {
  ...
  PloneReleaseView
}
```

To display your new View you need to configure it in your addons root `index.js`. This is done by adding the View to the importet files in the file and then setting it as the appropriate View for the contenttype:

```jsx
  config.views.contentTypesViews.plone_release = PloneReleaseView;
```

You should see the "I am the Plone Release View" text now on your content Object.

## Displaying the actual content

The `props` passed to the View contain a `content` object that in turn contains keys of all fields available in the Object. Extract that object in your function like:
```jsx
  const { content } = props;
```

You can now use these keys to display the content in your jsx. As you not only have plaintext fields, but also a richtext field you also need to import the widget from Volto to render richtext. Import the semantic ui container element as well:

```jsx
import RichTextViewWidget from '@plone/volto/components/theme/Widgets/RichTextWidget';
import { Container } from 'semantic-ui-react';
```

```jsx
return(
  <Container>
    <h1 className="documentFirstHeading">Plone {content.version}</h1>
    <p>Version: {content.version}</p>
    <p>Release Date: {content.release_date}</p>
    <h2>Changelog</h2>
    <RichTextViewWidget value={content.changelog} />
  </Container>
)
```

## Add blocks to the content type

If you now want to include blocks in your content type as well as the regular fields you first need to enable the blocks behavior for the content type in the content types control panel. Click once again on the 3 dots next to the content type. But this time choose "Edit". Go to the "Behaviors" tab, enable the "Blocks" behavior and save.
Back at your Plone release go to edit mode. You will notice, that you now have the blocks editor like on documents. Add a few blocks of your choice and save. After saving you will notice, that your blocks are actually not displayed. This is because the blocks renderer is not included in your custom view.

Change that by importing the `RenderBlocks` component from Volto:

```jsx
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
```

And include it in your markup like:

```jsx
  <RenderBlocks {...props} />
    return (
    <Container>
      <h1 className="documentFirstHeading">Plone {content.version}</h1>
      <p>Version: {content.version}</p>
      <p>Release Date: {content.release_date}</p>
      <h2>Changelog</h2>
      <RichTextViewWidget value={content.changelog} />
      <RenderBlocks {...props} />
    </Container>
  );
```
