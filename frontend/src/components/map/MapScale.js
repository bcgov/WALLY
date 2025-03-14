// Returns the width of the map view in meters
export default (map) => {
  const maxWidth = 100 // relative pixel distance as maxwidth
  const y = map._container.clientHeight / 2

  const latlng1 = map.unproject([0, y])
  const latlng2 = map.unproject([maxWidth, y])

  const R = 6371000
  const rad = Math.PI / 180
  const lat1 = latlng1.lat * rad
  const lat2 = latlng2.lat * rad
  const a = Math.sin(lat1) * Math.sin(lat2) +
          Math.cos(lat1) * Math.cos(lat2) * Math.cos((latlng2.lng - latlng1.lng) * rad)

  const maxMeters = R * Math.acos(Math.min(a, 1))

  return maxMeters
}
