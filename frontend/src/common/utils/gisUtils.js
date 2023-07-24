
export function convertLineString (fromProjection, coordinates) {
  const newCoords = []
  coordinates.forEach(coords => {
    newCoords.push(fromProjection.inverse(coords))
  })
  return newCoords
}

export function convertMultiLineString (fromProjection, coordinates) {
  const newCoords = []
  coordinates.forEach(coords => {
    newCoords.push(convertLineString(fromProjection, coords))
  })
  return newCoords
}

/**
 *
 * @param projection proj4 instance
 * @param geometry A feature's geometry
 * @param geometry.type Geometry type to determine data structure
 * @param geometry.coordinates Coordinates to be converted
 * @returns geometry { Object } with converted coordinates
 */
export function convertGeometryCoords (projection, geometry) {
  if (geometry === null) {
    return null
  }

  let coords4326 = []

  switch (geometry.type) {
    case 'Point':
      coords4326 = projection.inverse(geometry.coordinates)
      break
    case 'LineString':
      coords4326 = convertLineString(projection, geometry.coordinates)
      break
    case 'MultiLineString':
      coords4326 = convertMultiLineString(projection, geometry.coordinates)
      break
    default:
      throw Error(`Unsupported feature type ${geometry.type}`)
  }

  return coords4326
}
