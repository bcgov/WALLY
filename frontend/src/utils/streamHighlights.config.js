const featureCollection = {
    "type": "FeatureCollection",
    "features": []
  }

export const sources = [
    {
        name: "selectedStreamSource",
        options: featureCollection
    },
    {
        name: "upStreamSource",
        options: featureCollection
    },
    {
        name: "downStreamSource",
        options: featureCollection
    },
    {
        name: "selectedStreamBufferSource",
        options: featureCollection
    },
    {
        name: "upStreamBufferSource",
        options: featureCollection
    },
    {
        name: "downStreamBufferSource",
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
    },
    {
        "id": "selectedstreambuffer",
        "type": "fill",
        "source": sources[3].name,
        "layout": {
        },
        "paint": {
            "fill-color": "rgba(21, 0, 255, 0.25)"
        }
    },
    {
        "id": "upstreambuffer",
        "type": "fill",
        "source": sources[4].name,
        "layout": {
        },
        "paint": {
            "fill-color": "rgba(0, 255, 38, 0.25)"
        }
    },
    {
        "id": "downstreambuffer",
        "type": "fill",
        "source": sources[5].name,
        "layout": {
        },
        "paint": {
            "fill-color": "rgba(255, 72, 0, 0.25)"
        }
    }
]