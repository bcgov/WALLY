import { FILE_TYPES_ACCEPTED } from './customLayerUtils'

export function getFileExtension (filename) {
  if (!filename || !filename.length) {
    // basic check for validity before trying to parse filename
    console.warn(`invalid filename ${filename}`)
    return null
  }

  const filenameParts = filename.split('.')

  if (filenameParts.length === 1) {
    console.warn(`invalid filename ${filename}`)
    return null
  }
  return filenameParts[filenameParts.length - 1]
}

export function getDefaultFileStats (file) {
  if (!file) {
    return null
  }

  return {
    size: file.size,
    name: file.name,
    type: file.type
  }
}

export function generateFileStats (file) {
  const geojsonFc = file['data']

  const geojsonStats = {
    id: `${file.name}.${file.lastModified}`,
    fileType: file['type'],
    numFeatures: geojsonFc.features.length,
    geomType: geojsonFc.features[0].geometry.type,
    propertyFields: Object.keys(geojsonFc.features[0].properties)
  }
  return Object.assign({}, getDefaultFileStats(file), geojsonStats)
}

export function determineFileReadMethod (fileType) {
  const methods = {
    'geojson': 'text',
    'csv': 'text',
    'xlsx': 'arrayBuffer',
    'shapefile': 'arrayBuffer',
    'kml': 'text'
  }
  return methods[fileType]
}

export function determineFileType (filename) {
  const extension = getFileExtension(filename)
  for (const fileType of Object.keys(FILE_TYPES_ACCEPTED)) {
    if (FILE_TYPES_ACCEPTED[fileType].includes(extension)) {
      return {
        fileType: fileType,
        fileExtension: extension,
        fileSupported: true
      }
    }
  }

  // Could not determine file type based on file extension
  return {
    fileType: extension,
    fileExtension: extension,
    fileSupported: false
  }
}
