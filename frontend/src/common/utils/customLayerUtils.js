import csv2geojson from 'csv2geojson'
import { kml } from '@tmcw/togeojson'
import XLSX from 'xlsx'

export function groupErrorsByRow (errors) {
  // returns a new array containing a single object representing each row.
  let rowMap = {}
  let groupedErrors = []

  errors.forEach(r => {
    if (!rowMap[r.index]) {
      groupedErrors.push(r)
      rowMap[r.index] = true // mark row as seen
    }
  })
  return groupedErrors
}

export function createMessageFromErrorArray (errors) {
  if (!errors || !errors.length) {
    return ''
  }
  const numErrs = errors.length

  // get the first error.
  // some users spreadsheets have hundreds of rows so we won't
  // be able to show all possible errors.
  const firstErrRow = errors.map(e => e.index)[0]
  const firstErrMsg = errors.map(e => e.message)[0]

  let msg = `error on row ${firstErrRow}: ${firstErrMsg}`

  // show number of additional errors e.g. "and 2 more errors"
  if (numErrs > 1) {
    msg = `${msg} (and ${numErrs - 1} more ${numErrs === 2 ? 'error' : 'errors'})`
  }
  return msg
}

export function xlsxToGeoJSON (file) {
  // file should be of type Uint8Array
  // returns a promise (via csvToGeoJSON)

  const workbook = XLSX.read(file, { type: 'array' })
  const firstSheet = workbook.Sheets[workbook.SheetNames[0]]

  const csvData = XLSX.utils.sheet_to_csv(firstSheet, { blankrows: false })

  // Converting from xlsx directly to geojson would be more efficient
  // but we can only handle csv-like spreadsheets right now, so
  // by converting to csv first we can take advantage of the csv2geojson
  // library.
  return csvToGeoJSON(csvData)
}

export function kmlToGeoJSON (xml) {
  return kml(new DOMParser().parseFromString(xml, 'text/xml'))
}

export function csvToGeoJSON (file) {
  return new Promise((resolve, reject) => {
    csv2geojson.csv2geojson(file, (errors, data) => {
      if (data && data.features && data.features.length) {
        // check to make sure that features were given a geometry.
        // this can occur if the file was read but no lat/long columns were found.
        if (
          data.features &&
            data.features.length &&
            !data.features.map(f => f.geometry).filter(Boolean).length) {
          reject(new Error('could not find valid longitude and latitude headings in file.'))
        }
        resolve({ data, errors })
      } else {
        console.error(errors)

        const numErrs = errors && errors.length
        if (numErrs && numErrs > 0) {
          reject(new Error(createMessageFromErrorArray(errors)))
        }
        reject(new Error('An error occured loading file'))
      }
    })
  })
}

// from a FeatureCollection `fc`, return an array
// of the geometry types contained within the FeatureCollection.
export function layerGeometryTypes (fc) {
  let typeMap = {}
  let types = []

  fc.features.forEach(f => {
    // skip features with no geometry.
    if (!f.geometry) {
      return
    }

    const geomType = f.geometry.type

    // special handling for GeometryCollections
    // a GeometryCollection should have a `geometries` member which is an array
    // of geometries.  Ideally, GeometryCollections won't be nested.
    // this code block grabs the unique geometries and adds them to the type list (if
    // they haven't already been seen)
    if (geomType === 'GeometryCollection') {
      const collectionTypes = [...new Set(f.geometry.geometries.map(g => g.type))]
      collectionTypes.forEach(t => {
        if (!typeMap[t]) {
          typeMap[t] = true
          types.push(t)
        }
      })
      return
    }

    if (!typeMap[geomType]) {
      typeMap[geomType] = true
      types.push(geomType)
    }
  })
  return types
}
