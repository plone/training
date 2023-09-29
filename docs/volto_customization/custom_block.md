---
myst:
  html_meta:
    "description": "How to add a custom block"
    "property=og:description": "How to add a custom block"
    "property=og:title": "Volto Weather Block (custom block)"
    "keywords": "Volto, Training, Custom block"
---

# Volto Weather Block (custom block)

Let's create a volto block that will display weather information for Eibar. For this we can use <a target="_blank" href="https://open-meteo.com/">Open-Meteo API</a>. Open-Meteo is an open-source weather API and offers free access for non-commercial use. No API key required.

Creating a basic block in Volto, involves several steps. Below, I'll outline the steps to create a Volto block that displays the weather forecast in Eibar.

1. **Setup Your Volto Project:** If you haven't already, set up a Volto project. You can use the instructions presented in [Installation -> Bootstrap a new Volto project](installation.md#bootstrap-a-new-volto-project) section.

2. **Create a New Block:** In your Volto project directory, navigate to the "src/components" folder and locate/create the "Blocks" directory. Create a new folder for your custom block; let's name it "Weather".

3. **Define the Block Schema:** Inside the "Weather" folder, create a "schema.js" file to define your block's schema. Here's a basic schema for our block needs:

```{code-block} js
export const weatherBlockSchema = (props) => {
  return {
    title: 'Weather Block',
    description: 'Display weather information for location.',
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['latitude', 'longitude'],
      },
    ],
    properties: {
      latitude: {
        title: 'Latitude',
        description:
          'Enter the latitude of the location for which you want to display the weather (e.g., 43.1849).',
        widget: 'text',
      },
      longitude: {
        title: 'Longitude',
        description:
          'Enter the longitude of the location for which you want to display the weather (e.g., -2.4716).',
        widget: 'text',
      },
    },
    required: ['latitude', 'longitude'],
  };
};

export default weatherBlockSchema;
```

4. **Create the Block Component:** Inside the "Weather" folder, create a "Block.js" file to define your block's React component. This component will make an API request to fetch the weather data and display it:

```{code-block} jsx

```

```{code-block} jsx

```

5. **Register the Block:** In your Volto project, locate the "blocks.blocks.js" file and add an entry for your "Weather Block"

```{code-block} js

```

6. **Use the Weather Block:** In Volto's Dexterity-based content types, create or edit a content type that includes the "Weather Block" in the allowedBlocks field. Then, create a content item and add the "Weather Block" to display the weather information for the location you specify.

Additionally, you may customize the UI and add more weather details based on the API's response data as needed.
