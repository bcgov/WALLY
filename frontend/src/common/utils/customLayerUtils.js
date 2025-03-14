import csv2geojson from 'csv2geojson'
import { kml } from '@tmcw/togeojson'
import XLSX from 'xlsx'
import proj4 from 'proj4'
import * as shapefile from 'shapefile'
import {
  convertGeometryCoords
} from './gisUtils'
import { featureCollection } from '../mapbox/features'

export const FILE_TYPE_SHAPEFILE = 'shapefile'
export const FILE_TYPES_ACCEPTED = {
  geojson: ['geojson', 'json'],
  [FILE_TYPE_SHAPEFILE]: ['shp', 'dbf', 'prj'], // add zip file
  csv: ['csv'],
  xlsx: ['xls', 'xlsx'],
  kml: ['kml']
}

export function groupErrorsByRow (errors) {
  // returns a new array containing a single object representing each row.
  const rowMap = {}
  const groupedErrors = []

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

export function shapefileToGeoJSON (shpfile, dbffile = null, projection = null) {
  const proj = projection ? proj4(projection) : null

  return new Promise((resolve, reject) => {
    const features = []

    shapefile.open(shpfile, dbffile)
      .then(source => source.read()
        .then(function log (result) {
          if (result.done) {
            resolve(featureCollection(features))
            return
          }
          const feature = result.value

          // Convert coordinates based on projection file
          if (projection && feature.geometry && feature.geometry.coordinates) {
            feature.geometry.coordinates = convertGeometryCoords(proj,
              feature.geometry)
          }

          features.push(feature)
          return source.read().then(log)
        }))
      .catch(error => {
        reject(new Error(error.stack))
        console.error(error.stack)
      })
  })
}
