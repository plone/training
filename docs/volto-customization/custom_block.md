---
myst:
  html_meta:
    "description": "How to add a custom block"
    "property=og:description": "How to add a custom block"
    "property=og:title": "Volto Weather Block (custom block)"
    "keywords": "Volto, Training, Custom block"
---

# Volto Weather Block (custom block)

Let's create a Volto block that will display weather information for Helsinki. For this we can use [Open-Meteo API](https://open-meteo.com/). Open-Meteo is an open-source weather API and offers free access for non-commercial use. No API key required.

Creating a basic block in Volto involves several steps. Below, I'll outline the steps to create a Volto block that displays the weather forecast in Helsinki.

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
  const location = data.location || "Helsinki, Finland";

  const [weatherData, setWeatherData] = useState(null);
  const [temperatureData, setTemperatureData] = useState(null);

  const getTemperatureColor = (temp) => {
    if (temp <= 0) return "#4B9FE1"; // Cold blue
    if (temp <= 10) return "#84CEF1"; // Cool blue
    if (temp <= 20) return "#F7B267"; // Warm orange
    return "#FF6B6B"; // Hot red
  };
  const getTemperatureHeight = (temp) => {
    // Normalize temperature to a reasonable bar height
    const baseHeight = 30; // minimum height
    const scale = 2; // multiplier for each degree
    return baseHeight + (temp + 10) * scale; // +10 to handle negative temps
  };
  useEffect(() => {
    const latitude = data.latitude || "60.17"; // Default latitude if no latitude is provided
    const longitude = data.longitude || "24.94"; // Default to longitude if no longitude is provided

    const abortController = new AbortController(); // creating an AbortController

    fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=precipitation_probability&forecast_days=1`,
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

    fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m&forecast_days=1`,
      { signal: abortController.signal } // passing the signal to the query
    )
      .then((response) => response.json())
      .then((data) => {
        setTemperatureData(data);
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
        <div className="weather-block">
          <h2>Weather Forecast for {location}</h2>
          <div className="date">
            {new Date(weatherData?.hourly?.time[0]).toLocaleDateString(
              "en-US",
              {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
              }
            )}
          </div>

          {/* Temperature Section */}
          <h3>Temperature Forecast</h3>
          <div className="temperature-legend">
            <div className="legend-item">
              <span
                className="legend-color"
                style={{ backgroundColor: "#4B9FE1" }}
              ></span>
              <span className="legend-text">Cold (≤ 0°C)</span>
            </div>
            <div className="legend-item">
              <span
                className="legend-color"
                style={{ backgroundColor: "#84CEF1" }}
              ></span>
              <span className="legend-text">Cool (1-10°C)</span>
            </div>
            <div className="legend-item">
              <span
                className="legend-color"
                style={{ backgroundColor: "#F7B267" }}
              ></span>
              <span className="legend-text">Warm (11-20°C)</span>
            </div>
            <div className="legend-item">
              <span
                className="legend-color"
                style={{ backgroundColor: "#FF6B6B" }}
              ></span>
              <span className="legend-text">Hot (>20°C)</span>
            </div>
          </div>
          <div className="hourly-forecast temperature-forecast">
            {temperatureData?.hourly?.time.map((time, index) => {
              const hour = new Date(time).getHours();
              const temperature =
                temperatureData?.hourly?.temperature_2m[index];
              return (
                <div key={time} className="hourly-item">
                  <div className="hour">{hour}:00</div>

                  <div className="temperature-container">
                    <div
                      className="temperature-bar"
                      style={{
                        height: `${getTemperatureHeight(temperature)}px`,
                        backgroundColor: getTemperatureColor(temperature),
                      }}
                    >
                      <span className="temperature-tooltip">
                        {temperature.toFixed(1)}°C
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          {/* Percipitation Section */}
          <h3>Precipitation Forecast</h3>
          <div className="hourly-forecast ">
            {weatherData?.hourly?.time.map((time, index) => {
              const hour = new Date(time).getHours();
              const probability =
                weatherData?.hourly?.precipitation_probability[index];
              return (
                <div key={time} className="hourly-item">
                  <div className="hour">{hour}:00</div>
                  <div className="probability">
                    <div
                      className="probability-bar"
                      style={{
                        height: `${probability}%`,
                        backgroundColor: `rgba(0, 0, 255, ${
                          probability / 100
                        })`,
                      }}
                    />
                  </div>
                  <div className="probability-value">{probability}%</div>
                </div>
              );
            })}
          </div>
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

5. **Add css for the Block:** In your Volto project , inside src add "theme" folder and create "weather.less" for adding style to your "Weather Block"

```less
// Variables
@primary-bg: #f5f5f5;
@text-color: #666;
@border-radius: 8px;

.weather-block {
  padding: 1rem;
  background: @primary-bg;
  border-radius: @border-radius;
  margin-bottom: 2rem;
  .date {
    font-size: 1.1rem;
    color: @text-color;
    margin-bottom: 1rem;
    font-style: italic;
  }

  .hourly-forecast {
    display: flex;
    overflow-x: auto;
    padding: 1rem 0;
    flex-flow: wrap;
    gap: 1rem;
    height: 200px;
    align-items: flex-end;
  }

  .hourly-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 40px;

    .hour {
      font-size: 0.8rem;
      color: @text-color;
      margin-bottom: 0.5rem;
    }

    .probability {
      height: 100px;
      width: 20px;
      background: #eee;
      border-radius: 10px;
      overflow: hidden;
      position: relative;

      &-bar {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.3s ease;
        border-radius: 10px;
      }

      &-value {
        font-size: 0.8rem;
        margin-top: 0.5rem;
      }
    }
  }

  .temperature-legend {
    display: flex;
    gap: 20px;
    margin: 10px 0;
    flex-wrap: wrap;
    padding: 10px;
    background: @primary-bg;
    border-radius: 4px;

    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;

      .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        display: inline-block;
      }

      .legend-text {
        font-size: 14px;
        color: @text-color;
      }
    }
  }

  .legend {
    text-align: center;
    color: @text-color;
    margin-top: 1rem;
    font-size: 0.9rem;
  }
}
```

6. **Register the Block:** In your Volto project, locate the "components/index.js" file and add an the entries for your "Weather Block"

```js
...
import WeatherEdit from './components/Blocks/Weather/Edit';
import WeatherView from './components/Blocks/Weather/View';

...
export { WeatherView, WeatherEdit };

```

We need to configure the project to make it aware of a new block by adding it to the object configuration that is located in {file}`src/config/blocks.ts`.
For that we need the two blocks components we created and a SVG icon that will be displayed in the blocks chooser.

```ts
import type { ConfigType } from '@plone/registry';
import WeatherEdit from './../components/Blocks/Weather/Edit';
import WeatherView from './../components/Blocks/Weather/View';
import worldSVG from '@plone/volto/icons/world.svg';

export default function install(config: ConfigType) {
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
  };

  return config;
};
...
```

And then import the block config in {file}`src/index.ts` along with the css for the weather block.

```ts
import type { ConfigType } from "@plone/registry";
import installSettings from "./config/settings";
import installBlocks from "./config/blocks";
import "./theme/weather.less";
function applyConfig(config: ConfigType) {
  installSettings(config);
  installBlocks(config);
  return config;
}

export default applyConfig;
```

7. **Use the Weather Block:** In Volto's Dexterity-based content types, create or edit a content type that includes the "Weather Block" in the allowedBlocks field. Then, create a content item and add the "Weather Block" to display the weather information for the location you specify.

Additionally, you may customize the UI and add more weather details based on the API's response data as needed.
