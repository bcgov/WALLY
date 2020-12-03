import proj4 from 'proj4'
export function to4326 (fromProjection, coordinates) {
  // console.log('converting', coordinates, fromProjection)
  return proj4(fromProjection, 'WGS84', coordinates)
}

export function convertPoint (fromProjection, coordinates) {
  return to4326(fromProjection, coordinates)
}

export function convertLineString (fromProjection, coordinates) {
  const newCoords = []
  coordinates.forEach(coords => {
    newCoords.push(to4326(fromProjection, coords))
  })
  return newCoords
}

export function convertMultiLineString (fromProjection, coordinates) {
  const newCoords = []
  let newCoords2
  coordinates.forEach(coords => {
    newCoords2 = []
    coords.forEach(coords2 => {
      newCoords2.push(to4326(fromProjection, coords2))
    })
    newCoords.push(newCoords2)
  })
  return newCoords
}

export function convertGeometryCoords (projection, geometry) {
  if (geometry === null) {
    return null
  }

  let coords4326 = []

  switch (geometry.type) {
    case 'Point':
      coords4326 = convertPoint(projection, geometry.coordinates)
      break
    case 'LineString':
      coords4326 = convertLineString(projection, geometry.coordinates)
      break
    case 'MultiLineString':
      coords4326 = convertMultiLineString(projection, geometry.coordinates)
      break
    default:
      throw Error('Unsupported feature type')
  }

  return coords4326
}
