const featureCollection = {
    "type": "FeatureCollection",
    "features": []
  }

export const sources = [
    {
        name: 'selectedStreamSource',
        options: featureCollection
    },
    {
        name: 'upStreamSource',
        options: featureCollection
    },
    {
        name: 'downStreamSource',
        options: featureCollection
    },
]

export const layers = [
    {
        "id": "selectedstream",
        "type": "line",
        "source": sources[0].name,
        "layout": {
        "line-join": "round",
        "line-cap": "round"
        },
        "paint": {
            "line-color": "#1500ff",
            "line-width": 3
        }
    },
    {
        "id": "upstream",
        "type": "line",
        "source": sources[1].name,
        "layout": {
          "line-join": "round",
          "line-cap": "round"
        },
        "paint": {
            "line-color": "#00ff26",
            "line-width": 3
        }
    },
    {
        "id": "downstream",
        "type": "line",
        "source": sources[2].name,
        "layout": {
          "line-join": "round",
          "line-cap": "round"
        },
        "paint": {
            "line-color": "#ff4800",
            "line-width": 3
        }
    }
]