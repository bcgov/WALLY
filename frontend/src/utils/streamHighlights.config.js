const featureCollection = {
  'type': 'FeatureCollection',
  'features': []
}

export const sources = [
  {
    name: 'selectedStreamSource',
    options: featureCollection
  },
  {
    name: 'upstreamSource',
    options: featureCollection
  },
  {
    name: 'downstreamSource',
    options: featureCollection
  },
  {
    name: 'selectedStreamBufferSource',
    options: featureCollection
  },
  {
    name: 'upStreamBufferSource',
    options: featureCollection
  },
  {
    name: 'downStreamBufferSource',
    options: featureCollection
  }
]

export const layers = [
  {
    'id': 'selectedStream',
    'type': 'line',
    'source': sources[0].name,
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#1500ff',
      'line-width': 3
    }
  },
  {
    'id': 'upstream',
    'type': 'line',
    'source': sources[1].name,
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#00ff26',
      'line-width': 3
    }
  },
  {
    'id': 'downstream',
    'type': 'line',
    'source': sources[2].name,
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#ff4800',
      'line-width': 3
    }
  },
  {
    'id': 'selectedStreamBuffer',
    'type': 'fill',
    'source': sources[3].name,
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(21, 0, 255, 0.25)'
    }
  },
  {
    'id': 'upstreamBuffer',
    'type': 'fill',
    'source': sources[4].name,
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(0, 255, 38, 0.25)'
    }
  },
  {
    'id': 'downstreamBuffer',
    'type': 'fill',
    'source': sources[5].name,
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(255, 72, 0, 0.25)'
    }
  }
]
