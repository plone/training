---
myst:
  html_meta:
    "description": "How to add a custom block"
    "property=og:description": "How to add a custom block"
    "property=og:title": "Volto Weather Block (custom block)"
    "keywords": "Volto, Training, Custom block"
---

# Volto Weather Block (custom block)

Let's create a Volto block that will display weather information for Brasilia. For this we can use [Open-Meteo API](https://open-meteo.com/). Open-Meteo is an open-source weather API and offers free access for non-commercial use. No API key required.

Creating a basic block in Volto involves several steps. Below, I'll outline the steps to create a Volto block that displays the weather forecast in Brasilia.

1. **Setup Your Volto Project:** If you haven't already, set up a Volto project. You can use the instructions presented in [Installation -> Bootstrap a new Volto project](installation.md) section.

2. **Create a New Block:** In your Volto project directory, navigate to the "src/components" folder and locate/create the "Blocks" directory. Create a new folder for your custom block; let's name it "Weather".

3. **Define the Block Schema:** Inside the "Weather" folder, create a "schema.js" file to define your block's schema. Here's a basic schema for our block needs:

```js
export const weatherBlockSchema = (props) => {
  return {
    title: "Weather Block",
    description: "Display weather information for location.",
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["latitude", "longitude", "location"],
      },
    ],
    properties: {
      latitude: {
        title: "Latitude",
        description:
          "Enter the latitude of the location for which you want to display the weather (e.g., 43.1849).",
        widget: "text",
      },
      longitude: {
        title: "Longitude",
        description:
          "Enter the longitude of the location for which you want to display the weather (e.g., -2.4716).",
        widget: "text",
      },
      location: {
        title: "Location",
        description:
          "Enter the name of the location for which you want to display the weather (e.g., Brasilia, Brazil).",
        widget: "text",
      },
    },
    required: ["latitude", "longitude", "location"],
  };
};

export default weatherBlockSchema;
```

4. **Create the Block Component:** Inside the "Weather" folder, create a "View.jsx" file to define your block's React component. This component will make an API request to fetch the weather data and display it:

```jsx
import React, { useEffect, useState } from "react";

const View = (props) => {
  const { data = {} } = props;
  const location = data.location || "Brasilia, Brazil";

  const [weatherData, setWeatherData] = useState(null);
  useEffect(() => {
    const latitude = data.latitude || "-15.7797"; // Default latitude if no latitude is provided
    const longitude = data.longitude || "-47.9297"; // Default to longitude if no longitude is provided

    const abortController = new AbortController(); // creating an AbortController

    fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&timezone=auto`,
      { signal: abortController.signal } // passing the signal to the query
    )
      .then((response) => response.json())
      .then((data) => {
        setWeatherData(data);
      })
      .catch((error) => {
        if (error.name === "AbortError") return;
        console.error("Error fetching weather data:", error);
        throw error;
      });

    return () => {
      abortController.abort(); // stop the query by aborting on the AbortController on unmount
    };
  }, [data.latitude, data.longitude]);

  return (
    <>
      {weatherData ? (
        <div>
          <h2>Weather in {location}</h2>
          <p>Temperature: {weatherData.current_weather.temperature} &deg;C</p>
        </div>
      ) : (
        <p>Loading weather data...</p>
      )}
    </>
  );
};
export default View;
```

You should also create a "Edit.jsx" file. The BlockDataForm component will transform the schema.js data into a usable sidebar.

```jsx
import React, { useMemo } from "react";
import { SidebarPortal } from "@plone/volto/components";
import BlockDataForm from "@plone/volto/components/manage/Form/BlockDataForm";
import weatherBlockSchema from "./schema";
import View from "./View";

const Edit = (props) => {
  const schema = useMemo(() => weatherBlockSchema(props), [props]);

  return (
    <>
      <View {...props} mode="edit" />

      <SidebarPortal selected={props.selected}>
        <BlockDataForm
          schema={schema}
          title={schema.title}
          onChangeField={(id, value) => {
            props.onChangeBlock(props.block, {
              ...props.data,
              [id]: value,
            });
          }}
          onChangeBlock={props.onChangeBlock}
          formData={props.data}
          block={props.block}
        />
      </SidebarPortal>
    </>
  );
};

export default Edit;
```

5. **Register the Block:** In your Volto project, locate the "components/index.js" file and add an the entries for your "Weather Block"

```js
...
import WeatherEdit from './components/Blocks/Weather/Edit';
import WeatherView from './components/Blocks/Weather/View';

...
export { WeatherView, WeatherEdit };

```

We need to configure the project to make it aware of a new block by adding it to the object configuration that is located in "src/config.js". For that we need the 2 blocks components we created and a svg icon that will be displayed in the blocks chooser.

```js
import WeatherEdit from './components/Blocks/Weather/Edit';
import WeatherView from './components/Blocks/Weather/View';
import worldSVG from '@plone/volto/icons/world.svg';
...
export default function applyConfig(config) {

  ...

  config.blocks.blocksConfig.weather = {
    id: 'weather',
    title: 'Weather',
    icon: worldSVG,
    group: 'common',
    edit: WeatherEdit,
    view: WeatherView,
    restricted: false,
    mostUsed: false,
    sidebarTab: 1,
    blocks: {},
    security: {
      addPermission: [],
      view: [],
    },
  };

  ...

  return config;
};
...
```

6. **Use the Weather Block:** In Volto's Dexterity-based content types, create or edit a content type that includes the "Weather Block" in the allowedBlocks field. Then, create a content item and add the "Weather Block" to display the weather information for the location you specify.

Additionally, you may customize the UI and add more weather details based on the API's response data as needed.
