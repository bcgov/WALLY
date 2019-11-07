function coordinatesGeocoder (query) {
  // allows searching (in the geocoder/search box) for lat/long coordinates
  // this code is from the Mapbox documentation
  // https://docs.mapbox.com/mapbox-gl-js/example/mapbox-gl-geocoder-accept-coordinates/
  // match anything which looks like a decimal degrees coordinate pair
  const matches = query.match(/^[ ]*(?:Lat: )?(-?\d+\.?\d*)[, ]+(?:Lng: )?(-?\d+\.?\d*)[ ]*$/i)
  if (!matches) {
    return null
  }

  function coordinateFeature (lng, lat) {
    return {
      center: [lng, lat],
      geometry: {
        type: 'Point',
        coordinates: [lng, lat]
      },
      place_name: 'Lat: ' + lat + ' Lng: ' + lng,
      place_type: 'coordinate',
      properties: {},
      type: 'Feature'
    }
  }

  const coord1 = Number(matches[1])
  const coord2 = Number(matches[2])
  let geocodes = []

  if (coord1 < -90 || coord1 > 90) {
    // must be lng, lat
    geocodes.push(coordinateFeature(coord1, coord2))
  }

  if (coord2 < -90 || coord2 > 90) {
    // must be lat, lng
    geocodes.push(coordinateFeature(coord2, coord1))
  }

  if (geocodes.length === 0) {
    // else could be either lng, lat or lat, lng
    geocodes.push(coordinateFeature(coord1, coord2))
    geocodes.push(coordinateFeature(coord2, coord1))
  }

  return geocodes
}

export default coordinatesGeocoder
