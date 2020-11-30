import csv2geojson from 'csv2geojson'
import { kml } from '@tmcw/togeojson'
import XLSX from 'xlsx'
import * as shapefile from 'shapefile'

export const FILE_TYPES_ACCEPTED = {
  'geojson': ['geojson', 'json'],
  'shapefile': ['shp', 'dbf', 'shx'], // add zip file
  'csv': ['csv'],
  'xlsx': ['xls', 'xlsx'],
  'kml': ['kml']
}

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
